#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Honeypot Attack Simulator
-------------------------

Recreated high-volume attack simulator for HoneyTrace.

Generates realistic Git / CI/CD / credentials / brute-force / malformed / scan
traffic against the unified honeypot + logging server so that:
- ML ensemble gets rich data (ml_score, ml_risk_level, is_anomaly)
- Dashboard pages (Dashboard, Map, ML Insights, Alerts, Investigation) show
  non‑zero, dynamic values.

Usage (examples):
  python honeypot_attack_simulator.py --count 100 --mode mixed
  python honeypot_attack_simulator.py --count 10000 --mode mixed --concurrency 50 --force
"""

import argparse
import datetime
import random
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

import requests

DEFAULT_LOGGING_SERVER_URL = "http://localhost:5000/log"

USER_AGENT_POOL = [
    "curl/7.68.0",
    "curl/8.0.1",
    "wget/1.20.3",
    "python-requests/2.31.0",
    "git/2.34.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
]

SENSITIVE_FILES = [
    ".env",
    ".env.production",
    "config/secrets.yml",
    "config/credentials.yml.enc",
    "config/config.json",
    "docker-compose.yml",
    "k8s/deploy.yaml",
    "terraform/main.tf",
    "aws/credentials",
    "id_rsa",
    "private.key",
]

MALICIOUS_COMMIT_MESSAGES = [
    "Add malicious backdoor",
    "Inject payload",
    "Bypass security checks",
    "Remove authentication",
    "Disable firewall rules",
    "Add remote shell",
    "Backdoor access",
]


def random_public_ip() -> str:
    """Generate a random public IPv4 address (excluding private ranges)."""
    while True:
        a = random.randint(1, 223)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        d = random.randint(1, 254)
        # Exclude private and reserved ranges
        if a == 10 or (a == 172 and 16 <= b <= 31) or (a == 192 and b == 168) or a >= 224:
            continue
        return f"{a}.{b}.{c}.{d}"


def random_private_ip() -> str:
    """Generate a random private IPv4 address (for internal attacker simulation)."""
    return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"


def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def session_id_for_ip(ip: str) -> str:
    """Stable session id per IP to simulate persistent sessions."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"session-{ip}"))


# -----------------------------------------------------------------------------
# Attack generators
# -----------------------------------------------------------------------------


def gen_git_push(ip: str) -> Dict[str, Any]:
    malicious = random.random() < 0.5
    commit_message = random.choice(MALICIOUS_COMMIT_MESSAGES if malicious else ["Fix bug", "Refactor code"])
    files_changed = [
        "src/app.py",
        "README.md",
    ]
    if malicious:
        files_changed += ["src/backdoor.py", "config/secrets.yml"]

    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake Git Repository",
        "action": "git_push",
        "target_file": None,
        "payload": {
            "commit_message": commit_message,
            "branch": random.choice(["main", "master", "dev", "staging"]),
            "files_changed": files_changed,
            "file_count": len(files_changed),
        },
        "headers": {
            "User-Agent": random.choice(["git/2.34.1", "git/2.32.0"]),
            "Content-Type": "application/json",
        },
        "session_id": session_id_for_ip(ip),
        "user_agent": random.choice(["git/2.34.1", "git/2.32.0"]),
    }


def gen_file_access(ip: str) -> Dict[str, Any]:
    target_file = random.choice(SENSITIVE_FILES)
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake Git Repository",
        "action": "file_access",
        "target_file": target_file,
        "payload": {
            "file_type": "secrets" if any(s in target_file for s in [".env", "secret", "credentials", "id_rsa"]) else "config",
            "file_size": random.randint(100, 5000),
            "access_method": random.choice(["direct_request", "raw_url", "api_endpoint"]),
            "path": f"/repo/{target_file}",
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENT_POOL),
            "Accept": "application/json,text/plain,*/*",
        },
        "session_id": session_id_for_ip(ip),
        "user_agent": random.choice(USER_AGENT_POOL),
    }


def gen_cicd_job(ip: str) -> Dict[str, Any]:
    malicious = random.random() < 0.4
    job_name = random.choice(
        [
            "deploy-production",
            "run-tests",
            "security-scan",
            "exfiltrate-data",
            "install-backdoor",
        ]
    )
    if malicious:
        job_name = random.choice(["install-backdoor", "crypto-miner", "reverse-shell"])

    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake CI/CD Runner",
        "action": "ci_job_run",
        "target_file": None,
        "payload": {
            "job_name": job_name,
            "pipeline_id": random.randint(1000, 9999),
            "branch": random.choice(["main", "dev", "feature/secret-change"]),
            "contains_secrets": malicious,
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENT_POOL),
            "Authorization": f"Bearer fake_token_{random.randint(1000, 9999)}",
        },
        "session_id": session_id_for_ip(ip),
        "user_agent": random.choice(USER_AGENT_POOL),
    }


def gen_credentials_access(ip: str) -> Dict[str, Any]:
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake CI/CD Runner",
        "action": "ci_credentials_access",
        "target_file": "config/credentials.yml.enc",
        "payload": {
            "path": "config/credentials.yml.enc",
            "reason": random.choice(["deploy", "debug", "script"]),
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENT_POOL),
        },
        "session_id": session_id_for_ip(ip),
        "user_agent": random.choice(USER_AGENT_POOL),
    }


def gen_bruteforce(ip: str) -> Dict[str, Any]:
    username = random.choice(["admin", "root", "ci-user", "devops"])
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "TCP",
        "target_service": "Fake Git Repository",
        "action": "bruteforce_login",
        "target_file": None,
        "payload": {
            "username": username,
            "password": f"Pass{random.randint(1000, 9999)}!",
            "attempt": random.randint(1, 10),
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENT_POOL),
        },
        "session_id": session_id_for_ip(ip),
        "user_agent": random.choice(USER_AGENT_POOL),
    }


def gen_malformed(ip: str) -> Dict[str, Any]:
    payload = "A" * random.randint(2000, 8000)
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake Git Repository",
        "action": "malformed_payload",
        "target_file": None,
        "payload": {
            "raw": payload,
            "content_type": random.choice(["text/plain", "application/json"]),
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENT_POOL),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        "session_id": session_id_for_ip(ip),
        "user_agent": random.choice(USER_AGENT_POOL),
    }


def gen_scan(ip: str) -> Dict[str, Any]:
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "TCP",
        "target_service": "Unified Honeypot",
        "action": "scan_attempt",
        "target_file": None,
        "payload": {
            "ports_scanned": random.sample([22, 80, 443, 8000, 8001, 8002, 5432], k=4),
            "tool": random.choice(["nmap", "masscan", "custom"]),
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENT_POOL),
        },
        "session_id": session_id_for_ip(ip),
        "user_agent": random.choice(USER_AGENT_POOL),
    }


ATTACK_GENERATORS = {
    "git_push": gen_git_push,
    "file_access": gen_file_access,
    "ci_job_run": gen_cicd_job,
    "cred_access": gen_credentials_access,
    "bruteforce": gen_bruteforce,
    "malformed": gen_malformed,
    "scan_attempt": gen_scan,
}


def choose_attack_type(mode: str) -> str:
    if mode == "mixed":
        weights = {
            "git_push": 25,
            "file_access": 25,
            "ci_job_run": 15,
            "cred_access": 10,
            "bruteforce": 10,
            "malformed": 10,
            "scan_attempt": 5,
        }
        types = list(weights.keys())
        probs = list(weights.values())
        return random.choices(types, weights=probs)[0]
    if mode in ATTACK_GENERATORS:
        return mode
    return random.choice(list(ATTACK_GENERATORS.keys()))


# -----------------------------------------------------------------------------
# HTTP helpers
# -----------------------------------------------------------------------------


def send_log(server_url: str, log: Dict[str, Any], timeout: int = 5) -> Dict[str, Any]:
    try:
        resp = requests.post(server_url, json=log, timeout=timeout)
        ok = 200 <= resp.status_code < 300
        try:
            body = resp.json()
        except Exception:
            body = None
        return {
            "success": ok,
            "status_code": resp.status_code,
            "response": body,
        }
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "error": str(e),
        }


def check_health(base_url: str) -> bool:
    try:
        resp = requests.get(base_url.rstrip("/").replace("/log", "") + "/health", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


# -----------------------------------------------------------------------------
# Simulator
# -----------------------------------------------------------------------------


class AttackSimulator:
    def __init__(self, server_url: str, timeout: int = 5):
        self.server_url = server_url
        self.timeout = timeout
        self.stats = {"success": 0, "failed": 0}

    def simulate_one(self, attack_type: str, ip: Optional[str] = None, verbose: bool = False) -> Dict[str, Any]:
        if ip is None:
            ip = random_public_ip() if random.random() > 0.3 else random_private_ip()
        if attack_type not in ATTACK_GENERATORS:
            attack_type = "git_push"
        log = ATTACK_GENERATORS[attack_type](ip)
        result = send_log(self.server_url, log, timeout=self.timeout)
        result["attack_type"] = attack_type
        result["source_ip"] = ip
        result["timestamp"] = now_iso()
        if result.get("success"):
            self.stats["success"] += 1
        else:
            self.stats["failed"] += 1
        if verbose:
            status = "[OK]" if result.get("success") else "[FAIL]"
            print(f"{status} {attack_type:15s} from {ip:15s} -> {result.get('status_code')}")
        return result

    def run(
        self,
        count: int,
        mode: str = "mixed",
        concurrency: int = 1,
        delay: float = 0.0,
        verbose: bool = False,
    ) -> None:
        print(f"[*] Starting attack simulation")
        print(f"    Target: {self.server_url}")
        print(f"    Count: {count}")
        print(f"    Mode: {mode}")
        print(f"    Concurrency: {concurrency}")
        start = time.time()
        self.stats = {"success": 0, "failed": 0}

        if concurrency <= 1:
            for i in range(count):
                attack_type = choose_attack_type(mode)
                self.simulate_one(attack_type, verbose=verbose)
                if delay > 0:
                    time.sleep(delay)
                if (i + 1) % max(1, count // 10) == 0:
                    print(f"    Progress: {i + 1}/{count} ({(i + 1) * 100.0 / count:.1f}%)")
        else:
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = []
                for _ in range(count):
                    attack_type = choose_attack_type(mode)
                    futures.append(executor.submit(self.simulate_one, attack_type, None, False))
                    if delay > 0:
                        time.sleep(delay)
                completed = 0
                for f in as_completed(futures):
                    completed += 1
                    _ = f.result()
                    if completed % max(1, count // 10) == 0:
                        print(f"    Progress: {completed}/{count} ({completed * 100.0 / count:.1f}%)")

        elapsed = time.time() - start
        print()
        print("=" * 60)
        print("ATTACK SIMULATION SUMMARY")
        print("=" * 60)
        print(f"Total attacks: {count}")
        print(f"Successful:   {self.stats['success']}")
        print(f"Failed:       {self.stats['failed']}")
        if elapsed > 0:
            print(f"Duration:     {elapsed:.2f}s  ({count / elapsed:.2f} attacks/sec)")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Honeypot Attack Simulator - generate attack traffic for HoneyTrace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python honeypot_attack_simulator.py --count 100 --mode mixed
  python honeypot_attack_simulator.py --count 10000 --mode mixed --concurrency 50 --force
""",
    )
    parser.add_argument("--url", default=DEFAULT_LOGGING_SERVER_URL, help="Logging server /log URL")
    parser.add_argument("--count", type=int, default=100, help="Number of attacks to generate")
    parser.add_argument(
        "--mode",
        default="mixed",
        choices=["mixed"] + list(ATTACK_GENERATORS.keys()),
        help="Which attack type to generate",
    )
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent workers")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay between attacks (seconds)")
    parser.add_argument("--timeout", type=int, default=5, help="Request timeout in seconds")
    parser.add_argument("--force", action="store_true", help="Skip safety confirmation prompt")
    parser.add_argument("--verbose", action="store_true", help="Verbose output per attack")
    args = parser.parse_args()

    print("=" * 60)
    print("HONEYPOT ATTACK SIMULATOR")
    print("=" * 60)
    print("SAFETY WARNING:")
    print("  This tool sends simulated attacks to your logging server.")
    print("  Only use against your own HoneyTrace lab environment.")
    print()

    if not args.force:
        ans = input("Proceed with attack simulation? (yes/no): ").strip().lower()
        if ans not in ("yes", "y"):
            print("Aborted.")
            sys.exit(0)

    base = args.url
    if not base.endswith("/log"):
        base = base.rstrip("/") + "/log"

    if not check_health(base):
        print("[!] Logging server health check failed or server not running.")
        cont = input("Continue anyway? (yes/no): ").strip().lower()
        if cont not in ("yes", "y"):
            print("Aborted.")
            sys.exit(1)

    sim = AttackSimulator(server_url=base, timeout=args.timeout)
    try:
        sim.run(
            count=args.count,
            mode=args.mode,
            concurrency=args.concurrency,
            delay=args.delay,
            verbose=args.verbose,
        )
        print("[*] Simulation completed. Check dashboard at http://localhost:3000")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()



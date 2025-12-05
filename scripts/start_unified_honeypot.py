#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Honeypot System Startup Script
Starts all honeypot services and the logging server together
Windows-compatible version (no emojis)
"""

import subprocess
import sys
import os
import time
import threading
import signal
import requests
from datetime import datetime

class HoneypotManager:
    def __init__(self):
        self.processes = {}
        self.running = True
        
        # Service configurations
        self.services = {
            'logging_server': {
                'script': 'logging_server/logging_server.py',
                'port': 5000,
                'name': 'Logging Server',
                'description': 'Centralized logging and analytics'
            },
            'fake_git_repo': {
                'script': 'fake_git_repo.py',
                'port': 8001,
                'name': 'Fake Git Repository',
                'description': 'Git repository honeypot'
            },
            'fake_cicd_runner': {
                'script': 'fake_cicd_runner.py',
                'port': 8002,
                'name': 'Fake CI/CD Runner',
                'description': 'CI/CD runner honeypot'
            },
            'consolidated_honeypot': {
                'script': 'Honeypot/honeypot_services.py',
                'port': 8000,
                'name': 'Consolidated Honeypot',
                'description': 'Combined Git & CI/CD services'
            }
        }
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        try:
            import flask
            import requests
            print("[OK] Dependencies are installed")
            return True
        except ImportError as e:
            print(f"[ERROR] Missing dependency: {e}")
            print("[INFO] Install dependencies with: pip install Flask requests")
            return False
    
    def start_service(self, service_name, config):
        """Start a single service"""
        script_path = config['script']
        
        if not os.path.exists(script_path):
            print(f"[WARN] {config['name']}: Script not found ({script_path})")
            return None
        
        try:
            print(f"[*] Starting {config['name']} on port {config['port']}...")
            
            # Determine working directory based on script location
            if '/' in script_path or '\\' in script_path:
                script_dir = os.path.dirname(script_path)
                if script_dir:
                    script_file = os.path.basename(script_path)
                    cwd = os.path.abspath(script_dir)
                    full_script = os.path.join(cwd, script_file)
                else:
                    cwd = None
                    full_script = os.path.abspath(script_path)
            else:
                cwd = None
                full_script = os.path.abspath(script_path)
            
            process = subprocess.Popen(
                [sys.executable, full_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd if cwd else None,
                encoding='utf-8',
                errors='replace'
            )
            
            # Wait a moment to check if the process started successfully
            time.sleep(2)
            
            if process.poll() is None:  # Process is still running
                print(f"[OK] {config['name']} started successfully (PID: {process.pid})")
                return process
            else:
                stdout, stderr = process.communicate()
                print(f"[ERROR] {config['name']} failed to start")
                if stderr:
                    error_lines = stderr.strip().split('\n')
                    # Show first few error lines
                    for line in error_lines[:5]:
                        if line.strip():
                            print(f"   {line}")
                return None
                
        except Exception as e:
            print(f"[ERROR] Error starting {config['name']}: {e}")
            return None
    
    def check_service_health(self, service_name, config):
        """Check if a service is responding"""
        try:
            response = requests.get(f"http://localhost:{config['port']}/health", timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        return False
    
    def start_all_services(self):
        """Start all honeypot services"""
        print("Starting Unified Honeypot System...")
        print("=" * 60)
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Start services in order (logging server first)
        service_order = ['logging_server', 'fake_git_repo', 'fake_cicd_runner', 'consolidated_honeypot']
        
        for service_name in service_order:
            if service_name in self.services:
                config = self.services[service_name]
                process = self.start_service(service_name, config)
                
                if process:
                    self.processes[service_name] = process
                    time.sleep(1)  # Give services time to start
                else:
                    print(f"[WARN] Continuing without {config['name']}")
        
        return len(self.processes) > 0
    
    def monitor_services(self):
        """Monitor running services"""
        print("\nService Status:")
        print("-" * 40)
        
        for service_name, process in self.processes.items():
            config = self.services[service_name]
            
            if process.poll() is None:  # Process is running
                health_status = "[OK] Healthy" if self.check_service_health(service_name, config) else "[*] Starting"
                print(f"{config['name']:<25} | Port {config['port']:<5} | {health_status}")
            else:
                print(f"{config['name']:<25} | Port {config['port']:<5} | [STOPPED]")
    
    def show_service_info(self):
        """Show information about running services"""
        print("\nAvailable Services:")
        print("-" * 40)
        
        for service_name, config in self.services.items():
            if service_name in self.processes:
                print(f"[*] {config['name']}")
                print(f"   URL: http://localhost:{config['port']}")
                print(f"   Description: {config['description']}")
                print()
    
    def show_endpoints(self):
        """Show available endpoints"""
        print("Available Endpoints:")
        print("-" * 40)
        
        print("Logging Server (Port 5000):")
        print("   GET  /health - Health check")
        print("   GET  /stats - Statistics")
        print("   GET  /logs - Retrieve logs")
        print("   POST /log - Ingest logs")
        print()
        
        print("Fake Git Repository (Port 8001):")
        print("   GET  / - Repository info")
        print("   POST /repo/push - Git push")
        print("   POST /repo/pull - Git pull")
        print("   GET  /.env - Environment file")
        print("   GET  /secrets.yml - Secrets file")
        print()
        
        print("Fake CI/CD Runner (Port 8002):")
        print("   GET  / - CI/CD dashboard")
        print("   POST /ci/run - Execute job")
        print("   GET  /ci/status - Job status")
        print("   GET  /ci/logs/<job_id> - Job logs")
        print("   GET  /ci/credentials - Credentials")
        print()
        
        print("Consolidated Honeypot (Port 8000):")
        print("   GET  / - Service info")
        print("   GET  /health - Health check")
        print("   All Git & CI/CD endpoints combined")
        print()
    
    def run_tests(self):
        """Run basic connectivity tests"""
        print("Running Connectivity Tests...")
        print("-" * 40)
        
        test_results = {}
        
        for service_name, config in self.services.items():
            if service_name in self.processes:
                try:
                    response = requests.get(f"http://localhost:{config['port']}/health", timeout=5)
                    if response.status_code == 200:
                        test_results[service_name] = "[OK] PASS"
                    else:
                        test_results[service_name] = f"[ERROR] FAIL (Status: {response.status_code})"
                except Exception as e:
                    test_results[service_name] = f"[ERROR] FAIL ({str(e)[:30]}...)"
            else:
                test_results[service_name] = "[SKIP] Not running"
        
        for service_name, result in test_results.items():
            config = self.services[service_name]
            print(f"{config['name']:<25} | {result}")
    
    def stop_all_services(self):
        """Stop all running services"""
        print("\nStopping all services...")
        
        for service_name, process in self.processes.items():
            config = self.services[service_name]
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"[OK] {config['name']} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"[OK] {config['name']} force stopped")
            except Exception as e:
                print(f"[ERROR] Error stopping {config['name']}: {e}")
        
        self.processes.clear()
        print("[OK] All services stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.running = False
        self.stop_all_services()
        sys.exit(0)
    
    def run(self):
        """Main execution loop"""
        # Set up signal handlers
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, self.signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Start all services
            if not self.start_all_services():
                print("[ERROR] Failed to start any services")
                return
            
            # Show service information
            self.monitor_services()
            self.show_service_info()
            self.show_endpoints()
            
            # Run tests
            time.sleep(3)  # Give services time to fully start
            self.run_tests()
            
            print("\n" + "=" * 60)
            print("[SUCCESS] Unified Honeypot System is running!")
            print("[INFO] Press Ctrl+C to stop all services")
            print("[INFO] Monitor logs in real-time")
            print("[INFO] Check http://localhost:5000/stats for analytics")
            print("=" * 60)
            
            # Keep running until interrupted
            while self.running:
                time.sleep(10)
                
                # Check if any services have died
                dead_services = []
                for service_name, process in self.processes.items():
                    if process.poll() is not None:
                        dead_services.append(service_name)
                
                if dead_services:
                    print(f"\n[WARN] Services stopped unexpectedly: {', '.join(dead_services)}")
                    for service_name in dead_services:
                        del self.processes[service_name]
                
                # Show periodic status
                if len(self.processes) > 0:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {len(self.processes)} services running")
        
        except KeyboardInterrupt:
            print("\nShutdown requested by user")
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
        finally:
            self.stop_all_services()

def main():
    """Main entry point"""
    manager = HoneypotManager()
    manager.run()

if __name__ == "__main__":
    main()

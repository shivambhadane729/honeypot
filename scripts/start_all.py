#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Honeypot System Startup Script
Starts all services: Logging Server, Honeypot Services, and Frontend Dashboard
Works with the new organized folder structure
"""

import subprocess
import sys
import os
import time
import threading
import signal
import requests
from datetime import datetime

# Get the project root directory (parent of scripts folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class HoneypotSystemManager:
    def __init__(self):
        self.processes = {}
        self.running = True
        
        # Service configurations with updated paths
        self.services = {
            'logging_server': {
                'script': os.path.join(PROJECT_ROOT, 'logging_server', 'logging_server.py'),
                'port': 5000,
                'name': 'Logging Server',
                'description': 'Centralized logging and ML analytics',
                'cwd': os.path.join(PROJECT_ROOT, 'logging_server')
            },
            'fake_git_repo': {
                'script': os.path.join(PROJECT_ROOT, 'scripts', 'fake_git_repo.py'),
                'port': 8001,
                'name': 'Fake Git Repository',
                'description': 'Git repository honeypot',
                'cwd': PROJECT_ROOT
            },
            'fake_cicd_runner': {
                'script': os.path.join(PROJECT_ROOT, 'scripts', 'fake_cicd_runner.py'),
                'port': 8002,
                'name': 'Fake CI/CD Runner',
                'description': 'CI/CD runner honeypot',
                'cwd': PROJECT_ROOT
            },
            'consolidated_honeypot': {
                'script': os.path.join(PROJECT_ROOT, 'Honeypot', 'honeypot_services.py'),
                'port': 8000,
                'name': 'Consolidated Honeypot',
                'description': 'Combined Git & CI/CD services',
                'cwd': os.path.join(PROJECT_ROOT, 'Honeypot')
            }
        }
        
        self.frontend_path = os.path.join(PROJECT_ROOT, 'db1')
        self.frontend_port = 3000
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        try:
            import flask
            import requests
            print("[OK] Python dependencies are installed")
            return True
        except ImportError as e:
            print(f"[ERROR] Missing Python dependency: {e}")
            print("[INFO] Install with: pip install Flask requests")
            return False
    
    def check_node_installed(self):
        """Check if Node.js is installed for frontend"""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            if result.returncode == 0:
                print(f"[OK] Node.js is installed ({result.stdout.strip()})")
                return True
        except:
            pass
        print("[WARN] Node.js not found - Frontend will not start")
        print("[INFO] Install Node.js from https://nodejs.org/")
        return False
    
    def start_service(self, service_name, config):
        """Start a single service"""
        script_path = config['script']
        
        if not os.path.exists(script_path):
            print(f"[WARN] {config['name']}: Script not found ({script_path})")
            return None
        
        try:
            print(f"[*] Starting {config['name']} on port {config['port']}...")
            
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=config.get('cwd', PROJECT_ROOT),
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
                    for line in error_lines[:5]:
                        if line.strip():
                            print(f"   {line}")
                return None
                
        except Exception as e:
            print(f"[ERROR] Error starting {config['name']}: {e}")
            return None
    
    def start_frontend(self):
        """Start the React frontend dashboard"""
        if not os.path.exists(self.frontend_path):
            print(f"[WARN] Frontend directory not found: {self.frontend_path}")
            return None
        
        if not self.check_node_installed():
            return None
        
        try:
            print(f"[*] Starting Frontend Dashboard on port {self.frontend_port}...")
            
            # Check if node_modules exists
            node_modules = os.path.join(self.frontend_path, 'node_modules')
            if not os.path.exists(node_modules):
                print("[INFO] Installing frontend dependencies...")
                install_process = subprocess.run(
                    ['npm', 'install'],
                    cwd=self.frontend_path,
                    capture_output=True,
                    timeout=120
                )
                if install_process.returncode != 0:
                    print("[ERROR] Failed to install frontend dependencies")
                    return None
            
            process = subprocess.Popen(
                ['npm', 'start'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.frontend_path,
                encoding='utf-8',
                errors='replace'
            )
            
            time.sleep(5)  # Frontend takes longer to start
            
            if process.poll() is None:
                print(f"[OK] Frontend Dashboard started successfully (PID: {process.pid})")
                return process
            else:
                print("[ERROR] Frontend Dashboard failed to start")
                return None
                
        except Exception as e:
            print(f"[ERROR] Error starting Frontend Dashboard: {e}")
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
    
    def start_all_services(self, include_frontend=True):
        """Start all honeypot services"""
        print("=" * 70)
        print("HoneyTrace - Multi-Layer Honeypot System")
        print("Starting All Services...")
        print("=" * 70)
        print()
        
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
                    time.sleep(2)  # Give services time to start
                else:
                    print(f"[WARN] Continuing without {config['name']}")
        
        # Start frontend if requested
        if include_frontend:
            frontend_process = self.start_frontend()
            if frontend_process:
                self.processes['frontend'] = frontend_process
        
        return len(self.processes) > 0
    
    def monitor_services(self):
        """Monitor running services"""
        print("\n" + "=" * 70)
        print("Service Status")
        print("=" * 70)
        print(f"{'Service':<30} {'Port':<10} {'Status':<20}")
        print("-" * 70)
        
        for service_name, process in self.processes.items():
            if service_name == 'frontend':
                if process.poll() is None:
                    print(f"{'Frontend Dashboard':<30} {'3000':<10} {'[OK] Running':<20}")
                else:
                    print(f"{'Frontend Dashboard':<30} {'3000':<10} {'[STOPPED]':<20}")
            else:
                config = self.services[service_name]
                if process.poll() is None:  # Process is running
                    health_status = "[OK] Healthy" if self.check_service_health(service_name, config) else "[*] Starting"
                    print(f"{config['name']:<30} {str(config['port']):<10} {health_status:<20}")
                else:
                    print(f"{config['name']:<30} {str(config['port']):<10} {'[STOPPED]':<20}")
    
    def show_service_info(self):
        """Show information about running services"""
        print("\n" + "=" * 70)
        print("Service URLs")
        print("=" * 70)
        
        for service_name, config in self.services.items():
            if service_name in self.processes:
                print(f"[*] {config['name']}")
                print(f"   URL: http://localhost:{config['port']}")
                print(f"   Description: {config['description']}")
                print()
        
        if 'frontend' in self.processes:
            print("[*] Frontend Dashboard")
            print(f"   URL: http://localhost:{self.frontend_port}")
            print("   Description: React-based visualization dashboard")
            print()
    
    def show_endpoints(self):
        """Show available endpoints"""
        print("=" * 70)
        print("Available Endpoints")
        print("=" * 70)
        
        print("\nLogging Server (Port 5000):")
        print("   GET  /health - Health check")
        print("   GET  /stats - Statistics")
        print("   GET  /logs - Retrieve logs")
        print("   POST /log - Ingest logs")
        print("   GET  /api/ml-insights - ML model insights")
        print("   GET  /api/live-events - Real-time events")
        print("   GET  /api/analytics - Analytics data")
        print("   GET  /api/map-data - Geographic data")
        print()
        
        print("Fake Git Repository (Port 8001):")
        print("   GET  / - Repository info")
        print("   GET  /.env - Environment file")
        print("   GET  /secrets.yml - Secrets file")
        print()
        
        print("Fake CI/CD Runner (Port 8002):")
        print("   GET  / - CI/CD dashboard")
        print("   GET  /ci/credentials - Credentials")
        print()
        
        print("Consolidated Honeypot (Port 8000):")
        print("   GET  / - Service info")
        print("   GET  /health - Health check")
        print("   All Git & CI/CD endpoints combined")
        print()
    
    def run_tests(self):
        """Run basic connectivity tests"""
        print("=" * 70)
        print("Connectivity Tests")
        print("=" * 70)
        
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
            print(f"{config['name']:<30} | {result}")
    
    def stop_all_services(self):
        """Stop all running services"""
        print("\n" + "=" * 70)
        print("Stopping All Services...")
        print("=" * 70)
        
        for service_name, process in self.processes.items():
            service_display = 'Frontend Dashboard' if service_name == 'frontend' else self.services.get(service_name, {}).get('name', service_name)
            try:
                process.terminate()
                process.wait(timeout=5)
                print(f"[OK] {service_display} stopped")
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"[OK] {service_display} force stopped")
            except Exception as e:
                print(f"[ERROR] Error stopping {service_display}: {e}")
        
        self.processes.clear()
        print("\n[OK] All services stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.running = False
        self.stop_all_services()
        sys.exit(0)
    
    def run(self, include_frontend=True):
        """Main execution loop"""
        # Set up signal handlers
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, self.signal_handler)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Start all services
            if not self.start_all_services(include_frontend=include_frontend):
                print("[ERROR] Failed to start any services")
                return
            
            # Show service information
            self.monitor_services()
            self.show_service_info()
            self.show_endpoints()
            
            # Run tests
            time.sleep(5)  # Give services time to fully start
            self.run_tests()
            
            print("\n" + "=" * 70)
            print("[SUCCESS] HoneyTrace System is Running!")
            print("=" * 70)
            print("\n[INFO] Press Ctrl+C to stop all services")
            print("[INFO] Monitor logs in real-time")
            print("[INFO] Dashboard: http://localhost:3000")
            print("[INFO] Logging Server: http://localhost:5000/stats")
            print("=" * 70)
            
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
    import argparse
    
    parser = argparse.ArgumentParser(description='Start HoneyTrace Honeypot System')
    parser.add_argument('--no-frontend', action='store_true', 
                       help='Skip starting the frontend dashboard')
    args = parser.parse_args()
    
    manager = HoneypotSystemManager()
    manager.run(include_frontend=not args.no_frontend)

if __name__ == "__main__":
    main()


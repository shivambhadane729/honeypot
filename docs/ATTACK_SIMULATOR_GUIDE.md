# 🎯 Honeypot Attack Simulator Guide

## Overview

The **Honeypot Attack Simulator** (`honeypot_attack_simulator.py`) is a comprehensive tool for testing your honeypot system by generating realistic attacker behavior. It simulates various attack scenarios and sends them to your logging server, where they are automatically scored by your ML models and displayed on the dashboard.

## 🚀 Quick Start

### Basic Usage

```bash
# Quick test with 10 mixed attacks
python honeypot_attack_simulator.py --count 10

# Simulate 50 attacks with 5-second delay between each (realistic pace)
python honeypot_attack_simulator.py --count 50 --delay 5.0

# High-speed burst test (200 attacks with 10 concurrent workers)
python honeypot_attack_simulator.py --count 200 --concurrency 10
```

## 📋 Features

### Supported Attack Scenarios

1. **Git Repository Attacks**
   - `git_push` - Malicious commit pushes
   - `git_clone` - Repository cloning attempts
   - `git_fetch` - Fetch operations

2. **File Access Attacks**
   - `file_access` - Accessing sensitive files (`.env`, `secrets.yml`, etc.)
   - `cred_access` - Credentials file access

3. **CI/CD Attacks**
   - `ci_job_run` - Malicious CI/CD job execution
   - `api_abuse` - API endpoint abuse

4. **Brute-Force Attacks**
   - `bruteforce` - SSH login attempts

5. **Anomaly Attacks**
   - `malformed` - Malformed payloads (large payloads, invalid JSON, SQL injection, XSS)
   - `scan_attempt` - Port/endpoint scanning

### Attack Modes

- **`mixed`** (default) - Random mix of all attack types with realistic weights
- **`git_push`** - Only Git push attacks
- **`file_access`** - Only file access attacks
- **`bruteforce`** - Only brute-force attempts
- And more... (see `--help` for full list)

## 📖 Usage Examples

### Example 1: Quick Test

Test your system with a small number of attacks:

```bash
python honeypot_attack_simulator.py --count 10 --verbose
```

**Output:**
```
[*] Logging server is healthy
    Status: healthy
    Total logs: 0

[*] Starting attack simulation:
    Total attacks: 10
    Mode: mixed
    Concurrency: 1
    Delay: None

[OK] git_push       from 203.45.67.89   -> status=200
[OK] file_access    from 198.51.100.12  -> status=200
[OK] bruteforce     from 172.16.0.5     -> status=200
...
```

### Example 2: Realistic Simulation

Simulate realistic attacker behavior with delays:

```bash
python honeypot_attack_simulator.py --count 100 --delay 2.0 --mode mixed
```

This sends 100 attacks with a 2-second delay between each, creating a more realistic traffic pattern.

### Example 3: Burst Test (Demo Mode)

Generate high activity for dashboard visualization:

```bash
python honeypot_attack_simulator.py --count 500 --concurrency 20 --delay 0.01
```

This creates a burst of 500 attacks using 20 concurrent workers with minimal delay, perfect for:
- Testing ML model performance under load
- Generating spike visualizations on the dashboard
- Demonstrating real-time alert generation

### Example 4: Specific Attack Type

Test a specific attack scenario:

```bash
# Only test Git push attacks
python honeypot_attack_simulator.py --count 50 --mode git_push

# Only test brute-force attempts
python honeypot_attack_simulator.py --count 30 --mode bruteforce

# Only test file access attacks
python honeypot_attack_simulator.py --count 25 --mode file_access
```

### Example 5: Save Results to CSV

Save attack simulation results for analysis:

```bash
python honeypot_attack_simulator.py --count 100 --output attack_results.csv
```

## 🔧 Command-Line Options

```
--url URL           Logging server URL (default: http://localhost:5000)
--count N           Number of attacks to simulate (default: 10)
--mode MODE         Attack mode: mixed or specific type (default: mixed)
--concurrency N     Number of concurrent attacks (default: 1)
--delay SECONDS     Delay between attacks in seconds (default: 0.0)
--timeout SECONDS   Request timeout (default: 10)
--retries N         Retries on failure (default: 2)
--verbose           Show detailed output for each attack
--output FILE       Save results to CSV file
--force             Skip confirmation prompts
```

## 🎨 What Happens During Simulation?

1. **Attack Generation**
   - Random IP addresses (public and private)
   - Realistic attack payloads
   - Varied user agents and headers
   - Consistent session IDs per IP

2. **Log Submission**
   - Each attack is sent to `/log` endpoint
   - Server enriches with GeoIP data
   - ML models score each attack (Random Forest + Isolation Forest)
   - Results stored in database

3. **Dashboard Visualization**
   - Live Events page shows attacks in real-time
   - ML Insights page displays scores and predictions
   - Alerts page generates alerts for high-risk attacks
   - Analytics page shows attack trends
   - Map View shows geographic distribution

## 📊 Attack Distribution (Mixed Mode)

When using `--mode mixed`, attacks are distributed with realistic weights:

- Git push: 25%
- Git clone: 20%
- File access: 20%
- Git fetch: 15%
- Brute-force: 10%
- CI/CD job run: 10%
- Others: 5% each

## ⚠️ Safety & Best Practices

### ✅ Safe to Use

- ✅ Testing your own honeypot system
- ✅ Lab/demo environments
- ✅ Performance testing
- ✅ ML model validation

### ❌ Do NOT Use

- ❌ Against systems you don't own
- ❌ Against production systems without permission
- ❌ For actual malicious purposes
- ❌ On networks you don't control

## 🔍 Troubleshooting

### Server Not Responding

```bash
# Check if logging server is running
curl http://localhost:5000/health

# If not running, start it first
python logging_server/logging_server.py
```

### Connection Errors

- Verify the logging server URL with `--url`
- Check firewall settings
- Ensure the server is accessible

### Slow Performance

- Reduce `--concurrency` if experiencing timeouts
- Increase `--timeout` for slower networks
- Add `--delay` to reduce server load

## 📈 Integration with Dashboard

After running the simulator, check your dashboard:

1. **Live Events** - See attacks appearing in real-time
2. **ML Insights** - View ML scores and predictions
3. **Alerts** - Check generated alerts for high-risk attacks
4. **Analytics** - Analyze attack trends and patterns
5. **Map View** - Visualize geographic attack distribution
6. **Investigation** - Drill down into specific IP addresses

## 💡 Tips for Best Results

1. **Start Small** - Test with 10-20 attacks first
2. **Use Mixed Mode** - Most realistic for testing
3. **Add Delays** - `--delay 1.0` creates more realistic traffic
4. **Check Dashboard** - Monitor in real-time for best experience
5. **Save Results** - Use `--output` to track simulation history

## 🎯 Common Use Cases

### Testing ML Models

```bash
# Test with diverse attack types
python honeypot_attack_simulator.py --count 200 --mode mixed
```

### Demo/Presentation

```bash
# Create impressive spike for demo
python honeypot_attack_simulator.py --count 300 --concurrency 30 --delay 0.05
```

### Realistic Simulation

```bash
# Simulate realistic attack pattern
python honeypot_attack_simulator.py --count 100 --delay 5.0
```

### Performance Testing

```bash
# Test server under high load
python honeypot_attack_simulator.py --count 1000 --concurrency 50
```

## 📝 Example Output

```
============================================================
HONEYPOT ATTACK SIMULATOR
============================================================

SAFETY WARNING:
  This tool simulates attacks against your honeypot system.
  Only use this in a controlled lab environment.
  Do NOT use against systems you don't own.

Proceed with attack simulation? (yes/no): yes

[*] Logging server is healthy
    Status: healthy
    Total logs: 5

[*] Starting attack simulation:
    Total attacks: 50
    Mode: mixed
    Concurrency: 1
    Delay: None

    Progress: 5/50 (10.0%)
    Progress: 10/50 (20.0%)
    ...
    Progress: 50/50 (100.0%)

============================================================
ATTACK SIMULATION SUMMARY
============================================================
Total attacks: 50
Successful: 50
Failed: 0
Duration: 12.34s
Rate: 4.05 attacks/sec

Attack distribution:
  git_push          :   12
  git_clone         :   10
  file_access       :   10
  git_fetch         :    7
  bruteforce        :    5
  ci_job_run        :    3
  cred_access       :    1
  malformed         :    1
  api_abuse         :    1
============================================================

[*] Attack simulation completed successfully!
    Check your dashboard at http://localhost:3000 for visualization
```

## 🔗 Related Files

- `honeypot_attack_simulator.py` - Main simulator script
- `logging_server/logging_server.py` - Receives and processes attacks
- `ml_prediction_system.py` - Scores attacks with ML models
- `db1/` - Frontend dashboard for visualization

## 📚 Next Steps

1. Run a small test: `python honeypot_attack_simulator.py --count 10`
2. Check your dashboard to see the attacks appear
3. Review ML scores in the ML Insights page
4. Experiment with different attack modes and concurrency levels
5. Save results for later analysis

Happy testing! 🎯


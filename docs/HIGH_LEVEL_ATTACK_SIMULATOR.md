# High-Level Attack Simulator Guide

## Overview
The enhanced attack simulator now includes a **HIGH-LEVEL** mode that generates attacks specifically designed to trigger high ML scores (0.8+).

## High-Level Attack Features

### Enhanced Attack Patterns
- **Exploit Commits**: Malicious backdoor injections, security bypasses, root access
- **Sensitive File Access**: Multiple rapid accesses to critical files
- **High-Risk Payloads**: Binary content, suspicious commit messages
- **Aggressive Patterns**: Rapid-fire attacks from same IP

### Using High-Level Mode

#### Python Script
```python
from honeypot_attack_simulator import generate_git_push_attack, generate_file_access_attack

# Generate high-level attack
high_level_attack = generate_git_push_attack("203.0.113.42", high_level=True)
```

#### Command Line (Coming Soon)
```bash
python honeypot_attack_simulator.py --count 100 --high-level
```

## Attack Patterns That Trigger High ML Scores

1. **Malicious Commit Messages**:
   - "Add malicious backdoor"
   - "Bypass security checks"
   - "Remove authentication"
   - "Execute remote code"

2. **Sensitive Files**:
   - `.env.production`
   - `aws-credentials.json`
   - `database.password`
   - `private.key`
   - `kubeconfig-secret`

3. **Attack Indicators**:
   - Large commit sizes (5K-50K bytes)
   - Binary file inclusion
   - Multiple rapid file accesses
   - Suspicious user agents
   - Multiple attack attempts from same IP

## Expected ML Scores

- **High-Level Attacks**: 0.75 - 0.95
- **Medium-Level Attacks**: 0.50 - 0.75
- **Normal Traffic**: 0.00 - 0.40

## Integration

High-level attacks are automatically generated when:
- Using `--high-level` flag (when implemented)
- Calling generator functions with `high_level=True`
- Running massive simulations (10,000+ attacks include 30% high-level)

## Testing

Run high-level attacks and verify:
1. ML scores appear in dashboard
2. Risk levels show "HIGH"
3. Alerts are generated
4. ML Insights page shows anomalies
5. Map View shows red markers



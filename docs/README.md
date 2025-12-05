# 🍯 HoneyTrace - Multi-Layer Honeypot Infrastructure

**A Comprehensive Honeypot System with Real-Time ML-Powered Intrusion Detection**

HoneyTrace is an advanced multi-zone honeypot system designed to detect, log, enrich, and analyze attacker behavior in real-time. It features a fake Git server, CI/CD runner traps, intelligent logging backend with GeoIP enrichment, **ML ensemble-based anomaly detection** (Random Forest + Isolation Forest), and a modern React-based FSOCIETY dashboard for comprehensive visualization.

---

## 🎯 Key Features

### 🛡️ Honeypot Services
- **Fake Git Repository** (Port 8001): Simulates Git operations and serves fake sensitive files
- **Fake CI/CD Runner** (Port 8002): Mimics CI/CD pipelines with fake credentials
- **Unified Honeypot** (Port 8000): Combined service for all honeypot operations

### 🤖 Machine Learning Intrusion Detection
- **Random Forest Model**: 95.35% accuracy (Supervised learning for known attacks)
- **Isolation Forest Model**: 61.51% accuracy (Unsupervised learning for unknown anomalies)
- **Ensemble System**: Weighted combination (70% RF + 30% IF) for optimal detection
- **Real-time Scoring**: Automatic ML prediction for every log entry
- **Attack Classification**: Predicts attack types (Exploit, Backdoor, Data Exfiltration, etc.)

### 📡 Logging & Analytics
- **Centralized Logging Server** (Port 5000): Receives and processes all honeypot logs
- **GeoIP Enrichment**: Automatic geographic and ISP information
- **SQLite Database**: Efficient storage with ML predictions
- **RESTful API**: Complete API for data retrieval and analysis

### 🎨 Frontend Dashboard
- **React-based UI**: Modern, responsive dashboard (Kibana-inspired design)
- **Real-time Updates**: Live event streaming
- **7 Comprehensive Pages**:
  - 📊 Dashboard: Overview KPIs and charts
  - ⚡ Live Events: Real-time event stream with ML scores
  - 📈 Analytics: Statistical analysis and trends
  - 🌍 Map View: Geographic attack visualization
  - 🧠 ML Insights: Machine learning performance metrics
  - 🚨 Alerts: Alert management with filtering
  - 🔍 Investigation: Deep-dive IP investigation tool

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    HoneyTrace System                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Honeypot   │    │   Logging    │    │     ML       │ │
│  │   Services   │───►│   Server     │───►│  Ensemble    │ │
│  │  (Ports      │    │  (Port 5000) │    │  Predictor   │ │
│  │  8000-8002)  │    │              │    │              │ │
│  └──────────────┘    └──────┬───────┘    │  • RF (95%)  │ │
│                             │            │  • IF (61%)  │ │
│                             │            │  • Ensemble  │ │
│                             ▼            └──────────────┘ │
│                      ┌──────────────┐                     │
│                      │   Database   │                     │
│                      │  (SQLite)    │                     │
│                      │  + ML Scores │                     │
│                      └──────┬───────┘                     │
│                             │                             │
│                             ▼                             │
│                      ┌──────────────┐                     │
│                      │   Frontend   │                     │
│                      │   Dashboard  │                     │
│                      │  (React)     │                     │
│                      └──────────────┘                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### ⚡ Fastest Way to Start (Windows)

**Double-click:** `start_all.bat`

This opens all services in separate windows automatically!

---

### 📋 Step-by-Step Start

#### Prerequisites Check
```bash
python --version    # Should be 3.8+
node --version      # Should be 14+
npm --version       # Should be 6+
```

#### First-Time Installation

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r logging_server/requirements.txt
   pip install -r ml_requirements.txt
   ```

2. **Install Frontend dependencies**
   ```bash
   cd db1
   npm install
   cd ..
   ```

3. **Train ML Models** (if not already trained)
   ```bash
   python ml_training_system.py
   python ml_isolation_forest_training.py
   ```

#### Starting the System (3 Terminals)

**Terminal 1 - Logging Server:**
```bash
cd logging_server
python logging_server.py
```
✅ Server at: `http://localhost:5000`

**Terminal 2 - Honeypot Services:**
```bash
python start_unified_honeypot.py
```
✅ Services at: `http://localhost:8000-8002`

**Terminal 3 - Frontend Dashboard:**
```bash
cd db1
npm start
```
✅ Dashboard at: `http://localhost:3000`

---

### 📖 Detailed Documentation

- **START_PROJECT.md** - Complete startup guide with troubleshooting
- **QUICK_START.md** - Quick reference guide

---

### ✅ Verify It's Working

1. Open: http://localhost:5000/health → Should show `{"status": "healthy"}`
2. Open: http://localhost:3000 → Should show the dashboard
3. Check Terminal 1 for: `✅ ML models loaded successfully!`

---

## 🎯 Testing Your Honeypot

### Attack Simulator

Test your honeypot system with realistic attack scenarios using the built-in attack simulator:

```bash
# Quick test with 10 mixed attacks
python honeypot_attack_simulator.py --count 10

# Simulate 100 attacks with realistic delays
python honeypot_attack_simulator.py --count 100 --delay 2.0

# High-speed burst test for dashboard demo
python honeypot_attack_simulator.py --count 200 --concurrency 20
```

**Supported Attack Scenarios:**
- 🔥 Git Repository Attacks (push, clone, fetch)
- 📂 Sensitive File Access (`.env`, `secrets.yml`, etc.)
- 🛠 CI/CD Runner Attacks (job execution, API abuse)
- 🔐 Credentials Access Attempts
- 💥 Brute-Force Login Attempts
- 🚨 Malformed Payloads (large payloads, SQL injection, XSS)
- 🔍 Port/Endpoint Scanning

**Features:**
- ✅ Realistic attack patterns with random IPs
- ✅ Automatic ML scoring for each attack
- ✅ Real-time dashboard visualization
- ✅ CSV export for analysis
- ✅ Configurable concurrency and delays

See **ATTACK_SIMULATOR_GUIDE.md** for detailed usage and examples.

---

## 📊 ML Models

### Dataset
- **UNSW-NB15**: Network intrusion detection dataset
- **Training Set**: 175,341 rows
- **Testing Set**: 82,332 rows
- **Total**: 257,673 samples with 45 features

### Models

#### Random Forest (Supervised)
- **Accuracy**: 95.35%
- **Type**: Supervised classification
- **Purpose**: Detect known attack patterns
- **Best for**: Classifying known attack types

#### Isolation Forest (Unsupervised)
- **Accuracy**: 61.51%
- **Type**: Unsupervised anomaly detection
- **Purpose**: Detect unknown/zero-day attacks
- **Best for**: Catching novel attack patterns

#### Ensemble System
- **Combination**: Weighted average (70% RF + 30% IF)
- **Outputs**:
  - `ml_score`: Combined score (0.0 - 1.0)
  - `ml_risk_level`: MINIMAL, LOW, MEDIUM, HIGH
  - `is_anomaly`: Binary flag (0 or 1)
  - `predicted_attack_type`: Attack classification

---

## 🔧 Configuration

### ML Ensemble Weights
Edit `ml_prediction_system.py`:
```python
rf_weight = 0.70   # Random Forest weight
if_weight = 0.30   # Isolation Forest weight
```

### Risk Level Thresholds
```python
HIGH:     score >= 0.8
MEDIUM:   score >= 0.6
LOW:      score >= 0.4
MINIMAL:  score < 0.4
```

### Database Schema
The `logs` table stores:
- All honeypot log data
- GeoIP enrichment data
- ML predictions (`ml_score`, `ml_risk_level`, `is_anomaly`)

---

## 📁 Project Structure

```
HONEYPOT/
├── 📊 ML System
│   ├── ml_training_system.py              # RF training
│   ├── ml_isolation_forest_training.py    # IF training
│   ├── ml_prediction_system.py            # Ensemble predictor
│   └── ml_models/                         # Trained models
│
├── 🍯 Honeypot Services
│   ├── fake_git_repo.py
│   ├── fake_cicd_runner.py
│   └── start_unified_honeypot.py
│
├── 📡 Logging Server
│   └── logging_server/
│       └── logging_server.py              # Enhanced with ML
│
├── 🎨 Frontend
│   └── db1/                               # React dashboard
│
├── 📊 Dataset
│   └── csv/CSV Files/
│
├── 🎯 Testing Tools
    └── honeypot_attack_simulator.py       # Attack simulator script
│
└── 📝 Documentation
    ├── README.md                          # This file
    ├── ATTACK_SIMULATOR_GUIDE.md          # Attack simulator guide
    ├── PROJECT_COMPLETION_SUMMARY.md      # Completion status
    ├── PROJECT_ORGANIZATION.md            # Project structure
    └── ML_MODELS_INTEGRATION_SUMMARY.md   # ML details
```

---

## 📚 Documentation

- **[ATTACK_SIMULATOR_GUIDE.md](ATTACK_SIMULATOR_GUIDE.md)**: Comprehensive attack simulator guide
- **[PROJECT_COMPLETION_SUMMARY.md](PROJECT_COMPLETION_SUMMARY.md)**: Complete status of all features
- **[ML_MODELS_INTEGRATION_SUMMARY.md](ML_MODELS_INTEGRATION_SUMMARY.md)**: Detailed ML model information
- **[DATASET_SUMMARY.md](DATASET_SUMMARY.md)**: Dataset details and statistics
- **[PROJECT_ORGANIZATION.md](PROJECT_ORGANIZATION.md)**: Project structure guide
- **[CLEANUP_SCRIPT.md](CLEANUP_SCRIPT.md)**: Cleanup instructions

---

## 🧪 Testing

### Attack Simulator (Recommended)

The easiest way to test your honeypot system:

```bash
# Quick test with 10 mixed attacks
python honeypot_attack_simulator.py --count 10

# Realistic simulation (100 attacks with 2s delay)
python honeypot_attack_simulator.py --count 100 --delay 2.0

# High-speed burst test for dashboard demo
python honeypot_attack_simulator.py --count 200 --concurrency 20
```

See **[ATTACK_SIMULATOR_GUIDE.md](ATTACK_SIMULATOR_GUIDE.md)** for complete usage guide.

### Manual Testing

```bash
# Send test logs
cd logging_server
python send_test_log.py

# Test ML prediction
python ml_prediction_system.py

# Test integration
python test_integration.py
```

---

## 🎓 Features in Detail

### Real-time ML Scoring
Every log entry is automatically scored using the ML ensemble:
- Immediate prediction on log ingestion
- No separate processing step required
- Scores stored directly in database

### Frontend Integration
All dashboard pages show ML insights:
- **Dashboard**: ML score KPIs
- **Live Events**: Real-time ML scores
- **ML Insights**: Dedicated ML analytics page
- **Alerts**: Filtered by ML risk level
- **Investigation**: Per-IP ML analysis

### Attack Detection
The system detects various attack types:
- Exploits (Git-based attacks)
- Backdoors (Credential access)
- Data Exfiltration (Sensitive file access)
- Reconnaissance (Information gathering)
- Unknown Anomalies (Zero-day attacks)

---

## 🛠️ Development

### Adding New Models
1. Train model using training scripts
2. Save model files in `ml_models/`
3. Update `ml_prediction_system.py` to load new model
4. Add to ensemble logic

### Extending Frontend
1. Create new page in `db1/src/pages/`
2. Add route in `db1/src/App.js`
3. Create API endpoint in `logging_server/logging_server.py`
4. Add to navigation menu

---

## 📈 Performance

- **ML Prediction Latency**: ~50-100ms per log
- **Database Storage**: Real-time insertion
- **Frontend Updates**: 30-second refresh (configurable)
- **Concurrent Requests**: Supports multiple honeypot services

---

## 🔒 Security Notes

- This is a **honeypot system** - it's designed to attract attackers
- Run in isolated network environments
- Monitor all traffic and logs
- Use ML predictions as alerts, not absolute truth
- Review false positives regularly

---

## 📄 License

[Add your license here]

---

## 👥 Contributors

[Add contributors here]

---

## 🙏 Acknowledgments

- UNSW-NB15 dataset for network intrusion detection
- scikit-learn for ML models
- React and Chart.js for frontend visualization
- Flask for backend services

---

## 📞 Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Status**: ✅ Production Ready

All core features implemented and tested. The system is ready for deployment and use!

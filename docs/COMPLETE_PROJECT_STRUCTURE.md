# 🏗️ Complete Project Structure & File Information

## 📁 Project Overview

**Project Name**: Multi-Layer Honeypot Infrastructure with Real-Time ML & External Threat Intelligence Fusion

**Type**: Full-stack security monitoring system with ML-powered threat detection

**Technology Stack**:
- **Backend**: Python (Flask), SQLite
- **Frontend**: React.js, Chart.js
- **ML**: scikit-learn, pandas, numpy
- **Deployment**: Windows Batch Scripts

---

## 📂 Root Directory Structure

```
HONEYPOT/
├── 📁 scripts/              # Core Python scripts
├── 📁 logging_server/       # Backend Flask server
├── 📁 db1/                  # React frontend dashboard
├── 📁 data/                 # Database & ML models
├── 📁 docs/                 # Documentation
├── 📁 csv/                  # Training datasets
├── 📁 assets/               # Static assets
├── 📁 config/              # Configuration files
├── 📁 Honeypot/            # Legacy honeypot services
├── 📁 swanandi/            # Additional scripts
├── 🐍 attack_simulator.py  # Main attack simulator
├── 🐍 attack_simulator.bat # Attack simulator launcher
└── 🪟 start_all.bat        # Main startup script
```

---

## 🔧 Core Files (Root Directory)

### `start_all.bat` ⭐ **MAIN STARTUP SCRIPT**
- **Purpose**: Starts all services in one command
- **What it does**:
  - Checks Python and Node.js installation
  - Starts Logging Server (port 5000)
  - Starts Fake Git Repository (port 8001)
  - Starts Fake CI/CD Runner (port 8002)
  - Starts Unified Honeypot (port 8000)
  - Starts Frontend Dashboard (port 3000)
  - Opens browser automatically
- **Usage**: Double-click or run from command line
- **Location**: Root directory (outside folders)

### `attack_simulator.py` ⭐ **DYNAMIC ATTACK GENERATOR**
- **Purpose**: Generates realistic attack traffic to test the system
- **What it does**:
  - Generates 7 types of malicious attacks (git_push, file_access, ci_job_run, etc.)
  - Uses single IP (203.0.113.42) for realism
  - Sends attacks to logging server
  - Includes network features for ML models
  - **NO NORMAL TRAFFIC** - all attacks are malicious
- **Features**:
  - Configurable attack count
  - Multiple attack modes (mixed, malicious_only)
  - Concurrent execution support
  - Real-time statistics
- **Usage**: `python attack_simulator.py --count 100 --mode malicious_only`
- **Location**: Root directory

### `attack_simulator.bat`
- **Purpose**: Windows launcher for attack simulator
- **What it does**: Provides interactive menu to run attack simulator
- **Usage**: Double-click to run

---

## 📁 scripts/ - Core Python Scripts

### **Honeypot Services**

#### `fake_git_repo.py`
- **Purpose**: Fake Git Repository honeypot service
- **Port**: 8001
- **What it does**:
  - Simulates a Git repository
  - Catches git push attempts
  - Logs file access attempts
  - Sends logs to logging server
- **Attack Types Detected**: Git exploits, unauthorized commits, file exfiltration

#### `fake_cicd_runner.py`
- **Purpose**: Fake CI/CD Runner honeypot service
- **Port**: 8002
- **What it does**:
  - Simulates CI/CD pipeline runner
  - Catches malicious job submissions
  - Logs credential access attempts
  - Sends logs to logging server
- **Attack Types Detected**: CI/CD exploits, credential theft, backdoor installation

#### `start_unified_honeypot.py`
- **Purpose**: Unified/Consolidated honeypot service
- **Port**: 8000
- **What it does**:
  - Combines multiple honeypot services
  - Handles various attack types
  - Sends logs to logging server
- **Attack Types Detected**: Scanning, brute force, malformed payloads

### **Machine Learning Scripts**

#### `ml_prediction_system.py` ⭐ **CORE ML SYSTEM**
- **Purpose**: Main ML prediction engine
- **What it does**:
  - Loads 3 ML models (Random Forest, Isolation Forest, CIC-DarkNet)
  - Preprocesses honeypot log data
  - Performs ensemble prediction
  - Generates ML scores (0.0-1.0)
  - Determines risk levels (MINIMAL, LOW, MEDIUM, HIGH)
  - Classifies attack types
- **Key Features**:
  - Ensemble weighting: RF (60%), IF (25%), DarkNet (15%)
  - Malicious indicator detection
  - Score boosting for attacks
  - Returns: `ml_score`, `ml_risk_level`, `is_anomaly`, `predicted_attack_type`
- **Used by**: `logging_server.py` for real-time predictions

#### `ml_training_system.py`
- **Purpose**: Trains Random Forest model on UNSW-NB15 dataset
- **What it does**:
  - Loads training data
  - Feature engineering and selection
  - Trains Random Forest classifier
  - Saves model to `data/ml_models/`
- **Accuracy**: 95.35%
- **Output**: `randomforest_model.pkl`, `best_model_info.json`

#### `ml_isolation_forest_training.py`
- **Purpose**: Trains Isolation Forest model on UNSW-NB15 dataset
- **What it does**:
  - Loads training data
  - Trains Isolation Forest for anomaly detection
  - Hyperparameter tuning
  - Saves model to `data/ml_models/`
- **Accuracy**: 56.93%
- **Output**: `isolationforest_model.pkl`, `isolationforest_model_info.json`

#### `ml_isolation_forest_normal_only_training.py`
- **Purpose**: Trains Isolation Forest ONLY on normal traffic
- **What it does**:
  - Filters dataset for normal traffic (label=0)
  - Trains on normal-only data
  - Better anomaly detection for unknown attacks
- **Output**: `isolationforest_normal_only_model.pkl`

#### `ml_isolation_forest_inference.py`
- **Purpose**: Performs inference using Isolation Forest model
- **What it does**:
  - Loads trained model
  - Preprocesses new data
  - Predicts anomalies
  - Calculates anomaly ratio
- **Usage**: Testing and evaluation

#### `evaluate_isolation_forest_accuracy.py`
- **Purpose**: Evaluates Isolation Forest model accuracy
- **What it does**:
  - Loads test dataset
  - Makes predictions
  - Calculates metrics (accuracy, precision, recall, F1-score)
  - Generates confusion matrix

### **Utility Scripts**

#### `ml_honeypot_integration.py`
- **Purpose**: Integration testing for ML system
- **What it does**: Tests ML prediction with honeypot logs

#### `test_client.py`
- **Purpose**: Test client for logging server
- **What it does**: Sends test logs to verify server functionality

#### `test_integration.py`
- **Purpose**: Integration tests
- **What it does**: Tests end-to-end functionality

#### `start_all.py`
- **Purpose**: Python version of start_all.bat
- **What it does**: Starts all services programmatically

#### `honeypot_attack_simulator.py`
- **Purpose**: Alternative attack simulator
- **What it does**: Generates attack traffic

#### `high_risk_attack_blast.py`
- **Purpose**: Generates high-risk attacks
- **What it does**: Creates attacks with high ML scores

#### `run_massive_attack_simulation.py`
- **Purpose**: Large-scale attack simulation
- **What it does**: Runs thousands of attacks for testing

### **Batch Scripts** (`scripts/batch/`)

#### `start_all.bat`
- **Purpose**: Starts all backend services
- **What it does**: Launches logging server and honeypot services

#### `start_backend.bat`
- **Purpose**: Starts only backend services
- **What it does**: Launches logging server

#### `run_10000_attacks.bat`
- **Purpose**: Runs 10,000 attacks
- **What it does**: Executes attack simulator with 10k count

#### `run_20000_attacks.bat`
- **Purpose**: Runs 20,000 attacks
- **What it does**: Executes attack simulator with 20k count

---

## 📁 logging_server/ - Backend Flask Server

### `logging_server.py` ⭐ **MAIN BACKEND SERVER**
- **Purpose**: Central logging and API server
- **Port**: 5000
- **What it does**:
  - Receives logs from honeypot services
  - Performs GeoIP enrichment
  - Runs ML predictions on each log
  - Stores data in SQLite database
  - Provides REST API for frontend
- **Key Endpoints**:
  - `POST /log` - Receive honeypot logs
  - `GET /api/live-events` - Get recent events
  - `GET /api/analytics` - Get analytics data
  - `GET /api/ml-insights` - Get ML insights
  - `GET /api/alerts` - Get security alerts
  - `GET /api/investigate/<ip>` - Investigate specific IP
  - `GET /stats` - Get statistics
  - `GET /health` - Health check
- **Database**: SQLite (`data/honeypot.db`)
- **ML Integration**: Uses `ml_prediction_system.py` for real-time scoring

### `start_logging_server.py`
- **Purpose**: Launcher for logging server
- **What it does**: Starts Flask server with proper configuration

### `send_test_log.py`
- **Purpose**: Test script
- **What it does**: Sends test log to server

### `log.py`
- **Purpose**: Logging utilities
- **What it does**: Helper functions for logging

### `requirements.txt`
- **Purpose**: Python dependencies
- **Dependencies**: Flask, flask-cors, requests, pandas, numpy, scikit-learn, joblib, etc.

### `README.md`
- **Purpose**: Documentation for logging server

---

## 📁 db1/ - React Frontend Dashboard

### **Main Application Files**

#### `src/App.js` ⭐ **MAIN REACT APP**
- **Purpose**: Root React component
- **What it does**:
  - Sets up routing
  - Manages global state
  - Provides navigation
- **Routes**:
  - `/` - Dashboard
  - `/live-events` - Live Events
  - `/analytics` - Analytics
  - `/ml-insights` - ML Insights
  - `/alerts` - Security Alerts
  - `/investigate/:ip` - IP Investigation
  - `/map` - Map View

#### `src/api.js` ⭐ **API CLIENT**
- **Purpose**: Frontend API client
- **What it does**:
  - Handles all API calls to backend
  - Error handling
  - Connection checking
- **Methods**:
  - `getLiveEvents()` - Fetch live events
  - `getAnalytics()` - Fetch analytics
  - `getMLInsights()` - Fetch ML insights
  - `getAlerts()` - Fetch alerts
  - `investigateIP()` - Investigate IP
  - `getStats()` - Fetch statistics
  - `checkHealth()` - Check backend health

#### `src/index.js`
- **Purpose**: React entry point
- **What it does**: Renders App component

#### `src/index.css`
- **Purpose**: Global styles

#### `src/App.css`
- **Purpose**: App component styles

### **Pages** (`src/pages/`)

#### `Dashboard.js` ⭐ **MAIN DASHBOARD**
- **Purpose**: Main dashboard page
- **What it displays**:
  - Total attacks, unique IPs, recent activity
  - Average ML score, high-risk attacks, anomalies
  - Charts: Attacks by Service, Attack Actions, Attacks by Country
  - ML Score Trend (24h) - Time-based line chart
  - Risk Level Distribution
- **Refresh Rate**: Every 5 seconds
- **Data Source**: `/stats` endpoint

#### `LiveEvents.js` ⭐ **LIVE EVENTS PAGE**
- **Purpose**: Real-time event monitoring
- **What it displays**:
  - Table of recent events
  - IP, country, protocol, service, action
  - ML scores and risk levels
  - Real-time updates
- **Refresh Rate**: Every 5 seconds
- **Data Source**: `/api/live-events` endpoint
- **Features**: Filter by IP, filter by min ML score

#### `Analytics.js` ⭐ **ANALYTICS PAGE**
- **Purpose**: Attack analytics and statistics
- **What it displays**:
  - Total attacks, high-risk attacks, unique IPs, avg ML score
  - Attacks Over Time (24h) - Time-based line chart
  - Top Countries (bar chart)
  - Top IPs (bar chart)
  - Top Protocols (doughnut chart)
- **Refresh Rate**: Every 5 seconds
- **Data Source**: `/api/analytics` endpoint

#### `MLInsights.js` ⭐ **ML INSIGHTS PAGE**
- **Purpose**: Machine learning insights and analysis
- **What it displays**:
  - Average anomaly score, total anomalies, high-score IPs
  - Anomaly Score Trend (24h) - Time-based line chart
  - High-Score IPs (bar chart)
  - Risk Level Distribution (doughnut chart)
  - CIC-DarkNet Traffic Type Distribution
  - ML Model Ensemble information
- **Refresh Rate**: Every 5 seconds
- **Data Source**: `/api/ml-insights` endpoint

#### `Alerts.js` ⭐ **ALERTS PAGE**
- **Purpose**: Security alerts and threat detection
- **What it displays**:
  - Total alerts, critical, high, medium, low risk counts
  - Risk Level Distribution (doughnut chart)
  - Alerts Overview (bar chart)
  - List of alerts with full security details
  - Expandable alert cards with investigation link
- **Refresh Rate**: Every 5 seconds
- **Data Source**: `/api/alerts` endpoint
- **Features**:
  - Threshold filtering
  - Risk level filtering
  - Country/service filtering
  - Sort by score or time
  - Export to CSV
  - Full security details on expand

#### `Investigation.js` ⭐ **INVESTIGATION PAGE**
- **Purpose**: Deep dive investigation for specific IPs
- **What it displays**:
  - IP information (location, ISP, coordinates)
  - Statistics (total attacks, avg/max scores, unique actions/services)
  - ML Score Trend Over Time (24h) - Time-based line chart
  - Service Distribution (doughnut chart)
  - Action Distribution (bar chart)
  - Risk Level Distribution (doughnut chart)
  - Timeline view of all attacks
  - Detailed logs view
- **Data Source**: `/api/investigate/<ip>` endpoint
- **Features**: Three view modes (Overview, Timeline, Details)

#### `MapView.js`
- **Purpose**: Geographic visualization
- **What it displays**:
  - World map with attack locations
  - Attack markers by country
  - Color-coded by risk level
- **Data Source**: `/api/map-data` endpoint

### **Components** (`src/components/`)

#### `ConnectionStatus.js`
- **Purpose**: Connection status indicator
- **What it does**: Shows backend connection status

### **Styles**

#### `Pages.css`
- **Purpose**: Shared styles for all pages
- **What it contains**: Common page styles, chart containers, stat cards

#### `Alerts.css`
- **Purpose**: Alerts page specific styles

#### `InvestigationPage.css`
- **Purpose**: Investigation page specific styles

### **Configuration**

#### `package.json`
- **Purpose**: Node.js dependencies
- **Dependencies**: React, react-router-dom, chart.js, react-chartjs-2, react-toastify, etc.

#### `public/index.html`
- **Purpose**: HTML template
- **What it does**: Root HTML file for React app

---

## 📁 data/ - Data Storage

### `honeypot.db` ⭐ **SQLITE DATABASE**
- **Purpose**: Main database storing all logs
- **Table**: `logs`
- **Schema**:
  - `id` - Primary key
  - `timestamp` - Event timestamp
  - `source_ip` - Attacker IP
  - `geo_country`, `geo_city`, `geo_region` - GeoIP data
  - `geo_latitude`, `geo_longitude` - Coordinates
  - `geo_isp`, `geo_org` - ISP information
  - `protocol` - Network protocol
  - `target_service` - Honeypot service
  - `action` - Attack action type
  - `target_file` - Target file (if any)
  - `headers` - HTTP headers (JSON)
  - `payload` - Request payload (JSON)
  - `session_id` - Session identifier
  - `user_agent` - User agent string
  - `ml_score` - ML ensemble score (0.0-1.0)
  - `ml_risk_level` - Risk level (MINIMAL, LOW, MEDIUM, HIGH)
  - `is_anomaly` - Anomaly flag (0 or 1)
  - `predicted_attack_type` - Attack classification
  - `darknet_traffic_type` - CIC-DarkNet traffic type
  - `log_hash` - Integrity hash
  - `created_at` - Database insertion timestamp

### `ml_models/` ⭐ **ML MODEL STORAGE**
- **Purpose**: Stores trained ML models and preprocessing objects
- **Key Files**:
  - `randomforest_model.pkl` - Random Forest model (95.35% accuracy)
  - `isolationforest_model.pkl` - Isolation Forest model (56.93% accuracy)
  - `isolationforest_normal_only_model.pkl` - Normal-only IF model
  - `darknet_model.pkl` - CIC-DarkNet model (95% accuracy)
  - `best_model_info.json` - RF model metadata
  - `isolationforest_model_info.json` - IF model metadata
  - `darknet_model_info.json` - DarkNet model metadata
  - `feature_columns.json` - Feature column names
  - `standard_scaler.pkl` - RF scaler
  - `isolationforest_scaler.pkl` - IF scaler
  - `*_encoder.pkl` - Label encoders (proto, service, state)
  - `feature_selector.pkl` - Feature selectors

### `ml_results/` - ML Training Results
- **Purpose**: Stores ML training results and statistics
- **Files**:
  - `dataset_stats.json` - Dataset statistics
  - `isolation_forest_stats.json` - IF training stats
  - `isolationforest_normal_only_stats.json` - Normal-only IF stats
  - `feature_importance.csv` - Feature importance rankings
  - `training_report.md` - Training reports

---

## 📁 docs/ - Documentation

### **Main Documentation**

#### `README.md`
- **Purpose**: Main project documentation
- **What it contains**: Project overview, setup instructions

#### `PROJECT_STRUCTURE.md`
- **Purpose**: Project structure documentation

#### `QUICK_START.md`
- **Purpose**: Quick start guide

#### `HOW_TO_START.txt`
- **Purpose**: Step-by-step startup instructions

### **Technical Documentation**

#### `HONEYPOT_ARCHITECTURE_EXPLAINED.md`
- **Purpose**: Architecture explanation
- **What it contains**: How the honeypot system works

#### `HOW_ATTACKS_WORK.md`
- **Purpose**: Attack flow explanation
- **What it contains**: How attacks are detected and processed

#### `ML_MODELS_INTEGRATION_SUMMARY.md`
- **Purpose**: ML integration documentation
- **What it contains**: ML model details and integration

#### `GRAPHS_TIME_FIXES.md`
- **Purpose**: Time-based graph fixes documentation
- **What it contains**: All time-based chart implementations

#### `FRONTEND_ML_ENHANCEMENTS.md`
- **Purpose**: Frontend ML features documentation

#### `ATTACK_SIMULATOR_GUIDE.md`
- **Purpose**: Attack simulator usage guide

### **Project Reports**

#### `PROJECT_REPORT.md`
- **Purpose**: Complete project report

#### `PROJECT_COMPLETION_SUMMARY.md`
- **Purpose**: Project completion status

#### `COMPLETE_FIX_SUMMARY.md`
- **Purpose**: Fix summary documentation

---

## 📁 csv/ - Training Datasets

### `CSV Files/`
- **Purpose**: UNSW-NB15 dataset for ML training
- **Files**:
  - `UNSW_NB15_training-set.csv` - Training data
  - `UNSW_NB15_testing-set.csv` - Testing data
  - `NUSW-NB15_features.csv` - Feature descriptions
  - `NUSW-NB15_GT.csv` - Ground truth labels
  - `UNSW-NB15_*.csv` - Dataset partitions
  - `The UNSW-NB15 description.pdf` - Dataset documentation

---

## 📁 assets/ - Static Assets

### `db.png`
- **Purpose**: Dashboard image/logo
- **Usage**: Frontend display

---

## 📁 config/ - Configuration

### `.gitignore`
- **Purpose**: Git ignore rules
- **What it ignores**: `node_modules/`, `*.db`, `*.log`, `venv/`, etc.

---

## 📁 Honeypot/ - Legacy Services

### `honeypot_services.py`
- **Purpose**: Legacy honeypot implementation
- **Status**: May be deprecated in favor of unified services

### `start_honeypot.py`
- **Purpose**: Legacy honeypot launcher

### `static/`
- **Purpose**: Static files for legacy honeypot
- **Files**: `config.json`, `env_file`, `README.md`

---

## 📁 swanandi/ - Additional Scripts

### `attack_ml.py`
- **Purpose**: ML attack testing script

### `attack_traffic_external_1.py`
- **Purpose**: External attack traffic generator

---

## 🔄 Data Flow

### **Attack Flow**:
1. **Attack Simulator** (`attack_simulator.py`) generates attack
2. **Honeypot Services** (`fake_git_repo.py`, `fake_cicd_runner.py`, `start_unified_honeypot.py`) receive attack
3. **Logging Server** (`logging_server.py`) receives log
4. **ML Prediction** (`ml_prediction_system.py`) scores the attack
5. **Database** (`data/honeypot.db`) stores log with ML scores
6. **Frontend** (`db1/src/`) displays data via API calls

### **Frontend Flow**:
1. **React App** (`App.js`) loads
2. **API Client** (`api.js`) calls backend endpoints
3. **Backend** (`logging_server.py`) queries database
4. **Data** returned as JSON
5. **Pages** (`Dashboard.js`, `LiveEvents.js`, etc.) render charts and data
6. **Auto-refresh** every 5 seconds for real-time updates

---

## 🎯 Key Features by Component

### **ML System**
- ✅ 3 ML models (RF, IF, DarkNet)
- ✅ Ensemble prediction
- ✅ Real-time scoring
- ✅ Attack type classification
- ✅ Risk level determination

### **Honeypot Services**
- ✅ Fake Git Repository
- ✅ Fake CI/CD Runner
- ✅ Unified Honeypot
- ✅ Multiple attack type detection

### **Backend API**
- ✅ RESTful API
- ✅ GeoIP enrichment
- ✅ Real-time ML scoring
- ✅ SQLite database
- ✅ Multiple endpoints

### **Frontend Dashboard**
- ✅ 6 main pages
- ✅ Real-time updates (5s refresh)
- ✅ 19+ charts/graphs
- ✅ Dynamic data (no demo data)
- ✅ Time-based charts
- ✅ Full investigation features

### **Attack Simulator**
- ✅ 7 attack types
- ✅ Single IP for realism
- ✅ Network features for ML
- ✅ Configurable parameters
- ✅ Real-time statistics

---

## 🚀 Quick Start

1. **Start All Services**: Run `start_all.bat`
2. **Generate Attacks**: Run `python attack_simulator.py --count 100`
3. **View Dashboard**: Open `http://localhost:3000`

---

## 📊 Statistics

- **Total Python Files**: ~25 core scripts
- **Total React Components**: 9 pages + 1 component
- **Total API Endpoints**: 10+
- **Total Charts/Graphs**: 19+
- **ML Models**: 3 (RF, IF, DarkNet)
- **Honeypot Services**: 3 (Git, CI/CD, Unified)
- **Database Tables**: 1 (logs)
- **Frontend Pages**: 6 main pages

---

## ✅ Project Status

**All Systems Operational**:
- ✅ ML prediction system working
- ✅ All graphs displaying correctly with time
- ✅ Real-time updates functional
- ✅ Attack simulator generating high ML scores
- ✅ Alerts system working
- ✅ Investigation page functional
- ✅ All pages dynamic (no demo data)

---

**Last Updated**: Current session
**Project Version**: 1.0.0
**Status**: Production Ready


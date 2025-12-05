# 📁 Project Organization Guide

## Current Project Structure

```
HONEYPOT/
│
├── 📊 ML System (Complete)
│   ├── ml_training_system.py              # Random Forest training
│   ├── ml_isolation_forest_training.py    # Isolation Forest training
│   ├── ml_prediction_system.py            # ⭐ Enhanced: RF + IF Ensemble
│   ├── ml_honeypot_integration.py         # Real-time ML monitoring
│   ├── ml_requirements.txt                # ML dependencies
│   │
│   ├── ml_models/                         # Trained models
│   │   ├── randomforest_model.pkl         # ✅ RF Model (95.35% accuracy)
│   │   ├── isolationforest_model.pkl      # ✅ IF Model (61.51% accuracy)
│   │   ├── best_model_info.json           # RF metadata
│   │   ├── isolationforest_model_info.json # IF metadata
│   │   ├── feature_columns.json           # Feature list
│   │   └── [encoders, scalers, selectors] # Preprocessing objects
│   │
│   ├── ml_results/                        # Training results
│   │   ├── dataset_stats.json
│   │   ├── isolation_forest_stats.json
│   │   └── training_report.md
│   │
│   └── ml_plots/                          # Visualizations
│       └── [confusion matrices, ROC curves]
│
├── 🔐 Honeypot Services
│   ├── fake_git_repo.py                   # Fake Git server (Port 8001)
│   ├── fake_cicd_runner.py                # Fake CI/CD (Port 8002)
│   ├── start_unified_honeypot.py          # Unified honeypot (Port 8000)
│   │
│   └── Honeypot/                          # Alternative structure
│       ├── honeypot_services.py
│       ├── start_honeypot.py
│       └── static/                        # Fake files
│
├── 📡 Logging Server (Enhanced with ML)
│   ├── logging_server/
│   │   ├── logging_server.py              # ⭐ Enhanced: Auto ML scoring
│   │   ├── send_test_log.py               # Test log generator
│   │   ├── start_logging_server.py        # Server starter
│   │   └── requirements.txt
│   │
│   └── honeypot.db                        # SQLite database
│
├── 🎨 Frontend Dashboard
│   └── db1/                               # React application
│       ├── src/
│       │   ├── App.js                     # Main app with routes
│       │   ├── api.js                     # API service
│       │   ├── components/
│       │   │   └── ConnectionStatus.js
│       │   └── pages/
│       │       ├── Dashboard.js           # 📊 Overview
│       │       ├── LiveEvents.js          # ⚡ Real-time events
│       │       ├── Analytics.js           # 📈 Analytics
│       │       ├── MapView.js             # 🌍 Geographic map
│       │       ├── MLInsights.js          # 🧠 ML insights
│       │       ├── Alerts.js              # 🚨 Alerts
│       │       └── Investigation.js       # 🔍 IP investigation
│       └── package.json
│
├── 📊 Dataset
│   └── csv/
│       └── CSV Files/
│           ├── Training and Testing Sets/
│           │   ├── UNSW_NB15_training-set.csv  # 175,341 rows
│           │   └── UNSW_NB15_testing-set.csv   # 82,332 rows
│           └── [Other UNSW-NB15 files]
│
└── 📝 Documentation
    ├── README.md                          # Main readme
    ├── PROJECT_ORGANIZATION.md            # This file
    ├── ML_MODELS_INTEGRATION_SUMMARY.md   # ML models overview
    ├── DATASET_SUMMARY.md                 # Dataset details
    └── [Other docs...]
```

## 🎯 Key Features Implemented

### ✅ ML Ensemble System
- **Random Forest**: 95.35% accuracy (Supervised)
- **Isolation Forest**: 61.51% accuracy (Unsupervised)
- **Ensemble Logic**: Weighted combination (70% RF + 30% IF)
- **Auto-scoring**: Logs automatically scored on ingestion

### ✅ Logging Server Enhancements
- Automatic ML scoring for every log entry
- Stores: `ml_score`, `ml_risk_level`, `is_anomaly`
- Real-time prediction using ensemble

### ✅ Database Schema
```sql
logs (
    id, timestamp, source_ip,
    geo_country, geo_city, geo_region, geo_latitude, geo_longitude,
    protocol, target_service, action, target_file,
    ml_score REAL,              -- Ensemble score (0-1)
    ml_risk_level TEXT,         -- MINIMAL, LOW, MEDIUM, HIGH
    is_anomaly INTEGER,         -- 0 or 1
    created_at
)
```

## 🗑️ Files to Clean Up

### Duplicate/Unnecessary Files:
- ❌ `ml_models/ml_models/` - Nested duplicate directory
- ❌ `ml_models/ml_models/trian.py` - Typo file (old version)
- ❌ `ml_models/3687527.zip.fdmdownload` - Download artifact (deleted)
- ❌ `ml_models/Honeypot data.zip` - Unnecessary zip (deleted)
- ❌ `ml_models/model.pkl` - Old/duplicate model (if exists)
- ❌ `ml_models/model_info.json` - Old metadata (if exists)

### Files to Keep:
- ✅ All `.pkl` files in `ml_models/` (except duplicates)
- ✅ All `*_model_info.json` files
- ✅ All training and results files

## 📋 Frontend Pages Organization

### Tab Structure:
1. **Dashboard** (`/`) - Overview KPIs and charts
2. **Live Events** (`/live-events`) - Real-time event stream
3. **Analytics** (`/analytics`) - Statistical analysis
4. **Map View** (`/map`) - Geographic visualization
5. **ML Insights** (`/ml-insights`) - ML model performance
6. **Alerts** (`/alerts`) - Alert management
7. **Investigation** (`/investigate`) - IP investigation tool

## 🔧 Maintenance Tasks

### Regular Cleanup:
1. Remove duplicate model files
2. Archive old training logs
3. Clean up test databases
4. Remove unused dependencies

### Future Enhancements:
1. Add predicted_attack_type column to database
2. Create model versioning system
3. Add ensemble weight configuration
4. Implement model retraining pipeline

## 📦 Dependencies

### Backend:
- Flask + Flask-CORS
- scikit-learn
- pandas, numpy
- joblib (model serialization)
- requests (GeoIP, webhooks)

### Frontend:
- React
- React Router
- Chart.js / react-chartjs-2
- React Toastify
- Axios / Fetch API

## 🚀 Quick Start

1. **Train Models** (if needed):
   ```bash
   python ml_training_system.py
   python ml_isolation_forest_training.py
   ```

2. **Start Logging Server**:
   ```bash
   cd logging_server
   python logging_server.py
   ```

3. **Start Honeypot**:
   ```bash
   python start_unified_honeypot.py
   ```

4. **Start Frontend**:
   ```bash
   cd db1
   npm install
   npm start
   ```

## 📝 Notes

- ML models auto-load when logging server starts
- Ensemble scoring happens automatically for all logs
- Frontend displays ML scores in real-time
- Database stores all ML predictions for analysis


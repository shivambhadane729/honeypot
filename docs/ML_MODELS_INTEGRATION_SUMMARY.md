# 🤖 ML Models Integration Summary

## Overview

Your honeypot project has **TWO main ML models** trained and integrated for attack detection:

---

## 📊 1. **Random Forest (Supervised Learning)**

### Status: ✅ **Trained & Currently Integrated**

### Training Details:
- **File**: `ml_training_system.py`
- **Dataset**: UNSW-NB15 (Training & Testing sets)
- **Accuracy**: **95.35%** 🎯
- **Type**: Supervised Classification
- **Best Model**: Selected from multiple models (Random Forest, Gradient Boosting, Logistic Regression, SVM)

### Model Configuration:
- **Algorithm**: Random Forest Classifier
- **Hyperparameters**:
  - `n_estimators`: 100-200 trees
  - `max_depth`: 10-20 or None
  - `min_samples_split`: 2-5
- **Feature Scaling**: Not required (tree-based model)

### Integration:
- **Prediction System**: `ml_prediction_system.py`
  - Loads the trained Random Forest model
  - Preprocesses honeypot log data
  - Makes real-time attack predictions
  - Calculates attack probability scores

- **Storage Location**:
  - Model: `ml_models/randomforest_model.pkl`
  - Info: `ml_models/best_model_info.json`
  - Preprocessing: `ml_models/standard_scaler.pkl`, encoders, feature selector

---

## 🌲 2. **Isolation Forest (Unsupervised Learning)**

### Status: ✅ **Trained** ⚠️ **NOT YET INTEGRATED INTO PREDICTION SYSTEM**

### Training Details:
- **File**: `ml_isolation_forest_training.py`
- **Dataset**: UNSW-NB15 (Training & Testing sets)
- **Current Accuracy**: **35.94%** (Old) → **61.51%** (After optimization)
- **Type**: Unsupervised Anomaly Detection
- **Purpose**: Detect anomalies/attacks without labeled data

### Model Configuration:
- **Algorithm**: Isolation Forest
- **Hyperparameters** (Optimized):
  - `n_estimators`: 300-1000 (Currently testing 500)
  - `max_samples`: 0.7, 0.8, 0.9, 'auto'
  - `contamination`: Up to 0.5 (Isolation Forest limitation)
  - **Features**: Top 40 features selected using SelectKBest

### Special Features:
- **Threshold Optimization**: For high attack-rate datasets (>50%), uses dynamic threshold optimization
- **Combined Metric**: Optimizes using 45% accuracy + 30% F1 + 15% precision + 10% recall
- **Feature Scaling**: StandardScaler

### Storage Location:
- Model: `ml_models/isolationforest_model.pkl`
- Info: `ml_models/isolationforest_model_info.json`
- Preprocessing: `ml_models/isolationforest_scaler.pkl`, encoders, feature selector

### ⚠️ **Current Status**:
- ✅ Model is trained and saved
- ❌ **NOT integrated into `ml_prediction_system.py`**
- ❌ **NOT being used for real-time predictions**

---

## 🔄 Current Integration Architecture

### How ML Works Now:

```
┌─────────────────┐
│  Honeypot       │
│  Services       │ ──────► Logs sent to
│  (Ports 8000+   │
└─────────────────┘
                    │
                    ▼
          ┌──────────────────────┐
          │  Logging Server      │
          │  (Port 5000)         │
          │  - Receives logs     │
          │  - Adds GeoIP data   │
          │  - Stores in DB      │
          └──────────────────────┘
                    │
                    │  (Separate process)
                    ▼
          ┌──────────────────────┐
          │  ML Integration      │
          │  (ml_honeypot_       │
          │   integration.py)    │
          │  - Fetches logs      │
          │  - Uses Random       │
          │    Forest ONLY       │
          │  - Makes predictions │
          │  - Generates alerts  │
          └──────────────────────┘
```

### What's Happening:

1. **Honeypot Services** → Send logs to Logging Server
2. **Logging Server** → Stores logs in database (with `ml_score`, `ml_risk_level`, `is_anomaly` columns)
3. **ML Integration Service** → Runs separately, fetches logs, uses **Random Forest only**, makes predictions
4. **Database** → Has ML columns but they're populated by the integration service, not during log storage

---

## 📋 Supervised Models Available (Training System)

The `ml_training_system.py` can train multiple models:

1. ✅ **Random Forest** - Best performing (95.35% accuracy)
2. ✅ **Gradient Boosting** - Alternative ensemble method
3. ✅ **Logistic Regression** - Linear classifier
4. ✅ **SVM (Support Vector Machine)** - Kernel-based classifier
5. ❌ **Neural Network** - Removed due to memory issues

Only the **best model** (Random Forest) is saved and used for predictions.

---

## 🎯 Model Comparison

| Model | Type | Accuracy | Status | Use Case |
|-------|------|----------|--------|----------|
| **Random Forest** | Supervised | **95.35%** | ✅ Integrated | Primary attack detection |
| **Isolation Forest** | Unsupervised | **61.51%** | ⚠️ Trained but not integrated | Anomaly detection for unknown attacks |

---

## 🔍 What Each Model Does

### Random Forest (Currently Used):
- ✅ **Supervised learning** - Uses labeled attack data
- ✅ **High accuracy** - 95.35% on UNSW-NB15 dataset
- ✅ **Attack classification** - Binary: Attack (1) or Normal (0)
- ✅ **Probability scores** - Provides confidence scores (0-1)
- ✅ **Real-time predictions** - Fast inference
- ⚠️ **Requires labeled data** - Can't detect truly novel attacks

### Isolation Forest (Trained but Not Used):
- ✅ **Unsupervised learning** - No labels needed during inference
- ✅ **Anomaly detection** - Identifies unusual patterns
- ✅ **Novel attack detection** - Can catch attacks not in training data
- ⚠️ **Lower accuracy** - 61.51% (but improving with optimization)
- ⚠️ **Requires threshold tuning** - For high attack-rate scenarios
- ❌ **Not integrated** - Currently not used for predictions

---

## 📊 Database Schema (ML Columns)

The `logs` table in `honeypot.db` has these ML-related columns:

```sql
ml_score REAL           -- Attack probability (0.0 to 1.0)
ml_risk_level TEXT      -- MINIMAL, LOW, MEDIUM, HIGH
is_anomaly INTEGER      -- 0 = Normal, 1 = Anomaly/Attack
```

**Current State**: These columns exist but are populated by the ML Integration service, not during initial log storage.

---

## 🚀 Integration Status

### ✅ What's Working:
1. Random Forest model trained and saved
2. ML prediction system can load and use Random Forest
3. ML integration service can process logs
4. Database schema supports ML data
5. Frontend displays ML scores and insights

### ⚠️ What's Missing:
1. **Isolation Forest not integrated** into prediction system
2. ML predictions not automatically stored during log ingestion
3. No option to use both models together (ensemble)
4. No API endpoint to manually trigger ML predictions on stored logs

---

## 💡 Recommended Next Steps

1. **Integrate Isolation Forest**:
   - Update `ml_prediction_system.py` to load both models
   - Create ensemble predictions (combine Random Forest + Isolation Forest)
   - Update `ml_honeypot_integration.py` to use both models

2. **Real-time ML Scoring**:
   - Add ML prediction to logging server's `/log` endpoint
   - Store ML scores immediately when logs are received
   - No need for separate integration service

3. **Model Selection**:
   - Allow choosing which model(s) to use
   - Support ensemble mode (average or vote)
   - Different models for different risk scenarios

4. **Update Prediction System**:
   - Support loading Isolation Forest model
   - Handle threshold-based predictions
   - Combine supervised + unsupervised results

---

## 📁 Key Files

### Training:
- `ml_training_system.py` - Trains Random Forest (supervised)
- `ml_isolation_forest_training.py` - Trains Isolation Forest (unsupervised)

### Prediction:
- `ml_prediction_system.py` - Loads models and makes predictions (currently only Random Forest)

### Integration:
- `ml_honeypot_integration.py` - Monitors logs and applies ML (currently only Random Forest)

### Models:
- `ml_models/randomforest_model.pkl` - Trained Random Forest
- `ml_models/isolationforest_model.pkl` - Trained Isolation Forest
- `ml_models/best_model_info.json` - Random Forest metadata
- `ml_models/isolationforest_model_info.json` - Isolation Forest metadata

---

## 🎓 Summary

**You have TWO ML models:**

1. ✅ **Random Forest** - 95.35% accuracy, **CURRENTLY INTEGRATED** and working
2. ✅ **Isolation Forest** - 61.51% accuracy, **TRAINED** but **NOT INTEGRATED**

The Isolation Forest model exists and is trained, but it's not being used in the prediction pipeline. To use it, you would need to integrate it into `ml_prediction_system.py` and `ml_honeypot_integration.py`.


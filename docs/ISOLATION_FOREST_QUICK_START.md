# Isolation Forest Training - Quick Start Guide

## 🎯 What You Have

1. **Training Script**: `ml_isolation_forest_normal_only_training.py`
   - Trains ONLY on normal traffic (label=0)
   - Uses all numeric features
   - Applies StandardScaler
   - Saves model + scaler

2. **Inference Script**: `ml_isolation_forest_inference.py`
   - Loads trained model
   - Predicts anomalies on new data
   - Returns: -1 for anomaly, 1 for normal

---

## 📋 Step-by-Step Instructions

### Step 1: Train the Model

**Option A: Run interactively (prompts for file)**
```bash
python ml_isolation_forest_normal_only_training.py
# When prompted, enter: csv/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv
```

**Option B: Run with path directly**
```python
from ml_isolation_forest_normal_only_training import IsolationForestNormalOnlyTrainer

trainer = IsolationForestNormalOnlyTrainer()
trainer.run_training('csv/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv')
```

**What happens:**
- ✅ Loads CSV file
- ✅ Filters only normal traffic (label=0)
- ✅ Selects numeric features
- ✅ Scales with StandardScaler
- ✅ Trains Isolation Forest (1500 trees, max_features=0.8, contamination='auto')
- ✅ Saves to `ml_models/` directory

**Output files:**
- `ml_models/isolationforest_normal_only_model.pkl`
- `ml_models/isolationforest_normal_only_scaler.pkl`
- `ml_models/isolationforest_normal_only_features.json`
- `ml_results/isolationforest_normal_only_stats.json`

---

### Step 2: Test the Model

**Option A: Run inference script**
```bash
python ml_isolation_forest_inference.py
# When prompted, enter test CSV path
```

**Option B: Use in Python code**
```python
from ml_isolation_forest_inference import predict_anomalies
import pandas as pd

# Load test data
test_data = pd.read_csv('csv/CSV Files/Training and Testing Sets/UNSW_NB15_testing-set.csv')

# Predict anomalies
predictions = predict_anomalies(test_data)

# predictions: -1 = anomaly, 1 = normal
# Automatically prints anomaly ratio
```

---

### Step 3: Integrate with Your System (Optional)

Update `ml_prediction_system.py` to use the new model:

```python
# In ml_prediction_system.py, add:
from ml_isolation_forest_inference import IsolationForestInference

# Initialize
if_inference = IsolationForestInference(
    model_path='ml_models/isolationforest_normal_only_model.pkl',
    scaler_path='ml_models/isolationforest_normal_only_scaler.pkl',
    features_path='ml_models/isolationforest_normal_only_features.json'
)

# Use in prediction
predictions = if_inference.predict(log_data)
```

---

## 🚀 Quick Commands

### Train Model:
```bash
python -c "from ml_isolation_forest_normal_only_training import IsolationForestNormalOnlyTrainer; t = IsolationForestNormalOnlyTrainer(); t.run_training('csv/CSV Files/Training and Testing Sets/UNSW_NB15_training-set.csv')"
```

### Test Model:
```bash
python -c "from ml_isolation_forest_inference import predict_anomalies; import pandas as pd; data = pd.read_csv('csv/CSV Files/Training and Testing Sets/UNSW_NB15_testing-set.csv'); predict_anomalies(data)"
```

---

## 📊 Expected Results

**Training:**
- Will use ~93,000 normal samples (from training set)
- Trains Isolation Forest with 1500 trees
- Should complete in 5-15 minutes

**Testing:**
- Will predict on test data
- Should detect anomalies (attacks) as -1
- Prints anomaly ratio statistics

---

## ✅ Checklist

- [ ] Run training script
- [ ] Verify model files are created in `ml_models/`
- [ ] Test inference on test dataset
- [ ] Check anomaly ratio (should detect attacks)
- [ ] (Optional) Integrate into existing system

---

## 🔧 Troubleshooting

**If training fails:**
- Check CSV file path is correct
- Ensure CSV has 'label' column
- Verify Python packages installed: `pip install pandas numpy scikit-learn joblib`

**If inference fails:**
- Make sure training completed successfully
- Check that model files exist in `ml_models/`
- Verify test data has same feature columns

---

## 💡 Next Steps After Training

1. **Evaluate Performance**: Test on test dataset and check accuracy
2. **Compare with Old Model**: See if new approach improves accuracy
3. **Integrate**: Update `ml_prediction_system.py` to use new model
4. **Monitor**: Use in production and track anomaly detection rates


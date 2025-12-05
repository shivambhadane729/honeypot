# 🧹 Project Cleanup Guide

## Files/Directories to Remove

### 1. Duplicate Model Files (Nested Directory)
```bash
# These are duplicates - already in ml_models/
rm -rf ml_models/ml_models/
```

**Files in nested directory:**
- `ml_models/ml_models/trian.py` - Typo file (old version)
- `ml_models/ml_models/UNSW_NB15_*.csv` - Duplicate dataset files
- `ml_models/ml_models/ml_models/*.pkl` - Duplicate model files

### 2. Already Deleted
- ✅ `ml_models/3687527.zip.fdmdownload`
- ✅ `ml_models/Honeypot data.zip`

### 3. Optional Cleanup (Review First)
- `ml_models/model.pkl` - Check if duplicate of randomforest_model.pkl
- `ml_models/model_info.json` - Check if duplicate of best_model_info.json
- `ml_models/logisticregression_model.pkl` - Only needed if using Logistic Regression

## Safe to Delete

All files in `ml_models/ml_models/` are duplicates and safe to delete.

## Keep These

- ✅ All `*_model.pkl` files in `ml_models/`
- ✅ All `*_model_info.json` files
- ✅ All `*_encoder.pkl` files
- ✅ All `*_scaler.pkl` files
- ✅ All `feature_selector.pkl` files
- ✅ `best_model_info.json`
- ✅ `feature_columns.json`

## Manual Cleanup Commands (Windows PowerShell)

```powershell
# Remove nested duplicate directory
Remove-Item -Recurse -Force "ml_models\ml_models"

# Optional: Remove old/duplicate files (review first!)
# Remove-Item "ml_models\model.pkl"
# Remove-Item "ml_models\model_info.json"
```

## Verification

After cleanup, verify these files exist:
- ✅ `ml_models/randomforest_model.pkl`
- ✅ `ml_models/isolationforest_model.pkl`
- ✅ `ml_models/best_model_info.json`
- ✅ `ml_models/isolationforest_model_info.json`
- ✅ All encoders and scalers


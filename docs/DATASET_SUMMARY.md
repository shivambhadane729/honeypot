# 📊 Dataset Summary - ML Training Data

## Overview

Your project uses **ONE primary dataset** for training both ML models:

---

## 🎯 **UNSW-NB15 Dataset** (Primary Dataset)

### Status: ✅ Used for ALL ML Models

### Dataset Structure:
- **Name**: UNSW-NB15 (University of New South Wales Network-Based 15)
- **Type**: Network intrusion detection dataset
- **Purpose**: Training models to detect network attacks

### Dataset Files:
```
csv/CSV Files/Training and Testing Sets/
├── UNSW_NB15_training-set.csv  (175,341 rows)
└── UNSW_NB15_testing-set.csv   (82,332 rows)
```

### Combined Dataset Statistics:
- **Total Samples**: **257,673 rows**
- **Total Features**: **45 columns**
- **Attack Samples**: **164,673** (63.91%)
- **Normal Samples**: **93,000** (36.09%)
- **Attack Rate**: 63.91%

### Training/Testing Split:
- **Training Set**: 175,341 rows (68.06%)
- **Testing Set**: 82,332 rows (31.94%)

### Attack Categories:
The dataset includes **9 types of attacks**:

| Attack Type | Samples | Percentage |
|------------|---------|------------|
| **Generic** | 58,871 | 35.74% |
| **Exploits** | 44,525 | 27.03% |
| **Fuzzers** | 24,246 | 14.72% |
| **DoS** | 16,353 | 9.93% |
| **Reconnaissance** | 13,987 | 8.49% |
| **Analysis** | 2,677 | 1.63% |
| **Backdoor** | 2,329 | 1.41% |
| **Shellcode** | 1,511 | 0.92% |
| **Worms** | 174 | 0.11% |

---

## 🔄 How Models Use the Dataset

### 1. **Random Forest (Supervised Learning)**
- **Training**: Uses `UNSW_NB15_training-set.csv` (175,341 rows)
- **Testing**: Uses `UNSW_NB15_testing-set.csv` (82,332 rows)
- **Process**: 
  - Loads both files
  - Combines them (257,673 total rows)
  - Splits into train/test internally (80/20)
  - Trains on labeled data (attack = 1, normal = 0)
- **File**: `ml_training_system.py`

### 2. **Isolation Forest (Unsupervised Learning)**
- **Training**: Uses `UNSW_NB15_training-set.csv` (175,341 rows)
- **Testing**: Uses `UNSW_NB15_testing-set.csv` (82,332 rows)
- **Process**:
  - Loads both files
  - Combines them (257,673 total rows)
  - Uses labels only for evaluation (not for training)
  - Trains as unsupervised anomaly detector
- **File**: `ml_isolation_forest_training.py`

---

## 📁 Additional CSV Files (Auxiliary/Metadata)

Located in `csv/CSV Files/`:

1. **NUSW-NB15_features.csv** - Feature descriptions/metadata
2. **NUSW-NB15_GT.csv** - Ground truth labels (auxiliary)
3. **UNSW-NB15_1.csv** - Part of full dataset (not used)
4. **UNSW-NB15_2.csv** - Part of full dataset (not used)
5. **UNSW-NB15_3.csv** - Part of full dataset (not used)
6. **UNSW-NB15_4.csv** - Part of full dataset (not used)
7. **UNSW-NB15_LIST_EVENTS.csv** - Event list/reference
8. **The UNSW-NB15 description.pdf** - Dataset documentation

**Note**: These files are part of the UNSW-NB15 dataset package but are **NOT used for training**. Only the training-set and testing-set files in the "Training and Testing Sets" folder are used.

---

## 📊 Dataset Features (45 Columns)

The dataset includes network flow features such as:

### Basic Network Features:
- `dur` - Duration of flow
- `proto` - Protocol (TCP, UDP, etc.)
- `service` - Service type (HTTP, FTP, etc.)
- `state` - Connection state

### Packet Statistics:
- `spkts`, `dpkts` - Source/Destination packets
- `sbytes`, `dbytes` - Source/Destination bytes
- `rate` - Flow rate

### Timing Features:
- `sttl`, `dttl` - Source/Destination TTL
- `sload`, `dload` - Source/Destination load
- `sinpkt`, `dinpkt` - Inter-packet times

### Connection Tracking:
- `ct_srv_src`, `ct_srv_dst` - Connection counts
- `ct_state_ttl` - State-based connection tracking
- `ct_dst_ltm`, `ct_src_ltm` - Last time seen

### Protocol-Specific:
- `is_ftp_login` - FTP login indicator
- `ct_ftp_cmd` - FTP command tracking
- `ct_flw_http_mthd` - HTTP method tracking

### Target Variables:
- `label` - Binary classification (0 = Normal, 1 = Attack)
- `attack_cat` - Attack category (Normal, Generic, Exploits, etc.)

---

## 🎓 Dataset Characteristics

### Strengths:
✅ Large dataset (257K+ samples)
✅ Comprehensive attack types (9 categories)
✅ Real-world network traffic patterns
✅ Balanced feature set (45 features)
✅ Standardized format (CSV)

### Considerations:
⚠️ **High attack rate** (63.91% attacks) - Most samples are attacks
⚠️ **Class imbalance** - More attacks than normal traffic
⚠️ **Fixed split** - Training/testing split is predefined

### Why It's Good for Honeypot Training:
1. **Real network data** - Represents actual attack patterns
2. **Multiple attack types** - Covers various attack scenarios
3. **Feature-rich** - 45 features capture network behavior
4. **Well-documented** - Standard benchmark dataset

---

## 📈 Dataset Usage Summary

### Models Trained:
| Model | Dataset Used | Samples Used | Training Method |
|-------|--------------|--------------|-----------------|
| **Random Forest** | UNSW-NB15 | 257,673 total | Supervised (uses labels) |
| **Isolation Forest** | UNSW-NB15 | 257,673 total | Unsupervised (labels for eval only) |

### Key Point:
- **Both models use the SAME dataset** (UNSW-NB15)
- **Same 2 CSV files** for both models
- **Different training approaches** (supervised vs unsupervised)

---

## 📂 File Locations

```
HONEYPOT/
├── csv/
│   └── CSV Files/
│       ├── Training and Testing Sets/
│       │   ├── UNSW_NB15_training-set.csv  ← Used for training
│       │   └── UNSW_NB15_testing-set.csv   ← Used for testing
│       ├── UNSW-NB15_*.csv                 ← Not used (auxiliary)
│       └── NUSW-NB15_*.csv                 ← Not used (metadata)
│
├── ml_training_system.py                   ← Uses UNSW-NB15
├── ml_isolation_forest_training.py         ← Uses UNSW-NB15
│
└── ml_results/
    ├── dataset_stats.json                  ← Random Forest stats
    └── isolation_forest_stats.json         ← Isolation Forest stats
```

---

## 🎯 Summary

**Answer to "How many datasets?"**

### Short Answer:
- **1 primary dataset** (UNSW-NB15)
- **2 CSV files** (training-set.csv + testing-set.csv)
- **257,673 total samples** (combined)
- **Used by both ML models**

### Detailed Breakdown:
- **Random Forest**: Uses UNSW-NB15 (supervised learning)
- **Isolation Forest**: Uses UNSW-NB15 (unsupervised learning)
- **Both combine** training + testing sets for full dataset access
- **Same source**, different training approaches

---

## 💡 Next Steps

If you want to improve model performance, consider:
1. **Adding more datasets** - Combine with other network datasets
2. **Collecting honeypot-specific data** - Train on actual honeypot logs
3. **Data augmentation** - Generate synthetic attack patterns
4. **Balance classes** - Address the 64% attack rate imbalance


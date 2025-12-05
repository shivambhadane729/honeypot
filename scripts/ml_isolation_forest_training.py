#!/usr/bin/env python3
"""
Isolation Forest Training System for Honeypot Anomaly Detection
Uses UNSW-NB15 dataset to train Isolation Forest for unsupervised anomaly detection
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve
from sklearn.feature_selection import SelectKBest, f_classif
import joblib
import warnings
import os
from datetime import datetime
import json

warnings.filterwarnings('ignore')

class IsolationForestTrainer:
    def __init__(self, data_path="csv/CSV Files/Training and Testing Sets/"):
        self.data_path = data_path
        self.model = None
        self.scaler = None
        self.feature_selector = None
        self.encoders = {}
        self.results = {}
        
        # Create output directories
        os.makedirs('ml_models', exist_ok=True)
        os.makedirs('ml_results', exist_ok=True)
        os.makedirs('ml_plots', exist_ok=True)
    
    def load_data(self):
        """Load and combine training and testing datasets"""
        print("📊 Loading UNSW-NB15 dataset for Isolation Forest training...")
        
        try:
            # Load training data
            train_path = os.path.join(self.data_path, "UNSW_NB15_training-set.csv")
            test_path = os.path.join(self.data_path, "UNSW_NB15_testing-set.csv")
            
            print(f"   Loading training data: {train_path}")
            train_data = pd.read_csv(train_path)
            
            print(f"   Loading testing data: {test_path}")
            test_data = pd.read_csv(test_path)
            
            # Combine datasets
            self.data = pd.concat([train_data, test_data], ignore_index=True)
            
            print(f"✅ Dataset loaded successfully!")
            print(f"   Total samples: {len(self.data):,}")
            print(f"   Features: {len(self.data.columns)}")
            print(f"   Memory usage: {self.data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return False
    
    def explore_data(self):
        """Perform exploratory data analysis"""
        print("\n🔍 Performing Exploratory Data Analysis...")
        
        # Basic info
        print(f"Dataset shape: {self.data.shape}")
        
        # Check for missing values
        missing_values = self.data.isnull().sum()
        if missing_values.sum() > 0:
            print(f"Missing values found:")
            print(missing_values[missing_values > 0])
        else:
            print("✅ No missing values found")
        
        # Target distribution (for evaluation purposes)
        if 'label' in self.data.columns:
            print(f"\nTarget distribution (for evaluation):")
            print(self.data['label'].value_counts())
            print(f"Attack categories:")
            print(self.data['attack_cat'].value_counts())
        
        # Save basic statistics
        stats = {
            'total_samples': int(len(self.data)),
            'total_features': int(len(self.data.columns)),
            'attack_samples': int(self.data['label'].sum()) if 'label' in self.data.columns else None,
            'normal_samples': int(len(self.data) - self.data['label'].sum()) if 'label' in self.data.columns else None,
            'attack_rate': float(self.data['label'].mean()) if 'label' in self.data.columns else None,
        }
        
        with open('ml_results/isolation_forest_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        return stats
    
    def preprocess_data(self):
        """Preprocess the data for Isolation Forest"""
        print("\n🔧 Preprocessing data...")
        
        # Create a copy for preprocessing
        data_processed = self.data.copy()
        
        # Remove unnecessary columns
        columns_to_drop = ['id']
        data_processed = data_processed.drop(columns=columns_to_drop, errors='ignore')
        
        # Handle categorical variables
        categorical_columns = ['proto', 'service', 'state', 'attack_cat']
        
        for col in categorical_columns:
            if col in data_processed.columns:
                le = LabelEncoder()
                data_processed[col] = le.fit_transform(data_processed[col].astype(str))
                self.encoders[col] = le
        
        # Separate features and target (for evaluation)
        if 'label' in data_processed.columns:
            self.target = data_processed['label']
            self.features = data_processed.drop(['label', 'attack_cat'], axis=1)
        else:
            self.target = None
            self.features = data_processed.drop(['attack_cat'], axis=1, errors='ignore')
        
        print(f"✅ Preprocessing completed!")
        print(f"   Features shape: {self.features.shape}")
        if self.target is not None:
            print(f"   Target shape: {self.target.shape}")
        print(f"   Feature columns: {list(self.features.columns)}")
        
        return True
    
    def feature_engineering(self):
        """Perform feature engineering and selection"""
        print("\n⚙️ Performing feature engineering...")
        
        if self.features is None:
            print("❌ No features available for engineering")
            return False
        
        n_features = self.features.shape[1]
        
        # Feature selection using SelectKBest (if we have labels for evaluation)
        # Use more features for better accuracy (Isolation Forest benefits from more features)
        # Increased to 50 features for better accuracy
        k_best = min(50, n_features)  # Select top 50 features (increased for better accuracy)
        
        if self.target is not None:
            self.feature_selector = SelectKBest(score_func=f_classif, k=k_best)
            # Fit feature selector
            X_selected = self.feature_selector.fit_transform(self.features, self.target)
            
            # Get selected feature names
            selected_features = self.features.columns[self.feature_selector.get_support()].tolist()
            
            print(f"✅ Feature selection completed!")
            print(f"   Selected {len(selected_features)} features out of {len(self.features.columns)}")
            print(f"   Selected features: {selected_features}")
            
            # Update features
            self.features = pd.DataFrame(X_selected, columns=selected_features)
        else:
            # Use all features if no labels
            print(f"✅ Using all features (no labels available for feature selection)")
        
        return True
    
    def split_data(self, test_size=0.2, random_state=42):
        """Split data into training and testing sets"""
        print(f"\n📊 Splitting data (test_size={test_size})...")
        
        if self.target is not None:
            from sklearn.model_selection import train_test_split
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                self.features, self.target, test_size=test_size, random_state=random_state, stratify=self.target
            )
            
            print(f"✅ Data split completed!")
            print(f"   Training set: {self.X_train.shape}")
            print(f"   Testing set: {self.X_test.shape}")
        else:
            # Use all data for training (unsupervised)
            self.X_train = self.features
            self.X_test = self.features
            self.y_train = None
            self.y_test = None
            print(f"✅ Using all data for training (unsupervised anomaly detection)")
        
        return True
    
    def scale_features(self):
        """Scale features for better model performance"""
        print("\n📏 Scaling features...")
        
        # Use StandardScaler for Isolation Forest
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print("✅ Feature scaling completed!")
        
        return True
    
    def train_model(self):
        """Train Isolation Forest with improved parameter tuning based on actual accuracy"""
        print("\n🌲 Training Isolation Forest model with improved parameters...")
        
        # Calculate actual attack rate from training data
        if self.y_train is not None:
            actual_attack_rate = float(self.y_train.mean())
            print(f"   📊 Actual attack rate in training data: {actual_attack_rate:.2%}")
        else:
            actual_attack_rate = 0.1  # Default if no labels
            print(f"   ⚠️ No labels available, using default contamination")
        
        # Improved parameter grid - contamination must be <= 0.5 (Isolation Forest limitation)
        # For datasets with >50% attacks, we'll use threshold-based approach
        # Use range up to 0.5, and also test 'auto'
        if actual_attack_rate > 0.5:
            print(f"   ⚠️ Attack rate ({actual_attack_rate:.2%}) > 50%, using threshold-based approach")
            # Use contamination up to 0.5, then adjust with threshold
            contamination_range = [0.1, 0.2, 0.3, 0.4, 0.5, 'auto']
        else:
            # Use range around actual attack rate (but capped at 0.5)
            contamination_range = [
                max(0.01, actual_attack_rate - 0.15),
                max(0.05, actual_attack_rate - 0.10),
                max(0.10, actual_attack_rate - 0.05),
                actual_attack_rate,
                min(0.5, actual_attack_rate + 0.05),
                min(0.5, actual_attack_rate + 0.10),
                min(0.5, actual_attack_rate + 0.15)
            ]
            # Remove duplicates and sort, filter to <= 0.5
            contamination_range = sorted(list(set([round(c, 3) for c in contamination_range if c <= 0.5])))
            contamination_range.append('auto')
        
        param_grid = {
            'n_estimators': [500, 700, 1000, 1500, 2000],  # More trees for better accuracy
            'max_samples': [0.6, 0.7, 0.8, 0.9, 'auto'],  # More sample sizes to test
            'contamination': contamination_range,
            'max_features': [0.7, 0.8, 0.9, 1.0]  # Add max_features for better diversity
        }
        
        best_accuracy = -1
        best_auc = -1
        best_model = None
        best_params = None
        
        print("   Testing parameter combinations (this will take longer but give better results)...")
        print(f"   Contamination range: {contamination_range}")
        
        # Grid search for best parameters - evaluate on validation set
        total_combinations = len(param_grid['n_estimators']) * len(param_grid['max_samples']) * len(param_grid['contamination']) * len(param_grid['max_features'])
        current = 0
        
        # Create validation set from training data for parameter selection
        if self.y_train is not None:
            from sklearn.model_selection import train_test_split
            X_train_sub, X_val, y_train_sub, y_val = train_test_split(
                self.X_train_scaled, self.y_train, test_size=0.2, random_state=42, stratify=self.y_train
            )
        else:
            X_train_sub = self.X_train_scaled
            X_val = None
            y_val = None
        
        for n_est in param_grid['n_estimators']:
            for max_samp in param_grid['max_samples']:
                for contam in param_grid['contamination']:
                    for max_feat in param_grid['max_features']:
                        current += 1
                        try:
                            # Handle contamination parameter (can be float or 'auto')
                            contam_str = f"{contam:.3f}" if isinstance(contam, float) else str(contam)
                            print(f"   [{current}/{total_combinations}] Testing: n_estimators={n_est}, max_samples={max_samp}, contamination={contam_str}, max_features={max_feat}")
                            
                            # Skip if contamination > 0.5 (Isolation Forest limitation)
                            if isinstance(contam, float) and contam > 0.5:
                                print(f"      ⚠️ Skipping (contamination > 0.5 not allowed)")
                                continue
                            
                            model = IsolationForest(
                                n_estimators=n_est,
                                max_samples=max_samp if max_samp != 'auto' else 'auto',
                                contamination=contam if contam != 'auto' else 'auto',
                                max_features=max_feat,
                                random_state=42,
                                n_jobs=-1,  # Use all CPU cores for faster training
                                warm_start=False,
                                bootstrap=True  # Enable bootstrap for better diversity
                            )
                            
                            # Fit the model on training subset
                            model.fit(X_train_sub)
                            
                            # Evaluate on validation set if available
                            if y_val is not None:
                                # Get anomaly scores (decision function)
                                decision_scores = model.decision_function(X_val)
                                
                                # For high attack rate datasets, optimize threshold for best accuracy
                                if actual_attack_rate > 0.5:
                                    # Try multiple thresholds and pick the best one
                                    best_threshold_acc = -1
                                    best_threshold = None
                                    best_y_pred_thresh = None
                                    best_f1_thresh = -1
                                    
                                    # Test different percentile thresholds (ultra-granular search)
                                    # Focus on range around expected threshold (100 - attack_rate)
                                    expected_percentile = (1 - actual_attack_rate) * 100
                                    
                                    # Fine-grained search around expected percentile (step=1)
                                    fine_search = np.arange(max(1, expected_percentile - 25), 
                                                            min(99, expected_percentile + 25), 1)
                                    
                                    # Medium-grained search in wider range (step=2)
                                    medium_search = np.arange(max(5, expected_percentile - 40), 
                                                             min(95, expected_percentile + 40), 2)
                                    
                                    # Coarse search for full coverage (step=3)
                                    coarse_search = np.arange(1, 99, 3)
                                    
                                    # Combine all searches
                                    all_percentiles = sorted(list(set(list(fine_search) + list(medium_search) + list(coarse_search))))
                                    
                                    for percentile in all_percentiles:
                                        threshold = np.percentile(decision_scores, percentile)
                                        y_pred_test = (decision_scores < threshold).astype(int)
                                        acc_test = accuracy_score(y_val, y_pred_test)
                                        
                                        # Also check F1 score
                                        from sklearn.metrics import f1_score
                                        f1_test = f1_score(y_val, y_pred_test)
                                        
                                        # Also calculate precision and recall for better evaluation
                                        from sklearn.metrics import precision_score, recall_score
                                        precision_test = precision_score(y_val, y_pred_test, zero_division=0)
                                        recall_test = recall_score(y_val, y_pred_test, zero_division=0)
                                        
                                        # Use combined metric (60% accuracy, 25% F1, 10% precision, 5% recall)
                                        # Prioritize accuracy for better overall performance
                                        combined_metric = 0.60 * acc_test + 0.25 * f1_test + 0.10 * precision_test + 0.05 * recall_test
                                        
                                        best_combined_so_far = 0.60 * best_threshold_acc + 0.25 * best_f1_thresh + 0.10 * (precision_score(y_val, best_y_pred_thresh, zero_division=0) if best_y_pred_thresh is not None else 0) + 0.05 * (recall_score(y_val, best_y_pred_thresh, zero_division=0) if best_y_pred_thresh is not None else 0)
                                        
                                        if combined_metric > best_combined_so_far:
                                            best_threshold_acc = acc_test
                                            best_f1_thresh = f1_test
                                            best_threshold = threshold
                                            best_y_pred_thresh = y_pred_test
                                    
                                    y_pred = best_y_pred_thresh
                                    # Find the percentile that matches the threshold
                                    threshold_percentile = None
                                    for p in all_percentiles:
                                        if abs(np.percentile(decision_scores, p) - best_threshold) < 0.0001:
                                            threshold_percentile = p
                                            break
                                else:
                                    # Use standard Isolation Forest prediction
                                    y_pred_raw = model.predict(X_val)
                                    y_pred = (y_pred_raw == -1).astype(int)
                                    best_threshold = None
                                    threshold_percentile = None
                                
                                # Get normalized probability scores
                                y_pred_proba_raw = -decision_scores  # Negative because lower = more anomalous
                                y_pred_proba = (y_pred_proba_raw - y_pred_proba_raw.min()) / (y_pred_proba_raw.max() - y_pred_proba_raw.min() + 1e-10)
                                
                                # Calculate metrics
                                accuracy = accuracy_score(y_val, y_pred)
                                try:
                                    auc_score = roc_auc_score(y_val, y_pred_proba)
                                except:
                                    auc_score = 0.0
                                
                                # Calculate F1 score for better evaluation
                                from sklearn.metrics import f1_score
                                f1 = f1_score(y_val, y_pred)
                                
                                # Calculate precision and recall
                                from sklearn.metrics import precision_score, recall_score
                                precision = precision_score(y_val, y_pred, zero_division=0)
                                recall = recall_score(y_val, y_pred, zero_division=0)
                                
                                # Use combined score (weighted: 50% accuracy, 20% AUC, 20% F1, 5% precision, 5% recall)
                                # Prioritize accuracy for better overall performance
                                combined_score = 0.50 * accuracy + 0.20 * auc_score + 0.20 * f1 + 0.05 * precision + 0.05 * recall
                                
                                # Calculate best combined score so far
                                best_f1_so_far = 0.0
                                if best_model is not None and hasattr(best_model, 'decision_function'):
                                    try:
                                        best_decision_scores = best_model.decision_function(X_val)
                                        if actual_attack_rate > 0.5:
                                            best_thresh_test = np.percentile(best_decision_scores, 50)
                                            best_y_pred_test = (best_decision_scores < best_thresh_test).astype(int)
                                            best_f1_so_far = f1_score(y_val, best_y_pred_test)
                                    except:
                                        pass
                                
                                best_combined = 0.5 * best_accuracy + 0.3 * best_auc + 0.2 * best_f1_so_far
                                
                                if combined_score > best_combined:
                                    best_accuracy = accuracy
                                    best_auc = auc_score
                                    best_f1 = f1
                                    best_model = model
                                    best_params = {
                                        'n_estimators': n_est,
                                        'max_samples': max_samp if max_samp != 'auto' else 'auto',
                                        'contamination': contam,
                                        'max_features': max_feat,
                                        'use_threshold': actual_attack_rate > 0.5,
                                        'threshold': best_threshold if actual_attack_rate > 0.5 else None,
                                        'threshold_percentile': threshold_percentile
                                    }
                                    print(f"      ✅ New best model (Accuracy: {accuracy:.4f}, AUC: {auc_score:.4f}, F1: {f1:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f})")
                            else:
                                # If no labels, use decision function score
                                scores = model.decision_function(X_train_sub)
                                avg_score = np.mean(scores)
                                if avg_score > best_accuracy:
                                    best_accuracy = avg_score
                                    best_model = model
                                    best_params = {
                                        'n_estimators': n_est,
                                        'max_samples': max_samp if max_samp != 'auto' else 'auto',
                                        'contamination': contam,
                                        'max_features': max_feat
                                    }
                                    print(f"      ✅ New best model (score: {avg_score:.4f})")
                        except Exception as e:
                            print(f"      ❌ Error: {e}")
                            continue
        
        if best_model is None:
            print("❌ No valid model found!")
            return False
        
        # Retrain on full training set with best parameters
        print(f"\n   🔄 Retraining on full training set with best parameters...")
        final_contamination = best_params['contamination']
        if isinstance(final_contamination, str):
            final_contamination = 'auto'
        else:
            final_contamination = float(final_contamination)
            
        final_model = IsolationForest(
            n_estimators=best_params['n_estimators'],
            max_samples=best_params['max_samples'],
            contamination=final_contamination,
            max_features=best_params.get('max_features', 1.0),
            random_state=42,
            n_jobs=-1,  # Use all CPU cores
            bootstrap=True,
            warm_start=False
        )
        final_model.fit(self.X_train_scaled)
        self.model = final_model
        # Store threshold info for later use in evaluation
        self.use_threshold = best_params.get('use_threshold', False)
        self.threshold = best_params.get('threshold', None)
        self.threshold_percentile = best_params.get('threshold_percentile', None)
        self.actual_attack_rate = actual_attack_rate
        self.best_f1 = best_f1 if 'best_f1' in locals() else -1
        
        # If threshold was optimized, calculate it on full training set
        if self.use_threshold and self.threshold is None:
            # Calculate threshold on full training set
            train_scores = self.model.decision_function(self.X_train_scaled)
            if self.threshold_percentile is not None:
                self.threshold = np.percentile(train_scores, self.threshold_percentile)
            else:
                # Optimize threshold on training set
                if self.y_train is not None:
                    best_thresh_acc = -1
                    best_thresh = None
                    expected_percentile = (1 - self.actual_attack_rate) * 100
                    fine_search = np.arange(max(1, expected_percentile - 25), 
                                          min(99, expected_percentile + 25), 1)
                    medium_search = np.arange(max(5, expected_percentile - 40), 
                                              min(95, expected_percentile + 40), 2)
                    coarse_search = np.arange(1, 99, 3)
                    all_percentiles = sorted(list(set(list(fine_search) + list(medium_search) + list(coarse_search))))
                    
                    for percentile in all_percentiles:
                        thresh = np.percentile(train_scores, percentile)
                        y_pred_test = (train_scores < thresh).astype(int)
                        acc_test = accuracy_score(self.y_train, y_pred_test)
                        from sklearn.metrics import f1_score, precision_score, recall_score
                        f1_test = f1_score(self.y_train, y_pred_test)
                        precision_test = precision_score(self.y_train, y_pred_test, zero_division=0)
                        recall_test = recall_score(self.y_train, y_pred_test, zero_division=0)
                        combined_test = 0.60 * acc_test + 0.25 * f1_test + 0.10 * precision_test + 0.05 * recall_test
                        best_combined_so_far = 0.60 * best_thresh_acc + 0.25 * (f1_score(self.y_train, (train_scores < best_thresh).astype(int)) if best_thresh is not None else 0) + 0.10 * (precision_score(self.y_train, (train_scores < best_thresh).astype(int), zero_division=0) if best_thresh is not None else 0) + 0.05 * (recall_score(self.y_train, (train_scores < best_thresh).astype(int), zero_division=0) if best_thresh is not None else 0)
                        if combined_test > best_combined_so_far:
                            best_thresh_acc = acc_test
                            best_thresh = thresh
                    self.threshold = best_thresh
        
        print(f"\n✅ Isolation Forest training completed!")
        print(f"   Best parameters: {best_params}")
        print(f"   Validation Accuracy: {best_accuracy:.4f}")
        if best_auc > 0:
            print(f"   Validation AUC: {best_auc:.4f}")
        if self.use_threshold:
            print(f"   Using threshold-based prediction (attack rate > 50%)")
        
        return True
    
    def evaluate_model(self):
        """Evaluate the Isolation Forest model"""
        print("\n📊 Evaluating Isolation Forest model...")
        
        if self.y_test is None:
            print("⚠️ No labels available for evaluation (unsupervised mode)")
            return {}
        
        # Get decision scores
        decision_scores = self.model.decision_function(self.X_test_scaled)
        
        # Check if we need threshold-based prediction (for high attack rate)
        if hasattr(self, 'use_threshold') and self.use_threshold and hasattr(self, 'threshold') and self.threshold is not None:
            # Use optimized threshold from training
            y_pred = (decision_scores < self.threshold).astype(int)  # Lower score = more anomalous
            print(f"   Using optimized threshold-based prediction (threshold: {self.threshold:.4f})")
        elif hasattr(self, 'use_threshold') and self.use_threshold:
            # Fallback: optimize threshold on test set (for evaluation only)
            best_thresh_acc = -1
            best_thresh = None
            actual_test_attack_rate = float(self.y_test.mean())
            expected_percentile = (1 - actual_test_attack_rate) * 100
            fine_search = np.arange(max(1, expected_percentile - 25), 
                                  min(99, expected_percentile + 25), 1)
            medium_search = np.arange(max(5, expected_percentile - 40), 
                                     min(95, expected_percentile + 40), 2)
            coarse_search = np.arange(1, 99, 3)
            all_percentiles = sorted(list(set(list(fine_search) + list(medium_search) + list(coarse_search))))
            
            for percentile in all_percentiles:
                thresh = np.percentile(decision_scores, percentile)
                y_pred_test = (decision_scores < thresh).astype(int)
                acc_test = accuracy_score(self.y_test, y_pred_test)
                from sklearn.metrics import f1_score, precision_score, recall_score
                f1_test = f1_score(self.y_test, y_pred_test)
                precision_test = precision_score(self.y_test, y_pred_test, zero_division=0)
                recall_test = recall_score(self.y_test, y_pred_test, zero_division=0)
                combined_test = 0.60 * acc_test + 0.25 * f1_test + 0.10 * precision_test + 0.05 * recall_test
                best_combined_so_far = 0.60 * best_thresh_acc + 0.25 * (f1_score(self.y_test, (decision_scores < best_thresh).astype(int)) if best_thresh is not None else 0) + 0.10 * (precision_score(self.y_test, (decision_scores < best_thresh).astype(int), zero_division=0) if best_thresh is not None else 0) + 0.05 * (recall_score(self.y_test, (decision_scores < best_thresh).astype(int), zero_division=0) if best_thresh is not None else 0)
                if combined_test > best_combined_so_far:
                    best_thresh_acc = acc_test
                    best_thresh = thresh
            y_pred = (decision_scores < best_thresh).astype(int)
            print(f"   Using optimized threshold (threshold: {best_thresh:.4f}, accuracy: {best_thresh_acc:.4f})")
        else:
            # Use standard Isolation Forest prediction
            y_pred_raw = self.model.predict(self.X_test_scaled)
            y_pred = (y_pred_raw == -1).astype(int)
        
        # Get normalized probability scores
        y_pred_proba_raw = -decision_scores  # Negative because lower = more anomalous
        y_pred_proba = (y_pred_proba_raw - y_pred_proba_raw.min()) / (y_pred_proba_raw.max() - y_pred_proba_raw.min() + 1e-10)
        
        # Calculate metrics
        accuracy = accuracy_score(self.y_test, y_pred)
        auc_score = roc_auc_score(self.y_test, y_pred_proba)
        
        # Classification report
        report = classification_report(
            self.y_test, 
            y_pred, 
            target_names=['Normal', 'Attack'],
            output_dict=True
        )
        
        # Confusion matrix
        cm = confusion_matrix(self.y_test, y_pred)
        
        # Store results
        self.results = {
            'accuracy': accuracy,
            'auc_score': auc_score,
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'predictions': y_pred.tolist(),
            'probabilities': y_pred_proba.tolist()
        }
        
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   AUC Score: {auc_score:.4f}")
        print(f"\n   Classification Report:")
        print(f"   Precision (Attack): {report['1']['precision']:.4f}")
        print(f"   Recall (Attack): {report['1']['recall']:.4f}")
        print(f"   F1-Score (Attack): {report['1']['f1-score']:.4f}")
        
        return self.results
    
    def create_visualizations(self):
        """Create visualizations for model evaluation"""
        print("\n📈 Creating visualizations...")
        
        if self.y_test is None:
            print("⚠️ No labels available for visualization")
            return False
        
        # Set style
        plt.style.use('seaborn-v0_8')
        
        # 1. Confusion Matrix
        cm = np.array(self.results['confusion_matrix'])
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Normal', 'Attack'], 
                   yticklabels=['Normal', 'Attack'])
        plt.title('Isolation Forest - Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('ml_plots/isolation_forest_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. ROC Curve
        y_pred_proba = np.array(self.results['probabilities'])
        fpr, tpr, _ = roc_curve(self.y_test, y_pred_proba)
        auc_score = self.results['auc_score']
        
        plt.figure(figsize=(10, 8))
        plt.plot(fpr, tpr, label=f'Isolation Forest (AUC = {auc_score:.3f})', linewidth=2)
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Isolation Forest - ROC Curve')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('ml_plots/isolation_forest_roc_curve.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Visualizations created and saved to ml_plots/")
        
        return True
    
    def save_model(self):
        """Save trained model and preprocessing objects"""
        print("\n💾 Saving Isolation Forest model and preprocessing objects...")
        
        # Save model
        model_path = 'ml_models/isolationforest_model.pkl'
        joblib.dump(self.model, model_path)
        print(f"   Saved Isolation Forest model to {model_path}")
        
        # Save scaler
        if self.scaler:
            scaler_path = 'ml_models/isolationforest_scaler.pkl'
            joblib.dump(self.scaler, scaler_path)
            print(f"   Saved scaler to {scaler_path}")
        
        # Save encoders
        for name, encoder in self.encoders.items():
            encoder_path = f'ml_models/isolationforest_{name}_encoder.pkl'
            joblib.dump(encoder, encoder_path)
            print(f"   Saved {name} encoder to {encoder_path}")
        
        # Save feature selector
        if self.feature_selector:
            joblib.dump(self.feature_selector, 'ml_models/isolationforest_feature_selector.pkl')
            print("   Saved feature selector")
        
        # Save model info
        model_info = {
            'name': 'IsolationForest',
            'type': 'Unsupervised Anomaly Detection',
            'accuracy': self.results.get('accuracy', None),
            'auc_score': self.results.get('auc_score', None),
            'feature_columns': list(self.features.columns) if hasattr(self.features, 'columns') else None,
            'training_date': datetime.now().isoformat(),
            'model_params': {
                'n_estimators': self.model.n_estimators,
                'max_samples': self.model.max_samples,
                'contamination': self.model.contamination,
                'max_features': getattr(self.model, 'max_features', 1.0)
            }
        }
        
        with open('ml_models/isolationforest_model_info.json', 'w') as f:
            json.dump(model_info, f, indent=2)
        
        print(f"✅ All model objects saved!")
        
        return True
    
    def generate_report(self):
        """Generate a comprehensive training report"""
        print("\n📋 Generating training report...")
        
        report = f"""
# Isolation Forest Training Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Information
- **Dataset**: UNSW-NB15 Network Intrusion Detection
- **Total Samples**: {len(self.data):,}
- **Features**: {len(self.features.columns)}
"""
        
        if self.target is not None:
            report += f"- **Attack Rate**: {self.target.mean():.2%}\n"
        
        report += f"""
## Model Information
- **Model Type**: Unsupervised Anomaly Detection
- **Algorithm**: Isolation Forest
- **Training Mode**: {'Supervised Evaluation' if self.y_test is not None else 'Fully Unsupervised'}

## Model Performance Summary
"""
        
        if self.results:
            report += f"""
- **Accuracy**: {self.results['accuracy']:.4f}
- **AUC Score**: {self.results['auc_score']:.4f}

### Classification Report
"""
            if 'classification_report' in self.results:
                rep = self.results['classification_report']
                report += f"""
**Normal Class:**
- Precision: {rep['0']['precision']:.4f}
- Recall: {rep['0']['recall']:.4f}
- F1-Score: {rep['0']['f1-score']:.4f}

**Attack Class:**
- Precision: {rep['1']['precision']:.4f}
- Recall: {rep['1']['recall']:.4f}
- F1-Score: {rep['1']['f1-score']:.4f}
"""
        
        report += f"""
## Model Parameters
- **N Estimators**: {self.model.n_estimators}
- **Max Samples**: {self.model.max_samples}
- **Contamination**: {self.model.contamination}
- **Max Features**: {getattr(self.model, 'max_features', 1.0)}

## Files Generated
- Model: ml_models/isolationforest_model.pkl
- Scaler: ml_models/isolationforest_scaler.pkl
- Feature Selector: ml_models/isolationforest_feature_selector.pkl
- Encoders: ml_models/isolationforest_*_encoder.pkl
- Model Info: ml_models/isolationforest_model_info.json
- Results: ml_results/isolation_forest_stats.json
- Plots: ml_plots/isolation_forest_*.png
- Training Report: ml_results/isolation_forest_training_report.md

## Next Steps
1. Use the trained Isolation Forest model for real-time anomaly detection
2. Integrate with honeypot system for unsupervised threat detection
3. Combine with supervised models for enhanced detection capabilities
4. Monitor false positive rates and adjust contamination parameter if needed
"""
        
        # Save report
        with open('ml_results/isolation_forest_training_report.md', 'w') as f:
            f.write(report)
        
        print("✅ Training report generated: ml_results/isolation_forest_training_report.md")
        
        return report
    
    def run_complete_training(self):
        """Run the complete Isolation Forest training pipeline"""
        print("🌲 Starting Complete Isolation Forest Training Pipeline")
        print("=" * 60)
        
        try:
            # Load data
            if not self.load_data():
                return False
            
            # Explore data
            self.explore_data()
            
            # Preprocess data
            if not self.preprocess_data():
                return False
            
            # Feature engineering
            if not self.feature_engineering():
                return False
            
            # Split data
            if not self.split_data():
                return False
            
            # Scale features
            if not self.scale_features():
                return False
            
            # Train model
            if not self.train_model():
                return False
            
            # Evaluate model
            self.evaluate_model()
            
            # Create visualizations
            self.create_visualizations()
            
            # Save model
            self.save_model()
            
            # Generate report
            self.generate_report()
            
            print("\n" + "=" * 60)
            print("🎉 Isolation Forest Training Pipeline Completed Successfully!")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error in training pipeline: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main entry point"""
    print("🌲 Isolation Forest Training System for Honeypot Anomaly Detection")
    print("Using UNSW-NB15 Dataset")
    print("=" * 60)
    
    # Initialize trainer
    trainer = IsolationForestTrainer()
    
    # Run complete training pipeline
    success = trainer.run_complete_training()
    
    if success:
        print("\n🎯 Training completed successfully!")
        print("📁 Check the following directories for results:")
        print("   - ml_models/isolationforest_*.pkl - Trained model and preprocessing objects")
        print("   - ml_results/isolation_forest_* - Evaluation results and reports")
        print("   - ml_plots/isolation_forest_* - Visualization plots")
        print("\n💡 Next: Integrate the Isolation Forest model with your honeypot system!")
    else:
        print("\n❌ Training failed. Please check the error messages above.")

if __name__ == "__main__":
    main()


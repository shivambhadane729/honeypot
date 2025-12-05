#!/usr/bin/env python3
"""
Isolation Forest Training - Normal Traffic Only
Trains Isolation Forest ONLY on normal traffic (label=0) for true anomaly detection
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os
from datetime import datetime
import json

class IsolationForestNormalOnlyTrainer:
    def __init__(self):
        """Initialize trainer"""
        self.model = None
        self.scaler = None
        self.feature_columns = []
        self.training_stats = {}
        
        # Create output directories
        os.makedirs('ml_models', exist_ok=True)
        os.makedirs('ml_results', exist_ok=True)
    
    def load_data(self, file_path):
        """
        Load CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f"📊 Loading dataset from: {file_path}")
            self.data = pd.read_csv(file_path)
            print(f"✅ Dataset loaded successfully!")
            print(f"   Total rows: {len(self.data):,}")
            print(f"   Total columns: {len(self.data.columns)}")
            
            # Check if label column exists
            if 'label' not in self.data.columns:
                print("❌ Error: 'label' column not found in dataset")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return False
    
    def filter_normal_traffic(self):
        """
        Filter dataset to keep ONLY normal traffic (label=0)
        Remove label column from features
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("\n🔍 Filtering normal traffic only...")
            
            # Filter rows where label = 0 (normal traffic)
            normal_data = self.data[self.data['label'] == 0].copy()
            
            print(f"   Total rows in dataset: {len(self.data):,}")
            print(f"   Normal traffic rows: {len(normal_data):,}")
            print(f"   Attack rows (excluded): {len(self.data) - len(normal_data):,}")
            
            if len(normal_data) == 0:
                print("❌ Error: No normal traffic found (label=0)")
                return False
            
            # Remove label column from features
            if 'label' in normal_data.columns:
                normal_data = normal_data.drop(columns=['label'])
            
            # Also remove attack_cat if present (categorical label)
            if 'attack_cat' in normal_data.columns:
                normal_data = normal_data.drop(columns=['attack_cat'])
            
            # Remove 'id' column if present (not a feature)
            if 'id' in normal_data.columns:
                normal_data = normal_data.drop(columns=['id'])
            
            self.normal_data = normal_data
            
            print(f"✅ Normal traffic filtered!")
            print(f"   Features after removing labels: {len(normal_data.columns)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error filtering normal traffic: {e}")
            return False
    
    def select_numeric_features(self):
        """
        Select only numeric columns for training
        Exclude non-numeric columns
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("\n🔢 Selecting numeric features...")
            
            # Get numeric columns only
            numeric_columns = self.normal_data.select_dtypes(include=[np.number]).columns.tolist()
            
            # Exclude any remaining non-numeric columns
            non_numeric = self.normal_data.select_dtypes(exclude=[np.number]).columns.tolist()
            
            if non_numeric:
                print(f"   ⚠️ Excluding non-numeric columns: {non_numeric}")
            
            if len(numeric_columns) == 0:
                print("❌ Error: No numeric columns found")
                return False
            
            # Select only numeric features
            self.X_train = self.normal_data[numeric_columns].copy()
            self.feature_columns = numeric_columns
            
            print(f"✅ Numeric features selected!")
            print(f"   Number of numeric features: {len(numeric_columns)}")
            print(f"   Feature names: {numeric_columns[:10]}{'...' if len(numeric_columns) > 10 else ''}")
            
            # Check for missing values
            missing_count = self.X_train.isnull().sum().sum()
            if missing_count > 0:
                print(f"   ⚠️ Found {missing_count} missing values - will fill with 0")
                self.X_train = self.X_train.fillna(0)
            else:
                print(f"   ✅ No missing values found")
            
            return True
            
        except Exception as e:
            print(f"❌ Error selecting numeric features: {e}")
            return False
    
    def scale_features(self):
        """
        Apply StandardScaler to normalize features
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("\n📏 Scaling features with StandardScaler...")
            
            # Initialize and fit scaler on normal traffic
            self.scaler = StandardScaler()
            self.X_train_scaled = self.scaler.fit_transform(self.X_train)
            
            print(f"✅ Features scaled successfully!")
            print(f"   Scaled data shape: {self.X_train_scaled.shape}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error scaling features: {e}")
            return False
    
    def train_model(self):
        """
        Train Isolation Forest on normal traffic only
        
        Parameters:
            - n_estimators: 1500
            - max_features: 0.8
            - contamination: "auto"
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("\n🌲 Training Isolation Forest on normal traffic...")
            print("   Parameters:")
            print("     - n_estimators: 1500")
            print("     - max_features: 0.8")
            print("     - contamination: 'auto'")
            
            # Train Isolation Forest
            self.model = IsolationForest(
                n_estimators=1500,
                max_features=0.8,
                contamination='auto',  # Let model determine contamination rate
                random_state=42,
                n_jobs=-1,  # Use all CPU cores
                bootstrap=True,
                warm_start=False
            )
            
            # Fit on normal traffic only
            print("   Training in progress...")
            self.model.fit(self.X_train_scaled)
            
            print(f"✅ Model trained successfully!")
            print(f"   Training samples: {len(self.X_train_scaled):,}")
            print(f"   Features used: {len(self.feature_columns)}")
            
            # Store training statistics
            self.training_stats = {
                'n_estimators': 1500,
                'max_features': 0.8,
                'contamination': 'auto',
                'training_samples': len(self.X_train_scaled),
                'n_features': len(self.feature_columns),
                'feature_columns': self.feature_columns,
                'training_date': datetime.now().isoformat()
            }
            
            return True
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_model(self):
        """
        Save trained model and scaler using joblib
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("\n💾 Saving model and scaler...")
            
            # Save Isolation Forest model
            model_path = 'ml_models/isolationforest_normal_only_model.pkl'
            joblib.dump(self.model, model_path)
            print(f"   ✅ Model saved: {model_path}")
            
            # Save scaler
            scaler_path = 'ml_models/isolationforest_normal_only_scaler.pkl'
            joblib.dump(self.scaler, scaler_path)
            print(f"   ✅ Scaler saved: {scaler_path}")
            
            # Save feature columns
            feature_path = 'ml_models/isolationforest_normal_only_features.json'
            with open(feature_path, 'w') as f:
                json.dump(self.feature_columns, f, indent=2)
            print(f"   ✅ Feature columns saved: {feature_path}")
            
            # Save training statistics
            stats_path = 'ml_results/isolationforest_normal_only_stats.json'
            with open(stats_path, 'w') as f:
                json.dump(self.training_stats, f, indent=2)
            print(f"   ✅ Training stats saved: {stats_path}")
            
            print(f"\n✅ All files saved successfully!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving model: {e}")
            return False
    
    def run_training(self, file_path):
        """
        Run complete training pipeline
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("=" * 60)
        print("🌲 Isolation Forest Training - Normal Traffic Only")
        print("=" * 60)
        
        try:
            # Step 1: Load data
            if not self.load_data(file_path):
                return False
            
            # Step 2: Filter normal traffic
            if not self.filter_normal_traffic():
                return False
            
            # Step 3: Select numeric features
            if not self.select_numeric_features():
                return False
            
            # Step 4: Scale features
            if not self.scale_features():
                return False
            
            # Step 5: Train model
            if not self.train_model():
                return False
            
            # Step 6: Save model
            if not self.save_model():
                return False
            
            print("\n" + "=" * 60)
            print("🎉 Training completed successfully!")
            print("=" * 60)
            print("\n📁 Saved files:")
            print("   - ml_models/isolationforest_normal_only_model.pkl")
            print("   - ml_models/isolationforest_normal_only_scaler.pkl")
            print("   - ml_models/isolationforest_normal_only_features.json")
            print("   - ml_results/isolationforest_normal_only_stats.json")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Training pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point - user selects file manually"""
    print("🌲 Isolation Forest Training - Normal Traffic Only")
    print("=" * 60)
    print("\nPlease provide the path to your CSV file.")
    print("The file should contain a 'label' column (0=normal, 1=attack)")
    
    # Get file path from user
    file_path = input("\nEnter CSV file path: ").strip().strip('"').strip("'")
    
    if not file_path:
        print("❌ No file path provided")
        return
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    # Initialize trainer
    trainer = IsolationForestNormalOnlyTrainer()
    
    # Run training
    success = trainer.run_training(file_path)
    
    if success:
        print("\n✅ Training completed! You can now use the inference code.")
    else:
        print("\n❌ Training failed. Please check the error messages above.")


if __name__ == "__main__":
    main()


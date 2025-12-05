#!/usr/bin/env python3
"""
Isolation Forest Inference - Anomaly Detection
Loads trained model and scaler to predict anomalies on new data
"""

import pandas as pd
import numpy as np
import joblib
import json
import os

class IsolationForestInference:
    def __init__(self, model_path='ml_models/isolationforest_normal_only_model.pkl',
                 scaler_path='ml_models/isolationforest_normal_only_scaler.pkl',
                 features_path='ml_models/isolationforest_normal_only_features.json'):
        """
        Initialize inference with trained model and scaler
        
        Args:
            model_path: Path to saved Isolation Forest model
            scaler_path: Path to saved StandardScaler
            features_path: Path to saved feature columns JSON
        """
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.features_path = features_path
        self.model = None
        self.scaler = None
        self.feature_columns = []
        
        # Load model, scaler, and feature columns
        self.load_model()
    
    def load_model(self):
        """Load trained model, scaler, and feature columns"""
        try:
            print("📂 Loading model and scaler...")
            
            # Check if files exist
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            if not os.path.exists(self.scaler_path):
                raise FileNotFoundError(f"Scaler file not found: {self.scaler_path}")
            if not os.path.exists(self.features_path):
                raise FileNotFoundError(f"Features file not found: {self.features_path}")
            
            # Load model
            self.model = joblib.load(self.model_path)
            print(f"   ✅ Model loaded: {self.model_path}")
            
            # Load scaler
            self.scaler = joblib.load(self.scaler_path)
            print(f"   ✅ Scaler loaded: {self.scaler_path}")
            
            # Load feature columns
            with open(self.features_path, 'r') as f:
                self.feature_columns = json.load(f)
            print(f"   ✅ Feature columns loaded: {len(self.feature_columns)} features")
            
            print("✅ All components loaded successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def preprocess_data(self, data):
        """
        Preprocess input data: select numeric features and scale
        
        Args:
            data: DataFrame or array-like input data
            
        Returns:
            numpy array: Preprocessed and scaled data
        """
        try:
            # Convert to DataFrame if needed
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            
            # Remove label columns if present (not used for prediction)
            columns_to_drop = ['label', 'attack_cat', 'id']
            for col in columns_to_drop:
                if col in data.columns:
                    data = data.drop(columns=[col])
            
            # Select only the features used during training
            missing_features = set(self.feature_columns) - set(data.columns)
            if missing_features:
                print(f"⚠️ Warning: Missing features: {missing_features}")
                print(f"   Available features: {list(data.columns)}")
                # Use only available features
                available_features = [f for f in self.feature_columns if f in data.columns]
                if len(available_features) == 0:
                    raise ValueError("No matching features found!")
                data = data[available_features]
            else:
                data = data[self.feature_columns]
            
            # Fill missing values with 0
            data = data.fillna(0)
            
            # Convert to numeric (in case of string values)
            for col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
            data = data.fillna(0)
            
            # Scale using the same scaler from training
            data_scaled = self.scaler.transform(data)
            
            return data_scaled
            
        except Exception as e:
            print(f"❌ Error preprocessing data: {e}")
            raise
    
    def predict(self, data):
        """
        Predict anomalies on new data
        
        Args:
            data: DataFrame or array-like input data
            
        Returns:
            numpy array: Predictions (-1 for anomaly, 1 for normal)
        """
        try:
            # Preprocess data
            data_scaled = self.preprocess_data(data)
            
            # Make predictions
            predictions = self.model.predict(data_scaled)
            
            return predictions
            
        except Exception as e:
            print(f"❌ Error making predictions: {e}")
            raise
    
    def predict_with_scores(self, data):
        """
        Predict anomalies with decision scores
        
        Args:
            data: DataFrame or array-like input data
            
        Returns:
            tuple: (predictions, scores)
                - predictions: -1 for anomaly, 1 for normal
                - scores: Decision scores (lower = more anomalous)
        """
        try:
            # Preprocess data
            data_scaled = self.preprocess_data(data)
            
            # Get predictions
            predictions = self.model.predict(data_scaled)
            
            # Get decision scores
            scores = self.model.decision_function(data_scaled)
            
            return predictions, scores
            
        except Exception as e:
            print(f"❌ Error making predictions: {e}")
            raise
    
    def analyze_predictions(self, predictions):
        """
        Analyze prediction results and print statistics
        
        Args:
            predictions: Array of predictions (-1 for anomaly, 1 for normal)
        """
        predictions = np.array(predictions)
        
        # Count anomalies and normal
        anomalies = np.sum(predictions == -1)
        normal = np.sum(predictions == 1)
        total = len(predictions)
        
        # Calculate ratios
        anomaly_ratio = (anomalies / total) * 100 if total > 0 else 0
        normal_ratio = (normal / total) * 100 if total > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 Prediction Analysis")
        print("=" * 60)
        print(f"Total samples: {total:,}")
        print(f"Anomalies detected: {anomalies:,} ({anomaly_ratio:.2f}%)")
        print(f"Normal samples: {normal:,} ({normal_ratio:.2f}%)")
        print("=" * 60)
        
        return {
            'total': total,
            'anomalies': int(anomalies),
            'normal': int(normal),
            'anomaly_ratio': float(anomaly_ratio),
            'normal_ratio': float(normal_ratio)
        }


def predict_anomalies(data, model_path=None, scaler_path=None, features_path=None):
    """
    Convenience function to predict anomalies
    
    Args:
        data: DataFrame or array-like input data
        model_path: Optional path to model (uses default if None)
        scaler_path: Optional path to scaler (uses default if None)
        features_path: Optional path to features (uses default if None)
    
    Returns:
        numpy array: Predictions (-1 for anomaly, 1 for normal)
    """
    # Initialize inference
    if model_path is None:
        inference = IsolationForestInference()
    else:
        inference = IsolationForestInference(model_path, scaler_path, features_path)
    
    # Make predictions
    predictions = inference.predict(data)
    
    # Analyze and print results
    inference.analyze_predictions(predictions)
    
    return predictions


def main():
    """Example usage"""
    print("🔍 Isolation Forest Inference - Anomaly Detection")
    print("=" * 60)
    
    # Initialize inference
    inference = IsolationForestInference()
    
    if inference.model is None:
        print("❌ Failed to load model. Please train the model first.")
        return
    
    # Example: Load test data
    print("\n📊 Example: Testing on data...")
    print("   (In real usage, load your test CSV file)")
    
    # Get file path from user
    file_path = input("\nEnter CSV file path for prediction (or press Enter to skip): ").strip().strip('"').strip("'")
    
    if file_path and os.path.exists(file_path):
        try:
            # Load data
            print(f"\n📂 Loading data from: {file_path}")
            test_data = pd.read_csv(file_path)
            print(f"   Loaded {len(test_data):,} rows")
            
            # Make predictions
            print("\n🔍 Making predictions...")
            predictions = inference.predict(test_data)
            
            # Analyze results
            stats = inference.analyze_predictions(predictions)
            
            # Optionally get scores
            print("\n📈 Getting detailed scores...")
            predictions_with_scores, scores = inference.predict_with_scores(test_data)
            
            print(f"\n   Decision scores range: [{scores.min():.4f}, {scores.max():.4f}]")
            print(f"   Lower scores = more anomalous")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n💡 Usage example:")
        print("""
# Load your data
import pandas as pd
from ml_isolation_forest_inference import predict_anomalies

data = pd.read_csv('your_test_data.csv')
predictions = predict_anomalies(data)

# predictions: -1 = anomaly, 1 = normal
        """)


if __name__ == "__main__":
    main()


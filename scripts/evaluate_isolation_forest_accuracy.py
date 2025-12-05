#!/usr/bin/env python3
"""
Evaluate Isolation Forest Model Accuracy
Compares predictions with actual labels to calculate accuracy
"""

import pandas as pd
import numpy as np
from ml_isolation_forest_inference import IsolationForestInference
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os

def evaluate_accuracy(test_file_path):
    """
    Evaluate Isolation Forest model accuracy on test dataset
    
    Args:
        test_file_path: Path to test CSV file with labels
    """
    print("=" * 60)
    print("📊 Evaluating Isolation Forest Model Accuracy")
    print("=" * 60)
    
    # Load test data
    print(f"\n📂 Loading test data from: {test_file_path}")
    test_data = pd.read_csv(test_file_path)
    print(f"   Total samples: {len(test_data):,}")
    
    # Check if label column exists
    if 'label' not in test_data.columns:
        print("❌ Error: 'label' column not found in test data")
        return
    
    # Get actual labels
    y_true = test_data['label'].values  # 0 = normal, 1 = attack
    print(f"   Normal samples (label=0): {np.sum(y_true == 0):,}")
    print(f"   Attack samples (label=1): {np.sum(y_true == 1):,}")
    
    # Initialize inference
    print("\n🔍 Loading model and making predictions...")
    inference = IsolationForestInference()
    
    if inference.model is None:
        print("❌ Failed to load model")
        return
    
    # Make predictions
    predictions = inference.predict(test_data)
    
    # Convert Isolation Forest predictions to match label format
    # Isolation Forest: -1 = anomaly, 1 = normal
    # Our labels: 0 = normal, 1 = attack
    # So: -1 (anomaly) → 1 (attack), 1 (normal) → 0 (normal)
    y_pred = (predictions == -1).astype(int)  # -1 becomes 1 (attack), 1 becomes 0 (normal)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_true, y_pred)
    
    # Calculate other metrics
    from sklearn.metrics import precision_score, recall_score, f1_score
    
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Print results
    print("\n" + "=" * 60)
    print("📈 Accuracy Results")
    print("=" * 60)
    print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
    
    print("\n" + "=" * 60)
    print("📊 Confusion Matrix")
    print("=" * 60)
    print("                Predicted")
    print("              Normal  Attack")
    print(f"Actual Normal   {cm[0][0]:6d}  {cm[0][1]:6d}")
    print(f"       Attack    {cm[1][0]:6d}  {cm[1][1]:6d}")
    
    # Calculate per-class accuracy
    normal_accuracy = cm[0][0] / (cm[0][0] + cm[0][1]) if (cm[0][0] + cm[0][1]) > 0 else 0
    attack_accuracy = cm[1][1] / (cm[1][0] + cm[1][1]) if (cm[1][0] + cm[1][1]) > 0 else 0
    
    print("\n" + "=" * 60)
    print("📋 Per-Class Accuracy")
    print("=" * 60)
    print(f"Normal Traffic Accuracy: {normal_accuracy:.4f} ({normal_accuracy*100:.2f}%)")
    print(f"Attack Traffic Accuracy:  {attack_accuracy:.4f} ({attack_accuracy*100:.2f}%)")
    
    # Classification report
    print("\n" + "=" * 60)
    print("📄 Detailed Classification Report")
    print("=" * 60)
    report = classification_report(y_true, y_pred, target_names=['Normal', 'Attack'], output_dict=False)
    print(report)
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Evaluation Complete")
    print("=" * 60)
    print(f"\n🎯 Overall Accuracy: {accuracy*100:.2f}%")
    print(f"   This model correctly classifies {accuracy*100:.2f}% of all samples")
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'normal_accuracy': normal_accuracy,
        'attack_accuracy': attack_accuracy,
        'confusion_matrix': cm.tolist()
    }

if __name__ == "__main__":
    # Test file path
    test_file = os.path.join('csv', 'CSV Files', 'Training and Testing Sets', 'UNSW_NB15_testing-set.csv')
    
    if os.path.exists(test_file):
        results = evaluate_accuracy(test_file)
    else:
        print(f"❌ Test file not found: {test_file}")
        print("Please provide the path to your test CSV file")


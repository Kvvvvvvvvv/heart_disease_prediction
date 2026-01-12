"""
LEAK-FREE TRAINING PIPELINE
✅ Proper train-test split BEFORE scaling
✅ Pipeline for clean preprocessing
✅ Stratified split for balanced classes
✅ Feature importance extraction
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib
import json

print("=" * 60)
print("LEAK-FREE TRAINING PIPELINE")
print("=" * 60)

# Load data
print("\n1. Loading data...")
df = pd.read_csv("data/heart-disease-UCI.csv")

# ✅ CORRECT FEATURE SPLIT (EXCLUDE TARGET)
print("\n2. Preparing features and target...")
X = df.drop("target", axis=1)
y = df["target"]  # Use Series for stratify

print(f"   Features shape: {X.shape}")
print(f"   Target distribution:\n{y.value_counts()}")

# ✅ STRATIFIED SPLIT (BEFORE ANY SCALING)
print("\n3. Creating stratified train-test split...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    stratify=y,  # Maintain class distribution
    random_state=42
)

print(f"   Train set: {X_train.shape[0]} samples")
print(f"   Test set: {X_test.shape[0]} samples")

# ✅ PIPELINE (SCALING ONLY WHERE NEEDED)
print("\n4. Creating pipeline with scaling and model...")
pipeline = Pipeline([
    ("scaler", StandardScaler()),  # Scaling happens INSIDE pipeline
    ("model", RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    ))
])

# Fit pipeline (scaling happens on training data only)
print("\n5. Training model...")
pipeline.fit(X_train, y_train)

# Predictions
print("\n6. Making predictions...")
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

# Evaluation
print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

roc_auc = roc_auc_score(y_test, y_prob)
print(f"\nROC AUC Score: {roc_auc:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(f"\nConfusion Matrix:")
print(cm)

# ✅ FEATURE IMPORTANCE EXTRACTION
print("\n" + "=" * 60)
print("FEATURE IMPORTANCE")
print("=" * 60)

model = pipeline.named_steps["model"]
feature_names = X.columns
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

print("\nTop 10 Most Important Features:")
for i in range(min(10, len(feature_names))):
    idx = indices[i]
    print(f"{i+1:2d}. {feature_names[idx]:15s} : {importances[idx]:.4f}")

# Save feature importance plot
print("\n7. Creating feature importance visualization...")
plt.figure(figsize=(12, 8))
top_n = min(10, len(feature_names))
plt.barh(range(top_n), importances[indices][:top_n][::-1])
plt.yticks(range(top_n), [feature_names[indices[i]] for i in range(top_n-1, -1, -1)])
plt.xlabel("Feature Importance")
plt.title("Top 10 Feature Importances (Random Forest)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("feature_importance.png", dpi=150, bbox_inches='tight')
print("   Saved: feature_importance.png")

# Save model and metadata
print("\n8. Saving model and metadata...")
joblib.dump(pipeline, "heart_disease_model.pkl")
print("   Saved: heart_disease_model.pkl")

# Save feature names
with open("feature_names.json", "w") as f:
    json.dump(list(feature_names), f)
print("   Saved: feature_names.json")

# Save feature importances
feature_importance_dict = {
    "feature_names": list(feature_names),
    "importances": importances.tolist(),
    "sorted_indices": indices.tolist()
}
with open("feature_importances.json", "w") as f:
    json.dump(feature_importance_dict, f, indent=2)
print("   Saved: feature_importances.json")

# Save model metrics
metrics = {
    "roc_auc": float(roc_auc),
    "test_accuracy": float((y_pred == y_test).mean()),
    "n_features": int(len(feature_names)),
    "n_train_samples": int(len(X_train)),
    "n_test_samples": int(len(X_test))
}
with open("model_metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)
print("   Saved: model_metrics.json")

print("\n" + "=" * 60)
print("TRAINING COMPLETE!")
print("=" * 60)
print("\nModel is ready for deployment.")
print("Run 'streamlit run app.py' to start the web app.")

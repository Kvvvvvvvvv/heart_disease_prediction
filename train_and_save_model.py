"""
Train and save the heart disease prediction model
Run this once to create the model file
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
import joblib

print("Loading data...")
# Load data
df = pd.read_csv("data/heart-disease-UCI.csv")

# Prepare data
X = df.drop("target", axis=1)
y = df.target.values

# Split data
np.random.seed(42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("Training model with hyperparameter tuning...")
# Hyperparameter grid
log_reg_grid = {"C": np.logspace(-4, 4, 20),
                "solver": ["liblinear"]}

# Grid search for best parameters
gs_log_reg = GridSearchCV(LogisticRegression(),
                          param_grid=log_reg_grid,
                          cv=5,
                          verbose=False)

# Fit the model
gs_log_reg.fit(X_train, y_train)

print(f"Best parameters: {gs_log_reg.best_params_}")
print(f"Test accuracy: {gs_log_reg.score(X_test, y_test):.2%}")

# Train final model with best parameters
final_model = LogisticRegression(C=gs_log_reg.best_params_['C'],
                                 solver=gs_log_reg.best_params_['solver'])
final_model.fit(X_train, y_train)

# Save the model
model_filename = "heart_disease_model.pkl"
joblib.dump(final_model, model_filename)
print(f"\nModel saved as '{model_filename}'")

# Save feature names for reference
feature_names = list(X.columns)
import json
with open("feature_names.json", "w") as f:
    json.dump(feature_names, f)
print(f"Feature names saved as 'feature_names.json'")

print("\nModel training complete! You can now use the web app.")

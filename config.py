"""
Configuration settings for Heart Disease Prediction Application
"""

import os
from pathlib import Path

# Application Configuration
APP_NAME = "Heart Disease Prediction System"
VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "models"
SRC_DIR = BASE_DIR / "src"

# Model Configuration
MODEL_PATH = DATA_DIR / "heart_disease_model.pkl"
FEATURE_NAMES_PATH = DATA_DIR / "feature_names.json"
FEATURE_IMPORTANCES_PATH = DATA_DIR / "feature_importances.json"
MODEL_METRICS_PATH = DATA_DIR / "model_metrics.json"

# Data Configuration
DATASET_PATH = DATA_DIR / "heart-disease-UCI.csv"

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# API Configuration (if applicable)
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8501"))
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Feature names for validation
FEATURE_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 
    'fbs', 'restecg', 'thalach', 'exang', 
    'oldpeak', 'slope', 'ca', 'thal'
]

# Feature ranges for validation
FEATURE_RANGES = {
    'age': (1, 120),
    'sex': (0, 1),
    'cp': (0, 3),
    'trestbps': (50, 250),
    'chol': (100, 600),
    'fbs': (0, 1),
    'restecg': (0, 2),
    'thalach': (60, 220),
    'exang': (0, 1),
    'oldpeak': (0.0, 10.0),
    'slope': (0, 2),
    'ca': (0, 3),
    'thal': (0, 3)
}
# Heart Disease Prediction System (ML + Clinical Explainability)

A comprehensive heart disease risk prediction system built using machine learning, enhanced with explainability, document-based clinical input, and optional 3D visualization for risk interpretation.

This project goes beyond a basic UCI dataset classifier by integrating:
- Leak-free ML training
- Clinical-style explanations
- DOCX-based patient data ingestion
- Optional LLM-assisted reasoning (via Ollama)
- Web and Streamlit interfaces
- Experimental 3D heart risk visualization (non-diagnostic)

---

## 📌 Key Objectives

- Predict the **presence of heart disease** using structured clinical attributes
- Maintain **data leakage safety** during training
- Provide **explainable predictions** suitable for academic and demo purposes
- Enable **multiple interaction modes** (CLI, Web, Streamlit)
- Avoid generating diagnoses or patient-specific anatomy

> ⚠️ This project is **educational and research-oriented only**.  
> It must **not** be used for real clinical decision-making.

---

## 📊 Dataset

- **Source**: UCI Heart Disease Dataset  
- **Features include**:
  - Age
  - Sex
  - Chest pain type
  - Resting blood pressure
  - Cholesterol
  - Fasting blood sugar
  - Resting ECG
  - Max heart rate
  - Exercise-induced angina
  - ST depression
  - Slope, vessels, thalassemia

- **Target**: Presence / absence of heart disease

---

## 🧠 Machine Learning Pipeline

1. Data cleaning & validation
2. Categorical encoding & normalization
3. Leak-free train/test split
4. Model training (Random Forest / Logistic Regression)
5. Cross-validation
6. Metric evaluation (accuracy, precision, recall, F1)
7. Feature importance extraction
8. Model serialization (`.pkl`)

Relevant files:
- `train_model_leak_free.py`
- `train_and_save_model.py`
- `heart_disease_model.pkl`
- `model_metrics.json`
- `feature_importances.json`

---

## 🧾 DOCX-Based Clinical Input (Experimental)

This project supports structured `.docx` uploads representing patient summaries.

Supported files:
- `DOCX_UPLOAD_GUIDE.md`
- `DOCX_FEATURE_SUMMARY.md`
- `docx_parser.py`

Purpose:
- Simulate clinical report ingestion
- Map text fields → ML features
- Improve realism for demos & research

---

## 🌐 Application Interfaces

### 1️⃣ Flask Web App
- File: `app.py`
- Enhanced version: `app_enhanced.py`
- Entry points:
  - `run_project.py`
  - `start_web_app.bat`

### 2️⃣ Streamlit Interface
- File: `run_streamlit.py`
- Fast UI for model testing & visualization

### 3️⃣ CLI Mode
- File: `run_heart_disease.py`
- For quick local predictions

---

## 🧠 Explainability & LLM Integration (Optional)

- Local LLM support via **Ollama**
- Generates:
  - Human-readable explanations
  - Feature-driven reasoning summaries

Files:
- `ollama_integration.py`
- `ollama_integration_improved.py`
- `OLLAMA_SETUP.md`

> This is **assistive reasoning**, not medical advice.

---

## 🫀 3D Risk Visualization (Non-Diagnostic)

Experimental 3D heart visualization to represent **risk intensity**, NOT anatomy.

Files:
- `visualization_3d.py`
- `visualization_3d_fixed.py`
- `visualization_3d_realistic.py`
- `REALISTIC_3D_UPDATE.md`

⚠️ The visualization:
- Does NOT generate patient-specific heart structures
- Is metaphorical, not clinical imaging

---
>>>>>>> 79f7ad13a62bbbc0b1cea5589d657d37c972cc0e
# Heart Disease Prediction System

A comprehensive machine learning application for predicting heart disease risk based on patient medical attributes. Features an interactive web interface with 3D visualization, clinical explanations, and model interpretability.

## 🚀 Features

- **Machine Learning Model**: Random Forest classifier with leak-free pipeline
- **Interactive Web Interface**: Built with Streamlit
- **3D Heart Visualization**: Realistic 3D heart model with risk mapping
- **Clinical Decision Support**: Ollama-powered clinical explanations
- **Feature Importance**: Model interpretability and insights
- **Document Parsing**: DOCX patient data import capability
- **Model Performance**: ~85% accuracy, ~0.91 ROC AUC

## 📋 Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

## 🛠️ Installation & Setup

### Method 1: Local Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd heart-disease-prediction
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Train the model (if not already present):
   ```bash
   python src/models/train_model_leak_free.py
   ```

5. Run the application:
   ```bash
   streamlit run src/app/app_enhanced.py
   ```

### Method 2: Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t heart-disease-prediction .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 heart-disease-prediction
   ```

## 📁 Project Structure

```
heart-disease-prediction/
├── src/                    # Source code
│   ├── app/                # Application files
│   │   ├── app.py          # Basic Streamlit app
│   │   └── app_enhanced.py # Enhanced app with all features
│   ├── models/             # Model training and management
│   │   ├── train_model_leak_free.py
│   │   └── train_and_save_model.py
│   └── utils/              # Utility functions
│       ├── docx_parser.py
│       ├── ollama_integration.py
│       ├── visualization_3d.py
│       └── ...             # Other utilities
├── data/                   # Data files and models
├── docs/                   # Documentation
├── tests/                  # Test files
├── config.py               # Configuration settings
├── Dockerfile              # Container configuration
├── requirements.txt        # Dependencies
└── README.md
```

## 🔧 Configuration

Environment variables can be set to customize the application:

- `API_HOST`: Host address (default: 0.0.0.0)
- `API_PORT`: Port number (default: 8501)
- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)

## 🧪 Running Tests

Execute the test suite:

```bash
python -m pytest tests/
```

## 🚢 Production Deployment

For production deployments, consider:

1. Using environment variables for configuration
2. Setting up a reverse proxy (nginx/Apache)
3. Implementing proper logging
4. Securing the application
5. Monitoring and alerting

## 🌐 Streamlit Sharing Deployment

The project includes a Streamlit-ready version for easy deployment on Streamlit Sharing:

1. The `streamlit_app/` directory contains a simplified version of the app that's optimized for Streamlit Sharing
2. Copy the model files (`heart_disease_model.pkl`, `feature_names.json`) to your repository
3. Deploy directly to Streamlit Sharing using the `streamlit_app/streamlit_app.py` file
4. The app will automatically locate model files in the repository

To deploy to Streamlit Sharing:
1. Fork this repository
2. Ensure model files are in the repository
3. Connect to Streamlit Sharing and point to `streamlit_app/streamlit_app.py`
4. The app will be automatically deployed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is intended for educational and research purposes only. It does not constitute medical advice and should not be used as a substitute for professional medical consultation. Always consult qualified healthcare professionals for medical decisions.
=======
# Heart Disease Prediction System (ML + Clinical Explainability)

A comprehensive heart disease risk prediction system built using machine learning, enhanced with explainability, document-based clinical input, and optional 3D visualization for risk interpretation.

This project goes beyond a basic UCI dataset classifier by integrating:
- Leak-free ML training
- Clinical-style explanations
- DOCX-based patient data ingestion
- Optional LLM-assisted reasoning (via Ollama)
- Web and Streamlit interfaces
- Experimental 3D heart risk visualization (non-diagnostic)

---

## 📌 Key Objectives

- Predict the **presence of heart disease** using structured clinical attributes
- Maintain **data leakage safety** during training
- Provide **explainable predictions** suitable for academic and demo purposes
- Enable **multiple interaction modes** (CLI, Web, Streamlit)
- Avoid generating diagnoses or patient-specific anatomy

> ⚠️ This project is **educational and research-oriented only**.  
> It must **not** be used for real clinical decision-making.

---

## 📊 Dataset

- **Source**: UCI Heart Disease Dataset  
- **Features include**:
  - Age
  - Sex
  - Chest pain type
  - Resting blood pressure
  - Cholesterol
  - Fasting blood sugar
  - Resting ECG
  - Max heart rate
  - Exercise-induced angina
  - ST depression
  - Slope, vessels, thalassemia

- **Target**: Presence / absence of heart disease

---

## 🧠 Machine Learning Pipeline

1. Data cleaning & validation
2. Categorical encoding & normalization
3. Leak-free train/test split
4. Model training (Random Forest / Logistic Regression)
5. Cross-validation
6. Metric evaluation (accuracy, precision, recall, F1)
7. Feature importance extraction
8. Model serialization (`.pkl`)

Relevant files:
- `train_model_leak_free.py`
- `train_and_save_model.py`
- `heart_disease_model.pkl`
- `model_metrics.json`
- `feature_importances.json`

---

## 🧾 DOCX-Based Clinical Input (Experimental)

This project supports structured `.docx` uploads representing patient summaries.

Supported files:
- `DOCX_UPLOAD_GUIDE.md`
- `DOCX_FEATURE_SUMMARY.md`
- `docx_parser.py`

Purpose:
- Simulate clinical report ingestion
- Map text fields → ML features
- Improve realism for demos & research

---

## 🌐 Application Interfaces

### 1️⃣ Flask Web App
- File: `app.py`
- Enhanced version: `app_enhanced.py`
- Entry points:
  - `run_project.py`
  - `start_web_app.bat`

### 2️⃣ Streamlit Interface
- File: `run_streamlit.py`
- Fast UI for model testing & visualization

### 3️⃣ CLI Mode
- File: `run_heart_disease.py`
- For quick local predictions

---

## 🧠 Explainability & LLM Integration (Optional)

- Local LLM support via **Ollama**
- Generates:
  - Human-readable explanations
  - Feature-driven reasoning summaries

Files:
- `ollama_integration.py`
- `ollama_integration_improved.py`
- `OLLAMA_SETUP.md`

> This is **assistive reasoning**, not medical advice.

---

## 🫀 3D Risk Visualization (Non-Diagnostic)

Experimental 3D heart visualization to represent **risk intensity**, NOT anatomy.

Files:
- `visualization_3d.py`
- `visualization_3d_fixed.py`
- `visualization_3d_realistic.py`
- `REALISTIC_3D_UPDATE.md`

⚠️ The visualization:
- Does NOT generate patient-specific heart structures
- Is metaphorical, not clinical imaging

---
>>>>>>> 79f7ad13a62bbbc0b1cea5589d657d37c972cc0e

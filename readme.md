# ❤️ Heart Disease Prediction System  
### Machine Learning with Clinical-Style Explainability

An educational and research-oriented heart disease risk prediction system built using machine learning.  
The project emphasizes **leak-free training**, **explainable outputs**, and **multiple interaction interfaces** (CLI, Web, Streamlit).


---

## 🎯 Project Goals

- Predict the **presence or absence of heart disease** using structured clinical features
- Ensure **data leakage prevention** during model training
- Provide **human-readable explanations** for predictions
- Support **multiple input & interaction modes**
- Experiment with **non-diagnostic visual metaphors** for risk interpretation

---

## 📊 Dataset

- **Source**: UCI Heart Disease Dataset  
- **Target Variable**: Presence of heart disease (binary classification)

### Input Features
- Age
- Sex
- Chest pain type
- Resting blood pressure
- Serum cholesterol
- Fasting blood sugar
- Resting ECG
- Maximum heart rate
- Exercise-induced angina
- ST depression
- Slope of ST segment
- Number of major vessels
- Thalassemia

---

## 🧠 Machine Learning Pipeline

1. Data cleaning and validation  
2. Encoding of categorical features  
3. Feature scaling and normalization  
4. Leak-free train/test split  
5. Model training (Logistic Regression / Random Forest)  
6. Cross-validation  
7. Model evaluation (Accuracy, Precision, Recall, F1-score)  
8. Feature importance extraction  
9. Model serialization  

### Core Files
- `train_model_leak_free.py`
- `train_and_save_model.py`
- `heart_disease_model.pkl`
- `model_metrics.json`
- `feature_importances.json`

---

## 🧾 DOCX-Based Clinical Input (Experimental)

Supports structured `.docx` files to simulate clinical summaries.

### Purpose
- Mimic clinical report ingestion
- Map structured text → ML features
- Improve realism for demos and research

### Files
- `docx_parser.py`
- `DOCX_UPLOAD_GUIDE.md`
- `DOCX_FEATURE_SUMMARY.md`

---

## 🌐 Application Interfaces

### 1️⃣ Flask Web Application
- `app.py`
- `app_enhanced.py`
- Launch helpers:
  - `run_project.py`
  - `start_web_app.bat`

### 2️⃣ Streamlit Application
- **Main File**: `streamlit_app.py`
- Provides:
  - Interactive UI
  - Model testing
  - Feature-based explanations

### 3️⃣ Command Line Interface (CLI)
- `run_heart_disease.py`
- Lightweight local predictions

---

## 🧠 Explainability & LLM Integration (Optional)

Optional integration with **Ollama (local LLM)** for explanation generation.

### Capabilities
- Feature-driven reasoning summaries
- Human-readable explanation text

### Files
- `ollama_integration.py`
- `ollama_integration_improved.py`
- `OLLAMA_SETUP.md`

⚠️ LLM output is **assistive reasoning only**, not medical advice.

---

## 🫀 3D Risk Visualization (Experimental)

A metaphorical 3D heart visualization to represent **risk intensity**, not anatomy.

### Characteristics
- Non-diagnostic
- No patient-specific heart structures
- Visual metaphor only

### Files
- `visualization_3d.py`
- `visualization_3d_fixed.py`
- `visualization_3d_realistic.py`
- `REALISTIC_3D_UPDATE.md`

---

## 🚀 Deployment Notes (Streamlit)

- Platform: **Streamlit Community Cloud**
- Branch: `main`
- Main file path:

- App auto-redeploys on every GitHub push

---

## ⚠️ Disclaimer

This project is strictly for:
- Education
- Academic demonstrations
- Research experimentation

It **must NOT** be used for:
- Clinical diagnosis
- Medical decision-making
- Patient treatment

---

## 👤 Author

Developed for academic and research exploration in:
- Machine Learning
- Explainable AI
- Health informatics (non-clinical)

---

## 📜 License

For educational and research use only.


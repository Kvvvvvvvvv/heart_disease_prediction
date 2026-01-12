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

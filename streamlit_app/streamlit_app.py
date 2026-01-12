import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide"
)

# Title and description
st.title("❤️ Heart Disease Prediction System")
st.markdown("""
This application uses a machine learning model to predict the presence of heart disease based on patient medical attributes.
**Please enter the patient's information below to get a prediction.**
""")

# Define the path to the data directory
@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        # Look for model files in both root and data directories
        model_path = None
        feature_names_path = None
        
        possible_model_paths = [
            "heart_disease_model.pkl",
            "./heart_disease_model.pkl",
            "../heart_disease_model.pkl",
            "./data/heart_disease_model.pkl",
            "../data/heart_disease_model.pkl"
        ]
        
        possible_feature_paths = [
            "feature_names.json",
            "./feature_names.json",
            "../feature_names.json",
            "./data/feature_names.json",
            "../data/feature_names.json"
        ]
        
        for path in possible_model_paths:
            if os.path.exists(path):
                model_path = path
                break
                
        for path in possible_feature_paths:
            if os.path.exists(path):
                feature_names_path = path
                break
        
        if model_path is None or feature_names_path is None:
            st.error("⚠️ Model files not found! Please ensure 'heart_disease_model.pkl' and 'feature_names.json' are in the project directory.")
            st.stop()
        
        model = joblib.load(model_path)
        with open(feature_names_path, "r") as f:
            feature_names = json.load(f)
        return model, feature_names
    except Exception as e:
        st.error(f"⚠️ Error loading model: {str(e)}")
        st.stop()

model, feature_names = load_model()

# Sidebar with information
with st.sidebar:
    st.header("📋 Feature Information")
    st.markdown("""
    **1. Age**: Patient's age in years
    
    **2. Sex**: 
    - 0 = Female
    - 1 = Male
    
    **3. Chest Pain Type (cp)**:
    - 0 = Typical angina
    - 1 = Atypical angina
    - 2 = Non-anginal pain
    - 3 = Asymptomatic
    
    **4. Resting Blood Pressure**: In mm Hg
    
    **5. Cholesterol**: Serum cholesterol in mg/dL
    
    **6. Fasting Blood Sugar (fbs)**:
    - 0 = ≤ 120 mg/dL
    - 1 = > 120 mg/dL
    
    **7. Resting ECG (restecg)**:
    - 0 = Normal
    - 1 = ST-T wave abnormality
    - 2 = Left ventricular hypertrophy
    
    **8. Max Heart Rate**: Maximum heart rate achieved
    
    **9. Exercise Angina (exang)**:
    - 0 = No
    - 1 = Yes
    
    **10. ST Depression (oldpeak)**: ST depression induced by exercise
    
    **11. Slope**: Slope of peak exercise ST segment
    - 0 = Upsloping
    - 1 = Flat
    - 2 = Downsloping
    
    **12. Major Vessels (ca)**: Number of major vessels (0-3)
    
    **13. Thalassemia (thal)**:
    - 1 = Normal
    - 2 = Fixed defect
    - 3 = Reversible defect
    """)

# Main form
st.header("Patient Information Form")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
    sex = st.selectbox("Sex", options=[("Female", 0), ("Male", 1)], format_func=lambda x: x[0])[1]
    cp = st.selectbox("Chest Pain Type", 
                      options=[("Typical Angina", 0), ("Atypical Angina", 1), 
                              ("Non-anginal Pain", 2), ("Asymptomatic", 3)],
                      format_func=lambda x: x[0])[1]
    trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120)
    chol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=600, value=200)
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", 
                       options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])[1]
    restecg = st.selectbox("Resting ECG Results",
                           options=[("Normal", 0), ("ST-T Wave Abnormality", 1), 
                                   ("Left Ventricular Hypertrophy", 2)],
                           format_func=lambda x: x[0])[1]

with col2:
    thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150)
    exang = st.selectbox("Exercise Induced Angina",
                         options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0])[1]
    oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    slope = st.selectbox("Slope of Peak Exercise ST Segment",
                        options=[("Upsloping", 0), ("Flat", 1), ("Downsloping", 2)],
                        format_func=lambda x: x[0])[1]
    ca = st.number_input("Number of Major Vessels (0-3)", min_value=0, max_value=3, value=0)
    thal = st.selectbox("Thalassemia",
                       options=[("Normal", 1), ("Fixed Defect", 2), ("Reversible Defect", 3)],
                       format_func=lambda x: x[0])[1]

# Prediction button
st.markdown("---")
if st.button("🔍 Predict Heart Disease", type="primary", use_container_width=True):
    # Prepare input data
    input_data = pd.DataFrame({
        'age': [age],
        'sex': [sex],
        'cp': [cp],
        'trestbps': [trestbps],
        'chol': [chol],
        'fbs': [fbs],
        'restecg': [restecg],
        'thalach': [thalach],
        'exang': [exang],
        'oldpeak': [oldpeak],
        'slope': [slope],
        'ca': [ca],
        'thal': [thal]
    })
    
    # Ensure correct column order
    input_data = input_data[feature_names]
    
    # Make prediction
    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]
    
    # Display results
    st.markdown("---")
    st.header("📊 Prediction Results")
    
    # Result boxes
    result_col1, result_col2 = st.columns(2)
    
    with result_col1:
        if prediction == 1:
            st.error("⚠️ **Heart Disease Detected**")
            st.markdown("The model predicts that this patient **has heart disease**.")
        else:
            st.success("✅ **No Heart Disease Detected**")
            st.markdown("The model predicts that this patient **does not have heart disease**.")
    
    with result_col2:
        st.metric("Risk Score", f"{prediction_proba[1]*100:.1f}%")
        st.markdown(f"""
        - **No Disease**: {prediction_proba[0]*100:.1f}%
        - **Has Disease**: {prediction_proba[1]*100:.1f}%
        """)
    
    # Warning
    st.info("⚠️ **Disclaimer**: This is a machine learning prediction tool for educational purposes only. "
            "Always consult with qualified healthcare professionals for medical diagnosis and treatment.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Heart Disease Prediction System | Built with Streamlit & Scikit-Learn</p>
</div>
""", unsafe_allow_html=True)
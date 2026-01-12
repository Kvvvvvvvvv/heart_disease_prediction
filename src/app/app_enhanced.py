"""
Enhanced Heart Disease Prediction Web App
Features:
- Leak-free ML pipeline
- Feature importance visualization
- 3D heart visualization with risk mapping
- Ollama-powered clinical explanations
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
from ..utils.visualization_3d_fixed import create_realistic_3d_heart_html, get_risk_level
from ..utils.ollama_integration_improved import OllamaClinicalAssistant
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from ..utils.docx_parser import PatientDataParser
import io

# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction System",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("❤️ Heart Disease Prediction System")
st.markdown("""
**Advanced ML-powered cardiovascular risk assessment with 3D visualization and clinical decision support**

This application uses a leak-free machine learning pipeline to predict heart disease risk based on patient medical attributes.
""")

# Load model and metadata
@st.cache_resource
def load_model():
    """Load the trained model and metadata"""
    try:
        pipeline = joblib.load("heart_disease_model.pkl")
        with open("feature_names.json", "r") as f:
            feature_names = json.load(f)
        with open("feature_importances.json", "r") as f:
            feature_importances = json.load(f)
        with open("model_metrics.json", "r") as f:
            metrics = json.load(f)
        return pipeline, feature_names, feature_importances, metrics
    except FileNotFoundError as e:
        st.error(f"⚠️ Model files not found! Please run 'python train_model_leak_free.py' first.")
        st.error(f"Missing: {e}")
        st.stop()

pipeline, feature_names, feature_importances, metrics = load_model()

# Initialize Ollama assistant
ollama_assistant = OllamaClinicalAssistant()

# Sidebar
with st.sidebar:
    st.header("📋 Feature Information")
    st.markdown("""
    **1. Age**: Patient's age in years
    
    **2. Sex**: 
    - 0 = Female, 1 = Male
    
    **3. Chest Pain Type (cp)**:
    - 0 = Typical angina
    - 1 = Atypical angina
    - 2 = Non-anginal pain
    - 3 = Asymptomatic
    
    **4. Resting Blood Pressure**: In mm Hg
    
    **5. Cholesterol**: Serum cholesterol in mg/dL
    
    **6. Fasting Blood Sugar (fbs)**:
    - 0 = ≤ 120 mg/dL, 1 = > 120 mg/dL
    
    **7. Resting ECG (restecg)**:
    - 0 = Normal
    - 1 = ST-T wave abnormality
    - 2 = Left ventricular hypertrophy
    
    **8. Max Heart Rate**: Maximum heart rate achieved
    
    **9. Exercise Angina (exang)**:
    - 0 = No, 1 = Yes
    
    **10. ST Depression (oldpeak)**: ST depression induced by exercise
    
    **11. Slope**: Slope of peak exercise ST segment
    - 0 = Upsloping, 1 = Flat, 2 = Downsloping
    
    **12. Major Vessels (ca)**: Number of major vessels (0-3)
    
    **13. Thalassemia (thal)**:
    - 1 = Normal, 2 = Fixed defect, 3 = Reversible defect
    """)
    
    st.markdown("---")
    st.header("📊 Model Performance")
    st.metric("ROC AUC", f"{metrics['roc_auc']:.3f}")
    st.metric("Test Accuracy", f"{metrics['test_accuracy']:.1%}")
    st.metric("Features", metrics['n_features'])

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["🔍 Prediction", "📈 Feature Importance", "ℹ️ Model Info"])

with tab1:
    st.header("Patient Information Form")
    
    # File upload section
    st.subheader("📄 Option 1: Upload Patient Document (DOCX)")
    uploaded_file = st.file_uploader(
        "Upload a DOCX file with patient information",
        type=['docx'],
        help="Upload a DOCX file containing patient data. See template below."
    )
    
    # Template download
    parser = PatientDataParser()
    col_template1, col_template2 = st.columns([3, 1])
    with col_template1:
        st.info("💡 **Tip**: Download the template below, fill it with patient data, then upload it here for automatic processing.")
    with col_template2:
        if st.button("📥 Download Template"):
            template_doc = parser.create_template_docx()
            bio = io.BytesIO()
            template_doc.save(bio)
            bio.seek(0)
            st.download_button(
                label="Download",
                data=bio.getvalue(),
                file_name="patient_data_template.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
    
    # Parse uploaded file
    parsed_data = None
    if uploaded_file is not None:
        with st.spinner("Parsing document..."):
            parsed_data, errors = parser.parse_docx(uploaded_file)
            if parsed_data and len(parsed_data) > 0:
                st.success(f"✅ Successfully extracted {len(parsed_data)} fields from document!")
                if errors:
                    st.warning(f"⚠️ Some fields not found: {', '.join(errors[:3])}")
                # Show extracted data
                with st.expander("📋 View Extracted Data"):
                    st.json(parsed_data)
            else:
                st.error("❌ Could not extract patient data from document. Please check the format.")
                if errors:
                    for error in errors[:5]:
                        st.error(error)
    
    st.markdown("---")
    st.subheader("✍️ Option 2: Manual Entry")
    
    # Create form columns
    col1, col2 = st.columns(2)
    
    # Use parsed data if available, otherwise use form inputs
    if parsed_data and len(parsed_data) > 0:
        # Pre-fill form with parsed data
        age = parsed_data.get('age', 50)
        sex = parsed_data.get('sex', 0)
        cp = parsed_data.get('cp', 0)
        trestbps = parsed_data.get('trestbps', 120)
        chol = parsed_data.get('chol', 200)
        fbs = parsed_data.get('fbs', 0)
        restecg = parsed_data.get('restecg', 0)
        thalach = parsed_data.get('thalach', 150)
        exang = parsed_data.get('exang', 0)
        oldpeak = parsed_data.get('oldpeak', 1.0)
        slope = parsed_data.get('slope', 0)
        ca = parsed_data.get('ca', 0)
        thal = parsed_data.get('thal', 1)
        
        # Show extracted values (read-only display)
        st.info("📋 **Using data from uploaded document.** You can modify values below if needed.")
        col_display1, col_display2 = st.columns(2)
        with col_display1:
            st.text_input("Age (years)", value=str(age), key="age_display", disabled=True)
            st.text_input("Sex", value="Male" if sex == 1 else "Female", key="sex_display", disabled=True)
            cp_map = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-anginal Pain", 3: "Asymptomatic"}
            st.text_input("Chest Pain Type", value=cp_map.get(cp, "Unknown"), key="cp_display", disabled=True)
            st.text_input("Resting BP (mm Hg)", value=str(trestbps), key="trestbps_display", disabled=True)
            st.text_input("Cholesterol (mg/dL)", value=str(chol), key="chol_display", disabled=True)
            st.text_input("Fasting Blood Sugar", value="Yes" if fbs == 1 else "No", key="fbs_display", disabled=True)
            restecg_map = {0: "Normal", 1: "ST-T Wave Abnormality", 2: "Left Ventricular Hypertrophy"}
            st.text_input("Resting ECG", value=restecg_map.get(restecg, "Unknown"), key="restecg_display", disabled=True)
        with col_display2:
            st.text_input("Max Heart Rate", value=str(thalach), key="thalach_display", disabled=True)
            st.text_input("Exercise Angina", value="Yes" if exang == 1 else "No", key="exang_display", disabled=True)
            st.text_input("ST Depression", value=str(oldpeak), key="oldpeak_display", disabled=True)
            slope_map = {0: "Upsloping", 1: "Flat", 2: "Downsloping"}
            st.text_input("Slope", value=slope_map.get(slope, "Unknown"), key="slope_display", disabled=True)
            st.text_input("Major Vessels", value=str(ca), key="ca_display", disabled=True)
            thal_map = {1: "Normal", 2: "Fixed Defect", 3: "Reversible Defect"}
            st.text_input("Thalassemia", value=thal_map.get(thal, "Unknown"), key="thal_display", disabled=True)
    else:
        # Manual entry form
        with col1:
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=50, key="age")
            sex = st.selectbox("Sex", options=[("Female", 0), ("Male", 1)], format_func=lambda x: x[0], key="sex")[1]
            cp = st.selectbox("Chest Pain Type", 
                              options=[("Typical Angina", 0), ("Atypical Angina", 1), 
                                      ("Non-anginal Pain", 2), ("Asymptomatic", 3)],
                              format_func=lambda x: x[0], key="cp")[1]
            trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, value=120, key="trestbps")
            chol = st.number_input("Cholesterol (mg/dL)", min_value=100, max_value=600, value=200, key="chol")
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", 
                               options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], key="fbs")[1]
            restecg = st.selectbox("Resting ECG Results",
                                   options=[("Normal", 0), ("ST-T Wave Abnormality", 1), 
                                           ("Left Ventricular Hypertrophy", 2)],
                                   format_func=lambda x: x[0], key="restecg")[1]
        
        with col2:
            thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150, key="thalach")
            exang = st.selectbox("Exercise Induced Angina",
                                 options=[("No", 0), ("Yes", 1)], format_func=lambda x: x[0], key="exang")[1]
            oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1, key="oldpeak")
            slope = st.selectbox("Slope of Peak Exercise ST Segment",
                                options=[("Upsloping", 0), ("Flat", 1), ("Downsloping", 2)],
                                format_func=lambda x: x[0], key="slope")[1]
            ca = st.number_input("Number of Major Vessels (0-3)", min_value=0, max_value=3, value=0, key="ca")
            thal = st.selectbox("Thalassemia",
                               options=[("Normal", 1), ("Fixed Defect", 2), ("Reversible Defect", 3)],
                               format_func=lambda x: x[0], key="thal")[1]
    
    # Prediction button
    st.markdown("---")
    if st.button("🔍 Predict Heart Disease", type="primary", use_container_width=True):
        # Prepare input data
        patient_data = {
            'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps,
            'chol': chol, 'fbs': fbs, 'restecg': restecg, 'thalach': thalach,
            'exang': exang, 'oldpeak': oldpeak, 'slope': slope, 'ca': ca, 'thal': thal
        }
        
        input_data = pd.DataFrame([patient_data])
        input_data = input_data[feature_names]  # Ensure correct order
        
        # Make prediction
        prediction = pipeline.predict(input_data)[0]
        prediction_proba = pipeline.predict_proba(input_data)[0]
        risk_score = prediction_proba[1]  # Probability of heart disease
        
        # Display results
        st.markdown("---")
        st.header("📊 Prediction Results")
        
        # Result columns
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            if prediction == 1:
                st.error("⚠️ **Heart Disease Detected**")
                st.markdown(f"Risk Level: **{get_risk_level(risk_score)}**")
            else:
                st.success("✅ **No Heart Disease Detected**")
                st.markdown(f"Risk Level: **{get_risk_level(risk_score)}**")
        
        with result_col2:
            st.metric("Risk Score", f"{risk_score:.1%}")
            st.metric("Confidence", f"{max(prediction_proba)*100:.1f}%")
        
        with result_col3:
            st.markdown("**Probability Breakdown:**")
            st.markdown(f"- No Disease: {prediction_proba[0]*100:.1f}%")
            st.markdown(f"- Has Disease: {prediction_proba[1]*100:.1f}%")
        
        # 3D Visualization
        st.markdown("---")
        st.header("🫀 3D Heart Visualization")
        st.markdown("**Interactive 3D heart model - Click and drag to rotate, scroll to zoom**")
        
        # Calculate risk level
        risk_level = get_risk_level(risk_score)
        
        # Create realistic 3D visualization HTML
        html_content = create_realistic_3d_heart_html(risk_score, patient_data)
        
        # Display the HTML component
        components.html(html_content, height=600, scrolling=False)
        
        st.info(f"""
        **Visualization Guide:**
        - **{risk_level} Risk**: {'Dark red with glow indicates high cardiovascular risk' if risk_level == 'HIGH' else 'Normal red coloration suggests lower risk' if risk_level == 'LOW' else 'Brighter red indicates moderate risk'}
        - **Coronary Arteries**: Orange/red when cholesterol is elevated (LDL > 130)
        - **Electrical System**: Cyan (normal) or Purple (abnormal ECG)
        - **Chambers**: 4 chambers (Left/Right Ventricles, Left/Right Atria) with realistic anatomy
        - **Aorta**: Red vessel at top carrying blood from heart
        - **Heartbeat Animation**: Pulsing animation shows cardiac rhythm
        """)
        
        # Clinical Explanation
        st.markdown("---")
        st.header("💡 Clinical Explanation")
        
        with st.spinner("Generating clinical explanation..."):
            explanation = ollama_assistant.generate_explanation(
                patient_data, risk_score, prediction, feature_importances
            )
            st.markdown(explanation)
        
        # Disclaimer
        st.markdown("---")
        st.warning("""
        **⚠️ IMPORTANT DISCLAIMER:**
        This is a decision-support tool for educational and research purposes only. 
        It does NOT replace professional medical diagnosis or treatment. 
        Always consult qualified healthcare professionals for medical decisions.
        """)

with tab2:
    st.header("📈 Feature Importance Analysis")
    st.markdown("Understanding which features contribute most to the model's predictions.")
    
    # Get top features
    importances = np.array(feature_importances['importances'])
    sorted_indices = np.array(feature_importances['sorted_indices'])
    feature_names_list = feature_importances['feature_names']
    
    # Top 10 features
    top_n = 10
    top_indices = sorted_indices[:top_n]
    top_importances = importances[top_indices]
    top_names = [feature_names_list[i] for i in top_indices]
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(range(top_n), top_importances[::-1], color='steelblue')
    ax.set_yticks(range(top_n))
    ax.set_yticklabels(top_names[::-1])
    ax.set_xlabel("Feature Importance")
    ax.set_title("Top 10 Most Important Features (Random Forest)")
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, imp) in enumerate(zip(bars, top_importances[::-1])):
        ax.text(imp + 0.01, i, f'{imp:.3f}', va='center', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Feature importance table
    st.markdown("### Detailed Feature Importance")
    importance_df = pd.DataFrame({
        'Feature': top_names,
        'Importance': top_importances,
        'Rank': range(1, top_n + 1)
    })
    st.dataframe(importance_df, use_container_width=True, hide_index=True)

with tab3:
    st.header("ℹ️ Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Architecture")
        st.markdown("""
        **Algorithm**: Random Forest Classifier
        
        **Pipeline**:
        1. StandardScaler (scaling after train-test split)
        2. Random Forest (200 trees, max_depth=10)
        
        **Training Approach**:
        - ✅ Leak-free pipeline (scaling inside pipeline)
        - ✅ Stratified train-test split
        - ✅ Proper feature-target separation
        """)
        
        st.subheader("Model Performance")
        st.metric("ROC AUC Score", f"{metrics['roc_auc']:.4f}")
        st.metric("Test Accuracy", f"{metrics['test_accuracy']:.1%}")
        st.metric("Training Samples", metrics['n_train_samples'])
        st.metric("Test Samples", metrics['n_test_samples'])
        st.metric("Number of Features", metrics['n_features'])
    
    with col2:
        st.subheader("Dataset Information")
        st.markdown("""
        **Source**: UCI Heart Disease Dataset
        
        **Samples**: 303 patients
        
        **Features**: 13 clinical attributes
        
        **Target**: Binary classification (0 = No disease, 1 = Disease)
        """)
        
        st.subheader("Key Features")
        st.markdown("""
        - Age, Sex, Chest Pain Type
        - Blood Pressure, Cholesterol
        - ECG Results, Heart Rate
        - Exercise-related metrics
        - Thalassemia, Major Vessels
        """)
    
    st.markdown("---")
    st.subheader("⚠️ Important Notes")
    st.info("""
    1. **Leak-Free Training**: The model uses a proper pipeline with scaling applied only after train-test split
    2. **Feature Importance**: Random Forest provides interpretable feature importance scores
    3. **3D Visualization**: Visual representation is a risk-aware metaphor, not anatomical accuracy
    4. **Clinical Support**: Explanations are for decision-support only, not diagnosis
    5. **Synthetic Data**: This dataset is for educational purposes
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Heart Disease Prediction System | Leak-Free ML Pipeline | Built with Streamlit, Scikit-Learn & Plotly</p>
</div>
""", unsafe_allow_html=True)

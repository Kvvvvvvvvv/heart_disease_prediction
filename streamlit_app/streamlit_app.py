"""
Heart Disease Prediction Web App
Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI/UX
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #FF4B4B;
        --secondary-color: #0E1117;
        --accent-color: #00D4FF;
        --success-color: #00CC88;
        --warning-color: #FFA500;
        --danger-color: #FF4444;
        --background-light: #F0F2F6;
        --text-primary: #262730;
        --text-secondary: #555555;
    }
    
    /* Enhanced header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem !important;
        margin-top: 0.5rem !important;
    }
    
    /* Form styling */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Card styling */
    .prediction-card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        background: white;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .prediction-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    
    .success-card {
        border-left-color: #00CC88;
        background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
    }
    
    .danger-card {
        border-left-color: #FF4444;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
    }
    
    /* Metric styling */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar enhancements */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #00D4FF;
        background: #f0f9ff;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #666;
        cursor: help;
    }
    
    /* Animation */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-slide-in {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 2px solid #e0e0e0;
        color: #666;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem !important;
        }
        
        .metric-value {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Title and description with enhanced styling
st.markdown("""
<div class="main-header animate-slide-in">
    <h1>❤️ Heart Disease Prediction System</h1>
    <p>AI-Powered Cardiovascular Risk Assessment</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>🩺 About This Tool</strong><br>
    This application uses a machine learning model to predict the presence of heart disease based on patient medical attributes.
    Enter the patient's information below to get an instant risk assessment.
</div>
""", unsafe_allow_html=True)

# Load model and feature names
@st.cache_resource
def load_model():
    """Load the trained model"""
    import os
    try:
        # Try multiple possible paths
        possible_paths = [
            ("heart_disease_model.pkl", "feature_names.json"),
            ("../heart_disease_model.pkl", "../feature_names.json"),
            ("./heart_disease_model.pkl", "./feature_names.json"),
        ]
        
        for model_path, feature_path in possible_paths:
            if os.path.exists(model_path) and os.path.exists(feature_path):
                model = joblib.load(model_path)
                with open(feature_path, "r") as f:
                    feature_names = json.load(f)
                return model, feature_names
        
        # If not found, show error
        st.error("⚠️ Model files not found! Please ensure 'heart_disease_model.pkl' and 'feature_names.json' are available.")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Error loading model: {str(e)}")
        st.stop()

model, feature_names = load_model()

# Initialize session state for prediction history
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Helper function to create gauge chart
def create_gauge_chart(value, title):
    """Create a gauge chart for risk visualization"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 20, 'color': '#262730'}},
        delta = {'reference': 50, 'increasing': {'color': "#FF4444"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#667eea"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': '#00CC88'},
                {'range': [30, 70], 'color': '#FFA500'},
                {'range': [70, 100], 'color': '#FF4444'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70}}))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# Helper function to create feature contribution chart
def create_feature_contribution_chart(patient_data, feature_names):
    """Create a chart showing which features contributed to the prediction"""
    # Get feature values and normalize them for visualization
    values = [patient_data[name][0] for name in feature_names[:6]]  # Top 6 features
    
    fig = go.Figure(data=[
        go.Bar(
            x=feature_names[:6],
            y=values,
            marker=dict(
                color=values,
                colorscale='Viridis',
                showscale=True
            ),
            text=[f'{v:.1f}' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Key Patient Metrics',
        xaxis_title='Feature',
        yaxis_title='Value',
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# Sidebar with information
with st.sidebar:
    st.markdown("### 📋 Feature Information")
    
    # Add quick presets
    st.markdown("---")
    st.markdown("### 🎯 Quick Test Presets")
    
    preset_options = {
        "Custom": None,
        "Low Risk Patient": {
            'age': 35, 'sex': 0, 'cp': 0, 'trestbps': 110, 'chol': 180,
            'fbs': 0, 'restecg': 0, 'thalach': 170, 'exang': 0,
            'oldpeak': 0.5, 'slope': 0, 'ca': 0, 'thal': 1
        },
        "Moderate Risk Patient": {
            'age': 50, 'sex': 1, 'cp': 2, 'trestbps': 130, 'chol': 240,
            'fbs': 0, 'restecg': 1, 'thalach': 145, 'exang': 0,
            'oldpeak': 1.5, 'slope': 1, 'ca': 1, 'thal': 2
        },
        "High Risk Patient": {
            'age': 65, 'sex': 1, 'cp': 3, 'trestbps': 160, 'chol': 300,
            'fbs': 1, 'restecg': 2, 'thalach': 120, 'exang': 1,
            'oldpeak': 3.5, 'slope': 2, 'ca': 3, 'thal': 3
        }
    }
    
    selected_preset = st.selectbox("Select a preset:", list(preset_options.keys()))
    preset_data = preset_options[selected_preset]
    
    st.markdown("---")
    st.markdown("""
    <div style='font-size: 0.85rem;'>
    <strong>Feature Descriptions:</strong><br><br>
    
    <strong>Age:</strong> Patient's age in years<br><br>
    
    <strong>Sex:</strong><br>
    • Female (0)<br>
    • Male (1)<br><br>
    
    <strong>Chest Pain Type (cp):</strong><br>
    • Typical angina (0)<br>
    • Atypical angina (1)<br>
    • Non-anginal pain (2)<br>
    • Asymptomatic (3)<br><br>
    
    <strong>Resting BP:</strong> In mm Hg<br><br>
    
    <strong>Cholesterol:</strong> Serum cholesterol in mg/dL<br><br>
    
    <strong>Fasting Blood Sugar:</strong><br>
    • ≤ 120 mg/dL (0)<br>
    • > 120 mg/dL (1)<br><br>
    
    <strong>Resting ECG:</strong><br>
    • Normal (0)<br>
    • ST-T wave abnormality (1)<br>
    • Left ventricular hypertrophy (2)<br><br>
    
    <strong>Max Heart Rate:</strong> Maximum heart rate achieved<br><br>
    
    <strong>Exercise Angina:</strong><br>
    • No (0)<br>
    • Yes (1)<br><br>
    
    <strong>ST Depression:</strong> ST depression induced by exercise<br><br>
    
    <strong>Slope:</strong> Slope of peak exercise ST segment<br>
    • Upsloping (0)<br>
    • Flat (1)<br>
    • Downsloping (2)<br><br>
    
    <strong>Major Vessels:</strong> Number of major vessels (0-3)<br><br>
    
    <strong>Thalassemia:</strong><br>
    • Normal (1)<br>
    • Fixed defect (2)<br>
    • Reversible defect (3)
    </div>
    """, unsafe_allow_html=True)

# Main form
st.markdown("### 📝 Patient Information Form")
st.markdown("Fill in the patient's medical information below:")

# Create two columns for better layout
col1, col2 = st.columns(2)

# Use preset data if selected
default_values = preset_data if preset_data else {}

with col1:
    age = st.number_input("👤 Age (years)", min_value=1, max_value=120, 
                         value=default_values.get('age', 50),
                         help="Patient's age in years")
    sex = st.selectbox("⚥ Sex", options=[("Female", 0), ("Male", 1)], 
                      index=default_values.get('sex', 0),
                      format_func=lambda x: x[0],
                      help="Biological sex of the patient")[1]
    cp = st.selectbox("💔 Chest Pain Type", 
                      options=[("Typical Angina", 0), ("Atypical Angina", 1), 
                              ("Non-anginal Pain", 2), ("Asymptomatic", 3)],
                      index=default_values.get('cp', 0),
                      format_func=lambda x: x[0],
                      help="Type of chest pain experienced")[1]
    trestbps = st.number_input("🩺 Resting Blood Pressure (mm Hg)", min_value=50, max_value=250, 
                               value=default_values.get('trestbps', 120),
                               help="Blood pressure at rest")
    chol = st.number_input("🧪 Cholesterol (mg/dL)", min_value=100, max_value=600, 
                          value=default_values.get('chol', 200),
                          help="Serum cholesterol level")
    fbs = st.selectbox("🍬 Fasting Blood Sugar > 120 mg/dL", 
                       options=[("No", 0), ("Yes", 1)], 
                       index=default_values.get('fbs', 0),
                       format_func=lambda x: x[0],
                       help="Whether fasting blood sugar exceeds 120 mg/dL")[1]
    restecg = st.selectbox("📊 Resting ECG Results",
                           options=[("Normal", 0), ("ST-T Wave Abnormality", 1), 
                                   ("Left Ventricular Hypertrophy", 2)],
                           index=default_values.get('restecg', 0),
                           format_func=lambda x: x[0],
                           help="Resting electrocardiographic results")[1]

with col2:
    thalach = st.number_input("💓 Maximum Heart Rate Achieved", min_value=60, max_value=220, 
                             value=default_values.get('thalach', 150),
                             help="Maximum heart rate during exercise test")
    exang = st.selectbox("🏃 Exercise Induced Angina",
                         options=[("No", 0), ("Yes", 1)], 
                         index=default_values.get('exang', 0),
                         format_func=lambda x: x[0],
                         help="Whether exercise induces chest pain")[1]
    oldpeak = st.number_input("📉 ST Depression (oldpeak)", min_value=0.0, max_value=10.0, 
                             value=float(default_values.get('oldpeak', 1.0)), step=0.1,
                             help="ST depression induced by exercise relative to rest")
    slope = st.selectbox("📈 Slope of Peak Exercise ST Segment",
                        options=[("Upsloping", 0), ("Flat", 1), ("Downsloping", 2)],
                        index=default_values.get('slope', 0),
                        format_func=lambda x: x[0],
                        help="The slope of the peak exercise ST segment")[1]
    ca = st.number_input("🫀 Number of Major Vessels (0-3)", min_value=0, max_value=3, 
                        value=default_values.get('ca', 0),
                        help="Number of major vessels colored by fluoroscopy")
    thal = st.selectbox("🔬 Thalassemia",
                       options=[("Normal", 1), ("Fixed Defect", 2), ("Reversible Defect", 3)],
                       index=0 if not default_values else (default_values.get('thal', 1) - 1),
                       format_func=lambda x: x[0],
                       help="Thalassemia test result")[1]

# Prediction button
st.markdown("---")
predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])
with predict_col2:
    predict_button = st.button("🔍 Analyze Heart Disease Risk", type="primary", use_container_width=True)

if predict_button:
    with st.spinner("🔄 Analyzing patient data..."):
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
        risk_score = prediction_proba[1]
        
        # Store in history
        st.session_state.prediction_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'age': age,
            'sex': 'Male' if sex == 1 else 'Female',
            'risk_score': risk_score,
            'prediction': 'Disease' if prediction == 1 else 'No Disease'
        })
        
        # Display results with animation
        st.markdown('<div class="animate-slide-in">', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("## 📊 Prediction Results")
        
        # Result cards in columns
        result_col1, result_col2, result_col3 = st.columns(3)
        
        with result_col1:
            if prediction == 1:
                st.markdown("""
                <div class="prediction-card danger-card">
                    <h2 style='color: #FF4444; margin: 0;'>⚠️ Risk Detected</h2>
                    <p style='font-size: 1.1rem; margin-top: 0.5rem;'>The model predicts <strong>heart disease presence</strong></p>
                    <p style='color: #666; margin-top: 1rem; font-size: 0.9rem;'>Immediate medical consultation recommended</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="prediction-card success-card">
                    <h2 style='color: #00CC88; margin: 0;'>✅ Low Risk</h2>
                    <p style='font-size: 1.1rem; margin-top: 0.5rem;'>The model predicts <strong>no heart disease</strong></p>
                    <p style='color: #666; margin-top: 1rem; font-size: 0.9rem;'>Continue regular health monitoring</p>
                </div>
                """, unsafe_allow_html=True)
        
        with result_col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Risk Score</div>
                <div class="metric-value">{risk_score*100:.1f}%</div>
                <div style='color: #666; margin-top: 0.5rem;'>Probability of Heart Disease</div>
            </div>
            """, unsafe_allow_html=True)
        
        with result_col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">Confidence</div>
                <div class="metric-value">{max(prediction_proba)*100:.1f}%</div>
                <div style='color: #666; margin-top: 0.5rem;'>Model Confidence Level</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Probability breakdown
        st.markdown("### 📈 Detailed Probability Breakdown")
        prob_col1, prob_col2 = st.columns(2)
        
        with prob_col1:
            st.markdown(f"""
            <div style='padding: 1rem; background: linear-gradient(135deg, #e6ffed 0%, #b3ffe6 100%); 
                 border-radius: 10px; border-left: 4px solid #00CC88;'>
                <h4 style='margin: 0; color: #00CC88;'>✓ No Disease</h4>
                <p style='font-size: 2rem; font-weight: 700; margin: 0.5rem 0; color: #262730;'>
                    {prediction_proba[0]*100:.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with prob_col2:
            st.markdown(f"""
            <div style='padding: 1rem; background: linear-gradient(135deg, #ffe6e6 0%, #ffcccc 100%); 
                 border-radius: 10px; border-left: 4px solid #FF4444;'>
                <h4 style='margin: 0; color: #FF4444;'>⚠ Disease Present</h4>
                <p style='font-size: 2rem; font-weight: 700; margin: 0.5rem 0; color: #262730;'>
                    {prediction_proba[1]*100:.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk gauge chart
        st.markdown("### 🎯 Risk Assessment Gauge")
        gauge_col1, gauge_col2 = st.columns([2, 1])
        
        with gauge_col1:
            fig_gauge = create_gauge_chart(risk_score, "Cardiovascular Risk Level")
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with gauge_col2:
            st.markdown("""
            <div style='padding: 1.5rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
                <h4 style='margin-top: 0;'>Risk Levels Guide:</h4>
                <p style='margin: 0.5rem 0;'>
                    <span style='color: #00CC88; font-weight: 600;'>● 0-30%:</span> Low Risk<br>
                    <span style='color: #FFA500; font-weight: 600;'>● 30-70%:</span> Moderate Risk<br>
                    <span style='color: #FF4444; font-weight: 600;'>● 70-100%:</span> High Risk
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Feature contribution chart
        st.markdown("### 🔬 Patient Metrics Overview")
        fig_features = create_feature_contribution_chart(input_data, feature_names)
        st.plotly_chart(fig_features, use_container_width=True)
        
        # Export results option
        st.markdown("### 💾 Export Results")
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            # Create CSV data
            result_df = pd.DataFrame([{
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'Age': age,
                'Sex': 'Male' if sex == 1 else 'Female',
                'Prediction': 'Disease' if prediction == 1 else 'No Disease',
                'Risk Score': f"{risk_score*100:.1f}%",
                'Confidence': f"{max(prediction_proba)*100:.1f}%",
                'No Disease Probability': f"{prediction_proba[0]*100:.1f}%",
                'Disease Probability': f"{prediction_proba[1]*100:.1f}%"
            }])
            
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name=f"heart_disease_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with export_col2:
            # Create JSON data
            result_json = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'patient_data': {
                    'age': int(age),
                    'sex': 'Male' if sex == 1 else 'Female',
                    'chest_pain_type': ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'][cp],
                    'resting_bp': int(trestbps),
                    'cholesterol': int(chol),
                    'fasting_blood_sugar': 'High' if fbs == 1 else 'Normal',
                    'max_heart_rate': int(thalach)
                },
                'prediction': {
                    'result': 'Disease' if prediction == 1 else 'No Disease',
                    'risk_score': float(f"{risk_score*100:.1f}"),
                    'confidence': float(f"{max(prediction_proba)*100:.1f}"),
                    'probabilities': {
                        'no_disease': float(f"{prediction_proba[0]*100:.1f}"),
                        'disease': float(f"{prediction_proba[1]*100:.1f}")
                    }
                }
            }
            
            st.download_button(
                label="📥 Download Results as JSON",
                data=json.dumps(result_json, indent=2),
                file_name=f"heart_disease_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Warning
        st.markdown("---")
        st.warning("""
        **⚠️ MEDICAL DISCLAIMER:**  
        This is a machine learning prediction tool for **educational and research purposes only**.  
        It is **NOT a substitute for professional medical advice, diagnosis, or treatment**.  
        Always consult with qualified healthcare professionals for medical decisions and diagnosis.  
        The predictions are based on statistical patterns and may not reflect individual medical circumstances.
        """)

# Prediction history section
if st.session_state.prediction_history:
    st.markdown("---")
    st.markdown("### 📜 Prediction History")
    
    history_df = pd.DataFrame(st.session_state.prediction_history)
    
    # Display as a nice table
    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "timestamp": "Timestamp",
            "age": "Age",
            "sex": "Sex",
            "risk_score": st.column_config.ProgressColumn(
                "Risk Score",
                format="%.2f",
                min_value=0,
                max_value=1,
            ),
            "prediction": "Result"
        }
    )
    
    # Clear history button
    if st.button("🗑️ Clear History", type="secondary"):
        st.session_state.prediction_history = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <h3 style='color: #667eea; margin-bottom: 1rem;'>❤️ Heart Disease Prediction System</h3>
    <p style='font-size: 0.9rem; margin: 0.5rem 0;'>
        <strong>Powered by:</strong> Machine Learning • Streamlit • Scikit-Learn • Plotly
    </p>
    <p style='font-size: 0.85rem; color: #888; margin-top: 1rem;'>
        Version 2.0 | Enhanced UI/UX Design | Full-Stack Features
    </p>
    <p style='font-size: 0.8rem; color: #999; margin-top: 0.5rem;'>
        For educational and research purposes only. Not for clinical use.
    </p>
</div>
""", unsafe_allow_html=True)

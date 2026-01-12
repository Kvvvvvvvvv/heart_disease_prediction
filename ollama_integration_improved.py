"""
Improved Ollama Integration for Clinical Decision Support
Intelligently analyzes patient data to match risk scores
"""
import requests
import json

class OllamaClinicalAssistant:
    """
    Clinical decision-support assistant using Ollama
    Provides intelligent explanations that match risk scores
    """
    
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama3"  # Default model, can be changed
    
    def check_ollama_available(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def _analyze_risk_factors(self, patient_data, risk_score):
        """
        Intelligently analyze patient data to identify risk factors
        Uses clinical thresholds and considers combinations
        """
        factors = []
        severity_notes = []
        
        age = patient_data.get('age', 0)
        sex = patient_data.get('sex', 0)
        cp = patient_data.get('cp', 0)
        trestbps = patient_data.get('trestbps', 0)
        chol = patient_data.get('chol', 0)
        fbs = patient_data.get('fbs', 0)
        restecg = patient_data.get('restecg', 0)
        thalach = patient_data.get('thalach', 0)
        exang = patient_data.get('exang', 0)
        oldpeak = patient_data.get('oldpeak', 0)
        slope = patient_data.get('slope', 0)
        ca = patient_data.get('ca', 0)
        thal = patient_data.get('thal', 0)
        
        # Age-related factors (more nuanced)
        if age >= 65:
            factors.append("Advanced age (≥65 years)")
            severity_notes.append("high")
        elif age >= 55:
            factors.append("Age-related risk (55-64 years)")
            severity_notes.append("moderate")
        elif age >= 45:
            factors.append("Age factor (45-54 years)")
            severity_notes.append("low")
        
        # Gender (males have higher risk)
        if sex == 1 and age > 45:
            factors.append("Male gender with age-related risk")
            severity_notes.append("moderate")
        
        # Chest pain type (critical indicator)
        if cp == 0:  # Typical angina
            factors.append("Typical angina (classic chest pain pattern)")
            severity_notes.append("high")
        elif cp == 1:  # Atypical angina
            factors.append("Atypical angina pattern")
            severity_notes.append("moderate")
        elif cp == 3:  # Asymptomatic
            if risk_score > 0.5:
                factors.append("Asymptomatic presentation despite elevated risk")
                severity_notes.append("moderate")
        
        # Blood pressure (more nuanced thresholds)
        if trestbps >= 160:
            factors.append("Stage 2 hypertension (≥160 mm Hg)")
            severity_notes.append("high")
        elif trestbps >= 140:
            factors.append("Stage 1 hypertension (140-159 mm Hg)")
            severity_notes.append("moderate")
        elif trestbps >= 130:
            factors.append("Elevated blood pressure (130-139 mm Hg)")
            severity_notes.append("low")
        
        # Cholesterol (more nuanced)
        if chol >= 240:
            factors.append("High cholesterol (≥240 mg/dL)")
            severity_notes.append("high")
        elif chol >= 200:
            factors.append("Borderline high cholesterol (200-239 mg/dL)")
            severity_notes.append("moderate")
        elif chol >= 180:
            factors.append("Elevated cholesterol (180-199 mg/dL)")
            severity_notes.append("low")
        
        # Fasting blood sugar
        if fbs == 1:
            factors.append("Elevated fasting blood sugar (>120 mg/dL)")
            severity_notes.append("moderate")
        
        # Resting ECG abnormalities
        if restecg == 1:
            factors.append("ST-T wave abnormality on resting ECG")
            severity_notes.append("moderate")
        elif restecg == 2:
            factors.append("Left ventricular hypertrophy on ECG")
            severity_notes.append("high")
        
        # Maximum heart rate (lower is worse)
        if thalach < 120:
            factors.append("Low maximum heart rate (<120 bpm)")
            severity_notes.append("high")
        elif thalach < 140:
            factors.append("Reduced maximum heart rate (120-139 bpm)")
            severity_notes.append("moderate")
        
        # Exercise-induced angina
        if exang == 1:
            factors.append("Exercise-induced angina")
            severity_notes.append("high")
        
        # ST depression (critical indicator)
        if oldpeak >= 2.0:
            factors.append("Significant ST depression (≥2.0 mm)")
            severity_notes.append("high")
        elif oldpeak >= 1.0:
            factors.append("ST depression (1.0-1.9 mm)")
            severity_notes.append("moderate")
        elif oldpeak > 0:
            factors.append("Mild ST depression (<1.0 mm)")
            severity_notes.append("low")
        
        # Slope of ST segment
        if slope == 2:  # Downsloping (worst)
            factors.append("Downsloping ST segment (concerning pattern)")
            severity_notes.append("high")
        elif slope == 1:  # Flat
            factors.append("Flat ST segment")
            severity_notes.append("moderate")
        
        # Number of major vessels (critical)
        if ca >= 2:
            factors.append(f"Multiple major vessel involvement ({ca} vessels)")
            severity_notes.append("high")
        elif ca == 1:
            factors.append("Single major vessel involvement")
            severity_notes.append("moderate")
        
        # Thalassemia (thallium scan results)
        if thal == 2:  # Fixed defect
            factors.append("Fixed defect on thallium scan")
            severity_notes.append("high")
        elif thal == 3:  # Reversible defect
            factors.append("Reversible defect on thallium scan")
            severity_notes.append("moderate")
        
        # If risk is high but no obvious factors, look for combinations
        if risk_score > 0.6 and len(factors) < 3:
            # Check for subtle combinations
            if cp in [0, 1] and oldpeak > 0.5:
                factors.append("Combination of chest pain pattern and ST changes")
                severity_notes.append("moderate")
            if chol > 180 and trestbps > 120:
                factors.append("Combined cholesterol and blood pressure elevation")
                severity_notes.append("moderate")
            if age > 50 and thalach < 150:
                factors.append("Age-related cardiovascular changes with reduced exercise capacity")
                severity_notes.append("moderate")
        
        # If still no factors but high risk, explain model-based assessment
        if risk_score > 0.6 and len(factors) == 0:
            factors.append("Model-identified risk pattern (multiple subtle factors)")
            severity_notes.append("moderate")
        
        return factors, severity_notes
    
    def generate_explanation(self, patient_data, risk_score, prediction, feature_importances=None):
        """
        Generate clinical explanation using Ollama or intelligent fallback
        
        Parameters:
        -----------
        patient_data : dict
            Patient medical data
        risk_score : float
            Risk score (0-1)
        prediction : int
            Prediction (0 or 1)
        feature_importances : dict, optional
            Feature importance data for better explanations
        """
        
        # Always analyze risk factors first
        factors, severity_notes = self._analyze_risk_factors(patient_data, risk_score)
        risk_level = "LOW" if risk_score < 0.3 else "MODERATE" if risk_score < 0.6 else "HIGH"
        
        # Check if Ollama is available
        if self.check_ollama_available():
            return self._ollama_explanation(patient_data, risk_score, prediction, factors, risk_level)
        else:
            return self._intelligent_fallback(patient_data, risk_score, prediction, factors, severity_notes, risk_level)
    
    def _ollama_explanation(self, patient_data, risk_score, prediction, factors, risk_level):
        """Generate explanation using Ollama"""
        system_prompt = """You are a clinical decision-support assistant.
You do NOT diagnose diseases.
You explain cardiovascular risk using structured clinical data.
Always include disclaimers.
Use clear, non-alarming language.
Be specific about risk factors identified.
Keep responses concise (4-5 paragraphs maximum)."""
        
        factors_text = "\n".join([f"- {f}" for f in factors]) if factors else "- Multiple subtle risk factors identified by the model"
        
        user_prompt = f"""Patient Profile:
Age: {patient_data.get('age', 'N/A')} years
Sex: {'Male' if patient_data.get('sex', 0) == 1 else 'Female'}
Resting BP: {patient_data.get('trestbps', 'N/A')} mm Hg
Cholesterol: {patient_data.get('chol', 'N/A')} mg/dL
Max Heart Rate: {patient_data.get('thalach', 'N/A')} bpm
ST Depression: {patient_data.get('oldpeak', 'N/A')} mm
Chest Pain Type: {patient_data.get('cp', 'N/A')}
Exercise Angina: {'Yes' if patient_data.get('exang', 0) == 1 else 'No'}
Major Vessels: {patient_data.get('ca', 'N/A')}
Thalassemia: {patient_data.get('thal', 'N/A')}

Risk Score: {risk_score:.1%} ({risk_level} risk)
Prediction: {'Heart disease detected' if prediction == 1 else 'No heart disease detected'}

Identified Risk Factors:
{factors_text}

Explain:
1. Overall cardiovascular risk assessment matching the {risk_level} risk score
2. How the identified risk factors contribute to this risk level
3. What the 3D heart visualization represents for this patient
4. Specific lifestyle or follow-up recommendations based on the risk factors
5. Clear medical disclaimer"""
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": f"{system_prompt}\n\n{user_prompt}",
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                explanation = result.get("response", "")
                # Add disclaimer if not present
                if "disclaimer" not in explanation.lower():
                    explanation += "\n\n**⚠️ MEDICAL DISCLAIMER:** This is a decision-support tool for educational purposes only. Always consult qualified healthcare professionals for medical decisions."
                return explanation
            else:
                return self._intelligent_fallback(patient_data, risk_score, prediction, factors, [], risk_level)
                
        except Exception as e:
            print(f"Ollama error: {e}")
            return self._intelligent_fallback(patient_data, risk_score, prediction, factors, [], risk_level)
    
    def _intelligent_fallback(self, patient_data, risk_score, prediction, factors, severity_notes, risk_level):
        """Intelligent fallback explanation that matches risk scores"""
        
        # Build explanation based on risk level and factors
        explanation = f"""**Risk Assessment: {risk_level.upper()} RISK ({risk_score:.1%})**

**Overall Assessment:**
Based on comprehensive analysis of clinical parameters, the model indicates a **{risk_level.lower()}** cardiovascular risk level ({risk_score:.1%}). {'Heart disease indicators are present and require attention.' if prediction == 1 else 'The assessment suggests monitoring and preventive measures.'}

**Key Contributing Factors:**
"""
        
        if factors:
            # Group factors by severity
            high_severity = [f for f, s in zip(factors, severity_notes) if s == "high"]
            moderate_severity = [f for f, s in zip(factors, severity_notes) if s == "moderate"]
            low_severity = [f for f, s in zip(factors, severity_notes) if s == "low"]
            
            if high_severity:
                explanation += "\n**High Impact Factors:**\n"
                explanation += "\n".join([f"- {f}" for f in high_severity])
            
            if moderate_severity:
                explanation += "\n\n**Moderate Impact Factors:**\n"
                explanation += "\n".join([f"- {f}" for f in moderate_severity])
            
            if low_severity:
                explanation += "\n\n**Contributing Factors:**\n"
                explanation += "\n".join([f"- {f}" for f in low_severity])
        else:
            # If no obvious factors but high risk, explain model-based assessment
            explanation += f"""
The model has identified a {risk_level.lower()} risk level based on a combination of subtle factors that may not be immediately obvious. This could include:
- Interactions between multiple clinical parameters
- Pattern recognition across various cardiovascular indicators
- Non-linear relationships between risk factors

Even without obvious individual risk factors, the combination of values suggests elevated cardiovascular risk."""
        
        # Add specific recommendations based on risk level
        explanation += f"""

**3D Visualization Interpretation:**
The 3D heart visualization reflects the {risk_level.lower()} risk level. """
        
        if risk_level == "HIGH":
            explanation += "Dark red coloration with glow, orange/red coronary arteries, and potential markers indicate elevated cardiovascular risk requiring immediate attention."
        elif risk_level == "MODERATE":
            explanation += "Brighter red coloration and highlighted coronary arteries suggest moderate risk that warrants monitoring and lifestyle modifications."
        else:
            explanation += "Normal red coloration suggests lower risk, but regular monitoring is still recommended."
        
        explanation += f"""

**Recommendations:**
"""
        
        if risk_level == "HIGH":
            explanation += """
- **Immediate medical consultation** recommended
- Comprehensive cardiovascular evaluation
- Consider additional diagnostic tests (stress test, echocardiogram)
- Aggressive lifestyle modifications (diet, exercise, smoking cessation if applicable)
- Regular monitoring of blood pressure, cholesterol, and other cardiovascular markers
- Follow-up with cardiologist within 1-2 weeks"""
        elif risk_level == "MODERATE":
            explanation += """
- Schedule follow-up with healthcare provider within 1-2 months
- Implement lifestyle modifications (heart-healthy diet, regular exercise)
- Monitor blood pressure and cholesterol regularly
- Consider preventive medications if recommended by physician
- Annual cardiovascular risk assessment"""
        else:
            explanation += """
- Maintain healthy lifestyle (balanced diet, regular exercise)
- Annual health check-ups
- Continue monitoring cardiovascular markers
- Preventive measures to maintain low risk status"""
        
        explanation += """

**⚠️ MEDICAL DISCLAIMER:**
This is a decision-support tool for educational purposes only. It does NOT replace professional medical diagnosis or treatment. Always consult qualified healthcare professionals for medical decisions. This model uses example data and should not be used for actual patient care."""
        
        return explanation

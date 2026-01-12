"""
Ollama Integration for Clinical Decision Support
Provides safe, field-aware explanations
"""
import requests
import json

class OllamaClinicalAssistant:
    """
    Clinical decision-support assistant using Ollama
    Provides safe explanations with proper disclaimers
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
    
    def generate_explanation(self, patient_data, risk_score, prediction):
        """
        Generate clinical explanation using Ollama
        
        Parameters:
        -----------
        patient_data : dict
            Patient medical data
        risk_score : float
            Risk score (0-1)
        prediction : int
            Prediction (0 or 1)
        
        Returns:
        --------
        explanation : str
            Clinical explanation
        """
        
        # Check if Ollama is available
        if not self.check_ollama_available():
            return self._fallback_explanation(patient_data, risk_score, prediction)
        
        # System prompt (fixed)
        system_prompt = """You are a clinical decision-support assistant.
You do NOT diagnose diseases.
You explain cardiovascular risk using structured clinical data.
Always include disclaimers.
Use clear, non-alarming language.
Keep responses concise (3-4 paragraphs maximum)."""
        
        # User prompt (dynamic)
        risk_level = "LOW" if risk_score < 0.3 else "MODERATE" if risk_score < 0.6 else "HIGH"
        
        user_prompt = f"""Patient Profile:
Age: {patient_data.get('age', 'N/A')}
Sex: {'Male' if patient_data.get('sex', 0) == 1 else 'Female'}
Resting BP: {patient_data.get('trestbps', 'N/A')} mm Hg
Cholesterol: {patient_data.get('chol', 'N/A')} mg/dL
Max Heart Rate: {patient_data.get('thalach', 'N/A')} bpm
ST Depression: {patient_data.get('oldpeak', 'N/A')}
Chest Pain Type: {patient_data.get('cp', 'N/A')}
Exercise Angina: {'Yes' if patient_data.get('exang', 0) == 1 else 'No'}

Risk Score: {risk_score:.1%} ({risk_level} risk)
Prediction: {'Heart disease detected' if prediction == 1 else 'No heart disease detected'}

Explain:
1. Overall cardiovascular risk assessment
2. Key contributing factors from the patient's profile
3. What the 3D heart visualization represents
4. General lifestyle or follow-up suggestions
5. Clear medical disclaimer"""
        
        try:
            # Call Ollama API
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
                return result.get("response", self._fallback_explanation(patient_data, risk_score, prediction))
            else:
                return self._fallback_explanation(patient_data, risk_score, prediction)
                
        except Exception as e:
            print(f"Ollama error: {e}")
            return self._fallback_explanation(patient_data, risk_score, prediction)
    
    def _fallback_explanation(self, patient_data, risk_score, prediction):
        """Fallback explanation when Ollama is not available"""
        risk_level = "LOW" if risk_score < 0.3 else "MODERATE" if risk_score < 0.6 else "HIGH"
        
        explanation = f"""**Risk Assessment: {risk_level.upper()} RISK ({risk_score:.1%})**

**Overall Assessment:**
Based on the provided clinical parameters, the model indicates a {risk_level.lower()} cardiovascular risk level. {'Heart disease indicators are present.' if prediction == 1 else 'No significant heart disease indicators detected.'}

**Key Contributing Factors:**
"""
        
        # Add factors based on patient data
        factors = []
        if patient_data.get('age', 0) > 60:
            factors.append("Advanced age")
        if patient_data.get('chol', 0) > 240:
            factors.append("Elevated cholesterol levels")
        if patient_data.get('trestbps', 0) > 140:
            factors.append("High resting blood pressure")
        if patient_data.get('oldpeak', 0) > 2.0:
            factors.append("Significant ST depression")
        if patient_data.get('exang', 0) == 1:
            factors.append("Exercise-induced angina")
        
        if factors:
            explanation += "\n".join([f"- {f}" for f in factors])
        else:
            explanation += "- No major risk factors identified"
        
        explanation += f"""

**3D Visualization Interpretation:**
The 3D heart visualization reflects the {risk_level.lower()} risk level. {'Red coloration and artery highlighting indicate elevated cardiovascular risk.' if risk_level == 'HIGH' else 'Normal coloration suggests lower risk levels.'}

**Recommendations:**
- Regular cardiovascular monitoring
- Maintain healthy lifestyle (diet, exercise)
- Follow up with healthcare provider
- Consider additional diagnostic tests if risk is moderate to high

**⚠️ MEDICAL DISCLAIMER:**
This is a decision-support tool for educational purposes only. It does NOT replace professional medical diagnosis or treatment. Always consult qualified healthcare professionals for medical decisions. This model uses synthetic/example data and should not be used for actual patient care."""

        return explanation

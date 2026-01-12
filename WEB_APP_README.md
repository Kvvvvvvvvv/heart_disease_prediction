# Heart Disease Prediction Web App

A user-friendly web application for predicting heart disease based on patient medical attributes.

## 🚀 Quick Start

### Step 1: Train the Model (One-time setup)
```bash
python train_and_save_model.py
```
This will create `heart_disease_model.pkl` and `feature_names.json`.

### Step 2: Launch the Web App
```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📋 Features

- **Interactive Form**: Easy-to-use input form for patient data
- **Real-time Prediction**: Instant results with confidence scores
- **Feature Information**: Sidebar with detailed explanations of each feature
- **Professional UI**: Clean, modern interface built with Streamlit

## 🎯 How to Use

1. **Fill in Patient Information**:
   - Enter patient's age, sex, and medical measurements
   - Use the dropdowns for categorical features
   - All fields have helpful descriptions

2. **Get Prediction**:
   - Click the "Predict Heart Disease" button
   - View the prediction result (Has Disease / No Disease)
   - Check the confidence percentage

3. **Interpret Results**:
   - **Red Alert**: Heart disease detected - consult a doctor
   - **Green Check**: No heart disease detected
   - Confidence score shows prediction certainty

## ⚠️ Important Disclaimer

This is an **educational tool** for demonstration purposes only. 
**Always consult qualified healthcare professionals** for actual medical diagnosis and treatment decisions.

## 📊 Model Information

- **Algorithm**: Logistic Regression with Grid Search optimization
- **Accuracy**: ~88.5% on test data
- **Features**: 13 medical attributes
- **Training Data**: UCI Heart Disease Dataset (303 patients)

## 🔧 Troubleshooting

**Model file not found?**
- Run `python train_and_save_model.py` first

**Port already in use?**
- Streamlit will automatically use the next available port
- Check the terminal for the actual URL

**App not loading?**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're in the project directory

## 📁 Files

- `app.py` - Main Streamlit web application
- `train_and_save_model.py` - Script to train and save the model
- `heart_disease_model.pkl` - Trained model file (created after training)
- `feature_names.json` - Feature names for the model (created after training)

Enjoy using the Heart Disease Prediction System! ❤️

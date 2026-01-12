# 🚀 How to Run the Enhanced App

## ⚠️ IMPORTANT: Make sure you're running the RIGHT app!

You have TWO apps:
1. `app.py` - Basic version (what you're seeing now)
2. `app_enhanced.py` - Enhanced version with 3D visualization, feature importance, etc.

## ✅ Step-by-Step Instructions

### Step 1: Stop any running Streamlit apps
Close any browser tabs with Streamlit, and press `Ctrl+C` in any terminal windows running Streamlit.

### Step 2: Make sure model files exist
```bash
python train_model_leak_free.py
```

This creates:
- `heart_disease_model.pkl`
- `feature_names.json`
- `feature_importances.json` ← Required for enhanced app
- `model_metrics.json` ← Required for enhanced app

### Step 3: Run the ENHANCED app
```bash
streamlit run app_enhanced.py
```

**OR** double-click: `start_enhanced_app.bat`

### Step 4: Check the URL
Look in the terminal for:
```
Local URL: http://localhost:8501/?token=...
```

Copy the **ENTIRE URL** including `?token=...` and paste in browser.

## 🎯 What You Should See in Enhanced App

### Enhanced Features:
1. **Title**: "Advanced ML-powered cardiovascular risk assessment..."
2. **Tabs**: "🔍 Prediction", "📈 Feature Importance", "ℹ️ Model Info"
3. **3D Visualization**: Interactive heart that changes color based on risk
4. **Risk Level**: Shows "LOW", "MODERATE", or "HIGH" risk
5. **Clinical Explanation**: AI-powered or rule-based explanations
6. **Feature Importance Tab**: Shows top 10 features

### If you see the basic app instead:
- You're running `app.py` instead of `app_enhanced.py`
- Check the terminal command - should say `app_enhanced.py`
- Make sure you're using the correct file

## 🔍 Quick Check

Run this to verify files exist:
```bash
dir feature_importances.json model_metrics.json
```

If files are missing, run:
```bash
python train_model_leak_free.py
```

## 🐛 Troubleshooting

**"Model files not found" error?**
- Run `python train_model_leak_free.py` first

**Still seeing basic app?**
- Make sure you're running `app_enhanced.py` not `app.py`
- Check terminal shows: `streamlit run app_enhanced.py`
- Try closing browser and reopening with fresh URL

**Port already in use?**
- Streamlit will use next available port (8502, 8503, etc.)
- Check terminal for actual URL

## ✅ Success Indicators

When enhanced app is working, you'll see:
- ✅ "Advanced ML-powered..." subtitle
- ✅ Three tabs at the top
- ✅ Risk level (LOW/MODERATE/HIGH) in results
- ✅ 3D heart visualization after prediction
- ✅ Feature Importance tab with charts

If you don't see these, you're running the basic app!

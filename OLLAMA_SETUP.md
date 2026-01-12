# Ollama Setup Guide (Optional)

## What is Ollama?

Ollama allows you to run large language models locally for AI-powered clinical explanations. The app works great without it (using intelligent fallback), but Ollama provides more detailed, contextual explanations.

## Quick Setup

### Step 1: Download Ollama
Visit: https://ollama.ai
- Download for Windows/Mac/Linux
- Install the application

### Step 2: Pull a Model
Open terminal/command prompt and run:
```bash
ollama pull llama3
```

This downloads the Llama 3 model (~4.7GB). Other options:
- `ollama pull llama3.1` (newer version)
- `ollama pull mistral` (smaller, faster)
- `ollama pull phi3` (very small, fast)

### Step 3: Start Ollama
Ollama usually runs automatically after installation. To verify:
```bash
ollama list
```

If it shows your models, you're ready!

### Step 4: Test in the App
1. Run `streamlit run app_enhanced.py`
2. Make a prediction
3. The app will automatically detect and use Ollama
4. You'll get AI-powered explanations!

## Benefits

**With Ollama:**
- More detailed, contextual explanations
- Better understanding of risk factor combinations
- Natural language explanations

**Without Ollama (Fallback):**
- Still works perfectly!
- Intelligent risk factor analysis
- Matches risk scores accurately
- No installation needed

## Troubleshooting

**Ollama not detected?**
- Make sure Ollama is running
- Check: `ollama list` works in terminal
- Restart the Streamlit app

**Slow responses?**
- Use a smaller model: `ollama pull phi3`
- Or stick with the intelligent fallback (works great!)

## Note

The improved fallback explanation is now very intelligent and matches risk scores accurately, so Ollama is optional but nice to have!

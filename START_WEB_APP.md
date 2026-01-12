# How to Start the Web App - Step by Step

## ⚠️ Connection Refused? Follow These Steps:

### Method 1: Using Command Prompt/PowerShell (Recommended)

1. **Open PowerShell or Command Prompt**
   - Press `Windows + R`
   - Type `powershell` or `cmd`
   - Press Enter

2. **Navigate to the project folder:**
   ```powershell
   cd "C:\Users\keert\Downloads\UCI-Heart-Disease-Dataset-master\UCI-Heart-Disease-Dataset-master"
   ```

3. **Run Streamlit:**
   ```powershell
   streamlit run app.py
   ```

4. **Wait for the output** - You should see something like:
   ```
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

5. **Copy the URL** from the terminal (it will have a token)
   - Look for: `http://localhost:8501/?token=...`
   - Copy the ENTIRE URL including the token part

6. **Paste it in your browser** and press Enter

---

### Method 2: Double-Click the Batch File

1. **Double-click** `start_web_app.bat`
2. A terminal window will open
3. Wait for the URL to appear
4. Copy and paste it in your browser

---

### Method 3: Check What Port is Being Used

If port 8501 is busy, Streamlit will use a different port. Look at the terminal output for the actual port number.

---

## 🔍 Troubleshooting

### If you see "command not found":
```powershell
python -m streamlit run app.py
```

### If you see "model not found":
```powershell
python train_and_save_model.py
```
Then try running Streamlit again.

### If port 8501 is busy:
Streamlit will automatically use the next available port (8502, 8503, etc.)
**Check the terminal output for the actual URL!**

### If browser doesn't open automatically:
- Look at the terminal window
- Find the line that says "Local URL:"
- Copy that entire URL (including `?token=...`)
- Paste it in your browser

---

## ✅ Success Indicators

When it's working, you should see:
- Terminal shows: "You can now view your Streamlit app..."
- Browser opens automatically OR you see a URL in the terminal
- The web page loads with the Heart Disease Prediction form

---

## 🛑 To Stop the Server

Press `Ctrl + C` in the terminal window where Streamlit is running.

---

**Remember:** The URL in the terminal is what you need - copy the ENTIRE URL including the token part!

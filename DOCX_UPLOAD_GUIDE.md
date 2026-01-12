# 📄 DOCX Upload Feature - User Guide

## ✨ New Feature: Upload Patient Documents

You can now upload a DOCX file with patient information instead of manually typing everything!

## 🚀 How to Use

### Step 1: Download Template
1. In the app, click **"📥 Download Template"**
2. A template DOCX file will download
3. Open it in Microsoft Word or any word processor

### Step 2: Fill in Patient Data
Fill in the template with patient information. You can use formats like:
- `Age: 50`
- `Sex: Male` or `Sex: Female`
- `Cholesterol: 200`
- `Resting BP: 120`
- `ST Depression: 1.0`
- etc.

**Supported Formats:**
- `Field: Value` (e.g., `Age: 50`)
- `Field Value` (e.g., `Age 50`)
- `Value Field` (e.g., `50 years old`)
- Natural language (e.g., `Patient is 50 years old`)

### Step 3: Upload Document
1. Save your filled template
2. In the app, click **"Browse files"** under "Upload a DOCX file"
3. Select your DOCX file
4. The app will automatically parse and extract data

### Step 4: Review & Predict
1. Review the extracted data (shown in expandable section)
2. Modify any values if needed
3. Click **"🔍 Predict Heart Disease"**
4. Get instant results!

## 📋 Supported Fields

The parser recognizes these fields (case-insensitive):

| Field | Examples |
|-------|----------|
| **Age** | Age: 50, Patient age: 50, 50 years old |
| **Sex** | Sex: Male, Gender: Female, Male, Female |
| **Chest Pain** | Typical Angina, Atypical Angina, Non-anginal Pain, Asymptomatic |
| **Blood Pressure** | Resting BP: 120, Blood Pressure: 120, BP: 120 |
| **Cholesterol** | Cholesterol: 200, Total Cholesterol: 200 |
| **Fasting Blood Sugar** | FBS: Yes, Fasting Blood Sugar: No, >120 mg/dL |
| **Resting ECG** | Normal, ST-T wave abnormality, Left ventricular hypertrophy |
| **Max Heart Rate** | Max Heart Rate: 150, HR Max: 150 |
| **Exercise Angina** | Exercise Angina: Yes, Exercise-induced angina: No |
| **ST Depression** | ST Depression: 1.0, Oldpeak: 1.0 |
| **Slope** | Upsloping, Flat, Downsloping |
| **Major Vessels** | Major Vessels: 0, CA: 2, Number of vessels: 1 |
| **Thalassemia** | Normal, Fixed defect, Reversible defect |

## 💡 Tips

1. **Use the template** - It's formatted correctly
2. **Be consistent** - Use similar formats throughout
3. **Check extraction** - Review extracted data before predicting
4. **Manual override** - You can still edit values after upload

## ⚠️ Troubleshooting

**No data extracted?**
- Check that field names match (case-insensitive)
- Use format: `Field: Value` or `Field Value`
- Download template to see correct format

**Some fields missing?**
- The app will show which fields weren't found
- You can manually enter missing fields
- Check spelling of field names

**File not uploading?**
- Make sure it's a `.docx` file (not `.doc`)
- Check file isn't corrupted
- Try re-saving the file

## 🎯 Benefits

- ⚡ **Faster** - No manual typing
- ✅ **Accurate** - Reduces input errors
- 📄 **Documented** - Keep patient records in DOCX format
- 🔄 **Reusable** - Use same format for multiple patients

## 📝 Example Document Format

```
Patient Information Form

Age: 50
Sex: Female
Chest Pain Type: Typical Angina
Resting Blood Pressure: 120
Cholesterol: 200
Fasting Blood Sugar: No
Resting ECG: Normal
Maximum Heart Rate: 150
Exercise Angina: No
ST Depression: 1.0
Slope: Upsloping
Major Vessels: 0
Thalassemia: Normal
```

That's it! The app will automatically extract all values and show results! 🎉

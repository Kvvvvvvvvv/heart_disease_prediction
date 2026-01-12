"""
Helper script to run Streamlit with proper error handling
"""
import subprocess
import sys
import os

print("=" * 60)
print("Starting Heart Disease Prediction Web App")
print("=" * 60)
print()

# Check if model exists
if not os.path.exists("heart_disease_model.pkl"):
    print("ERROR: Model file not found!")
    print("Please run: python train_and_save_model.py")
    sys.exit(1)

if not os.path.exists("feature_names.json"):
    print("ERROR: Feature names file not found!")
    print("Please run: python train_and_save_model.py")
    sys.exit(1)

print("Model files found. Starting Streamlit...")
print()
print("The app will open in your browser.")
print("If it doesn't, look for a URL in the output below.")
print("Press Ctrl+C to stop the server.")
print()
print("-" * 60)
print()

# Run streamlit
try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/app/app.py"], check=True)
except KeyboardInterrupt:
    print("\n\nServer stopped by user.")
except subprocess.CalledProcessError as e:
    print(f"\nERROR: Failed to start Streamlit: {e}")
    print("\nTry running manually: streamlit run app.py")
except Exception as e:
    print(f"\nERROR: {e}")

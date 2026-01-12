"""
Simple script to run the Heart Disease Prediction project
Just run: python run_project.py
"""
import json
import sys

print("=" * 60)
print("Heart Disease Prediction Project - Running Notebook")
print("=" * 60)

# Read the notebook
try:
    with open('UCI-heart-disease.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
except FileNotFoundError:
    print("ERROR: UCI-heart-disease.ipynb not found!")
    sys.exit(1)

# Extract and combine all code cells
code_cells = []
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        # Skip magic commands that won't work in regular Python
        if '%matplotlib inline' in source:
            source = source.replace('%matplotlib inline', '')
        if source.strip():  # Only add non-empty cells
            code_cells.append(source)

# Combine all code into one script
full_code = '\n\n# ===== CELL SEPARATOR =====\n\n'.join(code_cells)

print(f"\nExecuting {len(code_cells)} code cells...\n")
print("-" * 60)

# Execute the code
try:
    exec(compile(full_code, 'UCI-heart-disease.ipynb', 'exec'))
    print("\n" + "=" * 60)
    print("SUCCESS! Project execution completed.")
    print("=" * 60)
except Exception as e:
    print(f"\nERROR during execution: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

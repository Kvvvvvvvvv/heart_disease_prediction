#!/usr/bin/env python3
"""
Medical Dashboard Application
This script runs the premium role-based medical web application with:
- User/Doctor/Admin dashboards
- Real-time chat functionality
- Heart disease prediction integration
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'flask',
        'numpy', 
        'pandas',
        'scikit_learn',
        'joblib',
        'sqlite3'  # Built-in module
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'scikit_learn':
                import sklearn
            elif package == 'sqlite3':
                import sqlite3
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def check_model_files():
    """Check if required model files exist."""
    required_files = [
        'heart_disease_model.pkl',
        'feature_names.json'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Missing required model files: {', '.join(missing_files)}")
        print("Please ensure the model files are in the project root directory.")
        return False
    
    return True

def main():
    """Main function to run the medical dashboard application."""
    print("🏥 Starting Medical Dashboard Application...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check model files
    if not check_model_files():
        sys.exit(1)
    
    print("✅ All dependencies and model files are present!")
    print()
    
    try:
        # Import and run the main application
        from main_app import app, init_db
        
        print("🔧 Initializing database...")
        init_db()
        print("✅ Database initialized successfully!")
        print()
        
        print("🌐 Starting Flask server...")
        print("Access the application at:")
        print("  - User Dashboard: http://localhost:5000/user")
        print("  - Doctor Dashboard: http://localhost:5000/doctor") 
        print("  - Admin Dashboard: http://localhost:5000/admin")
        print("  - Login: http://localhost:5000/login")
        print()
        print("Demo Credentials:")
        print("  - Admin: admin / admin123")
        print("  - Doctor: doctor1 / doctor123")
        print("  - User: user1 / user123")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting the application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
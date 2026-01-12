# Heart Disease Prediction System

A comprehensive machine learning application for predicting heart disease risk based on patient medical attributes. Features an interactive web interface with 3D visualization, clinical explanations, and model interpretability.

## 🚀 Features

- **Machine Learning Model**: Random Forest classifier with leak-free pipeline
- **Interactive Web Interface**: Built with Streamlit
- **3D Heart Visualization**: Realistic 3D heart model with risk mapping
- **Clinical Decision Support**: Ollama-powered clinical explanations
- **Feature Importance**: Model interpretability and insights
- **Document Parsing**: DOCX patient data import capability
- **Model Performance**: ~85% accuracy, ~0.91 ROC AUC

## 📋 Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

## 🛠️ Installation & Setup

### Method 1: Local Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd heart-disease-prediction
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Train the model (if not already present):
   ```bash
   python src/models/train_model_leak_free.py
   ```

5. Run the application:
   ```bash
   streamlit run src/app/app_enhanced.py
   ```

### Method 2: Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t heart-disease-prediction .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 heart-disease-prediction
   ```

## 📁 Project Structure

```
heart-disease-prediction/
├── src/                    # Source code
│   ├── app/                # Application files
│   │   ├── app.py          # Basic Streamlit app
│   │   └── app_enhanced.py # Enhanced app with all features
│   ├── models/             # Model training and management
│   │   ├── train_model_leak_free.py
│   │   └── train_and_save_model.py
│   └── utils/              # Utility functions
│       ├── docx_parser.py
│       ├── ollama_integration.py
│       ├── visualization_3d.py
│       └── ...             # Other utilities
├── data/                   # Data files and models
├── docs/                   # Documentation
├── tests/                  # Test files
├── config.py               # Configuration settings
├── Dockerfile              # Container configuration
├── requirements.txt        # Dependencies
└── README.md
```

## 🔧 Configuration

Environment variables can be set to customize the application:

- `API_HOST`: Host address (default: 0.0.0.0)
- `API_PORT`: Port number (default: 8501)
- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)

## 🧪 Running Tests

Execute the test suite:

```bash
python -m pytest tests/
```

## 🚢 Production Deployment

For production deployments, consider:

1. Using environment variables for configuration
2. Setting up a reverse proxy (nginx/Apache)
3. Implementing proper logging
4. Securing the application
5. Monitoring and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is intended for educational and research purposes only. It does not constitute medical advice and should not be used as a substitute for professional medical consultation. Always consult qualified healthcare professionals for medical decisions.

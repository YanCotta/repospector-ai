# Getting Started with RepoSpector AI

## Quick Start Guide

Follow these steps to get RepoSpector AI running on your local machine:

### 1. Clone the Repository
```bash
git clone https://github.com/YanCotta/repospector-ai.git
cd repospector-ai
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt

# Install the package in development mode
pip install -e .
```

### 4. Configure API Keys
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

### 6. Open Your Browser
Navigate to `http://localhost:8501` and start analyzing repositories!

## Features Overview

- **🤖 Multi-Agent Analysis**: Three specialized AI agents working together
- **📊 Visual Dashboard**: Beautiful Streamlit web interface
- **🔒 Secure**: Environment-based API key management
- **📈 Detailed Reports**: Comprehensive analysis with actionable insights

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you've activated the virtual environment
2. **API Key Issues**: Verify your OpenAI API key is correctly set in the sidebar
3. **Network Issues**: Ensure you have internet access for GitHub repo cloning

For more help, check the main README.md or open an issue on GitHub.

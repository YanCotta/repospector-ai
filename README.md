# 🔍 RepoSpector AI

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI Pipeline](https://github.com/YanCotta/repospector-ai/workflows/CI%20Pipeline/badge.svg)](https://github.com/YanCotta/repospector-ai/actions)

An AI-powered multi-agent system built with CrewAI that automatically reviews GitHub repositories. Get expert-level feedback on your code structure, documentation, and best practices.

## 🎯 Project Status

- ✅ **Production Ready**: Full CI/CD pipeline with automated testing
- ✅ **Type Safe**: Complete MyPy type checking with Python 3.12+ support
- ✅ **Code Quality**: Automated formatting with Black and linting with Ruff
- ✅ **Well Tested**: Comprehensive test suite with coverage reporting
- ✅ **Modern Standards**: Pre-commit hooks and professional development workflow

## ✨ Features

- 🤖 **Multi-Agent Analysis**: Three specialized AI agents (RepoAnalyst, DocumentationSpecialist, ChiefReviewer)
- 📊 **Comprehensive Reports**: Detailed markdown reports with scores, strengths, and improvement suggestions
- 🔧 **Professional Structure**: Clean architecture with proper logging, configuration, and error handling
- �️ **Modern Web Interface**: Beautiful Streamlit dashboard with real-time progress tracking
- 🔒 **Secure**: Environment-based API key management
- 🧪 **Well-Tested**: Comprehensive unit tests with coverage reporting

## 🏗️ Architecture

### AI Agents
- **RepoAnalyst**: Senior Software Engineer specializing in code repository structure analysis
- **DocumentationSpecialist**: Technical Writer focused on README evaluation and documentation quality
- **ChiefReviewer**: Principal Engineer who synthesizes findings into actionable reports

### Technology Stack
- **CrewAI**: Multi-agent orchestration framework
- **LangChain**: LLM integration and tooling
- **OpenAI GPT-4**: Advanced language model for analysis
- **Streamlit**: Modern web framework for interactive dashboards
- **Pydantic**: Data validation and settings management

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YanCotta/repospector-ai.git
   cd repospector-ai
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

### Usage

**Start the web application:**
```bash
streamlit run app.py
```

**Open your browser and go to:**
```
http://localhost:8501
```

**Enter your OpenAI API key in the sidebar and paste a GitHub repository URL to analyze!**

## 📋 Requirements

### API Keys Required
- **OpenAI API Key**: Required for LLM analysis
- **SerpAPI Key**: Optional, for enhanced web search capabilities

### Environment Variables
Create a `.env` file with:
```bash
OPENAI_API_KEY=your_openai_api_key_here
# SERPAPI_API_KEY=your_serpapi_key_here  # Optional
```

## 🧪 Development

### CI/CD Pipeline

This project includes a comprehensive CI/CD pipeline that runs on every push and pull request:

- **Code Quality**: Automated linting, formatting, and type checking
- **Testing**: Full test suite with coverage reporting
- **Security**: Automated security scanning with Bandit and Safety
- **Build**: Package building and distribution validation
- **Docker**: Container build verification

All checks must pass before code can be merged, ensuring high code quality and reliability.

### Running Tests
```bash
# Activate virtual environment
source .venv/bin/activate

# Run tests with coverage
pytest

# Run tests with detailed coverage report
pytest --cov-report=html
```

### Code Quality

```bash
# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/ tests/

# Run linting and auto-fixes
ruff check --fix src/ tests/

# Run type checking
mypy src/

# Run all pre-commit checks
pre-commit run --all-files
```

### Development Installation
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## 📊 Example Output

When you run RepoSpector AI on a repository, you'll get a comprehensive markdown report displayed in the web interface and available for download.

## 🏗️ Project Structure

```text
repospector-ai/
├── app.py                       # Streamlit web application
├── src/repospector_ai/          # Main source code
│   ├── __init__.py
│   ├── agents.py                # CrewAI agents
│   ├── tasks.py                 # CrewAI tasks
│   ├── core/                    # Core utilities
│   │   ├── config.py            # Configuration management
│   │   └── logger.py            # Centralized logging
│   └── tools/                   # Custom tools
│       └── repo_analysis_tool.py # Repository analysis
├── tests/                       # Unit tests
│   ├── test_config.py           # Configuration tests
│   ├── test_logger.py           # Logging tests
│   └── test_init.py             # Package tests
├── docs/                        # Documentation
├── .github/workflows/           # CI/CD pipeline
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── .pre-commit-config.yaml      # Code quality hooks
├── Dockerfile                   # Container configuration
├── pyproject.toml               # Modern Python configuration
├── requirements.txt             # Core dependencies
├── requirements-dev.txt         # Development dependencies
└── setup.py                     # Package configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI) for multi-agent orchestration
- Powered by [OpenAI GPT-4](https://openai.com/) for intelligent analysis
- Web interface built with [Streamlit](https://streamlit.io/) for modern dashboards

---

**Made with ❤️ by [YanCotta](https://github.com/YanCotta)**

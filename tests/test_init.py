"""
Unit tests for __init__.py module.
"""

import pytest
from pathlib import Path


def test_package_structure():
    """Test that package structure exists."""
    base_path = Path(__file__).parent.parent / "src" / "repospector_ai"
    
    assert base_path.exists()
    assert (base_path / "__init__.py").exists()
    assert (base_path / "agents.py").exists()
    assert (base_path / "tasks.py").exists()
    assert (base_path / "core").exists()
    assert (base_path / "tools").exists()


def test_package_metadata():
    """Test that package metadata is correctly defined."""
    try:
        import repospector_ai
        
        assert hasattr(repospector_ai, "__version__")
        assert hasattr(repospector_ai, "__author__")
        assert hasattr(repospector_ai, "__email__")
        
        assert repospector_ai.__version__ == "0.1.0"
        assert repospector_ai.__author__ == "YanCotta"
        assert repospector_ai.__email__ == "yancotta@example.com"
        
    except ImportError as e:
        pytest.skip(f"Package import failed: {e}")


def test_module_docstring():
    """Test that module has proper docstring."""
    try:
        import repospector_ai
        
        assert repospector_ai.__doc__ is not None
        assert "RepoSpector AI" in repospector_ai.__doc__
        assert "multi-agent system" in repospector_ai.__doc__
        
    except ImportError as e:
        pytest.skip(f"Package import failed: {e}")


def test_core_modules_exist():
    """Test that core modules exist as files."""
    base_path = Path(__file__).parent.parent / "src" / "repospector_ai"
    
    # Check core module files exist
    assert (base_path / "core" / "__init__.py").exists()
    assert (base_path / "core" / "config.py").exists()
    assert (base_path / "core" / "logger.py").exists()
    
    # Check tools module files exist  
    assert (base_path / "tools" / "__init__.py").exists()
    assert (base_path / "tools" / "repo_analysis_tool.py").exists()


def test_application_files_exist():
    """Test that main application files exist."""
    base_path = Path(__file__).parent.parent
    
    # Check main application files
    assert (base_path / "app.py").exists()
    assert (base_path / "requirements.txt").exists()
    assert (base_path / "setup.py").exists()
    assert (base_path / "README.md").exists()
    assert (base_path / ".env.example").exists()

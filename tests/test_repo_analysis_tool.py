"""
Unit tests for the repository analysis tool.
"""

import json
import tempfile
import unittest.mock
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from git.exc import GitCommandError

from repospector_ai.tools.repo_analysis_tool import analyze_repository_contents


class TestRepositoryAnalysisTool:
    """Test cases for the repository analysis tool."""

    def test_analyze_repository_success(self):
        """Test successful repository analysis with all files present."""
        # Mock data
        mock_readme_content = "# Test Repository\nThis is a test repository."
        mock_license_content = "MIT License\nCopyright (c) 2024"
        
        with patch("repospector_ai.tools.repo_analysis_tool.Repo") as mock_repo_class, \
             patch("tempfile.mkdtemp") as mock_mkdtemp, \
             patch("shutil.rmtree") as mock_rmtree, \
             patch("pathlib.Path.exists") as mock_exists, \
             patch("pathlib.Path.read_text") as mock_read_text:
            
            # Setup mocks
            mock_temp_dir = "/tmp/test_repo"
            mock_mkdtemp.return_value = mock_temp_dir
            mock_repo = MagicMock()
            mock_repo_class.clone_from.return_value = mock_repo
            
            # Mock file existence
            def mock_exists_side_effect(path):
                path_str = str(path)
                return any(file in path_str for file in [
                    "README.md", "LICENSE", ".gitignore", "pyproject.toml", 
                    "src", "tests", "docs"
                ])
            
            mock_exists.side_effect = mock_exists_side_effect
            
            # Mock file reading
            def mock_read_text_side_effect():
                if "README.md" in str(mock_read_text.call_args[0][0]):
                    return mock_readme_content
                elif "LICENSE" in str(mock_read_text.call_args[0][0]):
                    return mock_license_content
                return ""
            
            mock_read_text.side_effect = mock_read_text_side_effect
            
            # Execute the function
            result = analyze_repository_contents("https://github.com/test/repo.git")
            
            # Parse the JSON result
            result_data = json.loads(result)
            
            # Assertions
            assert "readme_content" in result_data
            assert "license_content" in result_data
            assert "structure_analysis" in result_data
            
            structure = result_data["structure_analysis"]
            assert structure["has_readme"] is True
            assert structure["has_license"] is True
            assert structure["has_gitignore"] is True
            assert structure["has_pyproject_toml"] is True
            assert structure["has_src_directory"] is True
            assert structure["has_tests_directory"] is True
            assert structure["has_docs_directory"] is True
            
            # Verify cleanup was called
            mock_rmtree.assert_called_once_with(mock_temp_dir)

    def test_analyze_repository_invalid_url(self):
        """Test behavior with invalid GitHub URL."""
        with patch("repospector_ai.tools.repo_analysis_tool.Repo") as mock_repo_class, \
             patch("tempfile.mkdtemp") as mock_mkdtemp, \
             patch("shutil.rmtree") as mock_rmtree:
            
            mock_temp_dir = "/tmp/test_repo"
            mock_mkdtemp.return_value = mock_temp_dir
            mock_repo_class.clone_from.side_effect = GitCommandError("git clone", 128)
            
            # Execute the function
            result = analyze_repository_contents("https://invalid-url.com/repo.git")
            
            # Parse the JSON result
            result_data = json.loads(result)
            
            # Assertions
            assert "error" in result_data
            assert "Failed to clone repository" in result_data["error"]
            
            # Verify cleanup was called even on error
            mock_rmtree.assert_called_once_with(mock_temp_dir)

    def test_analyze_repository_missing_readme(self):
        """Test behavior when README.md is missing."""
        with patch("repospector_ai.tools.repo_analysis_tool.Repo") as mock_repo_class, \
             patch("tempfile.mkdtemp") as mock_mkdtemp, \
             patch("shutil.rmtree") as mock_rmtree, \
             patch("pathlib.Path.exists") as mock_exists, \
             patch("pathlib.Path.read_text") as mock_read_text:
            
            mock_temp_dir = "/tmp/test_repo"
            mock_mkdtemp.return_value = mock_temp_dir
            mock_repo = MagicMock()
            mock_repo_class.clone_from.return_value = mock_repo
            
            # Mock file existence - README.md is missing
            def mock_exists_side_effect(path):
                path_str = str(path)
                if "README.md" in path_str:
                    return False
                return any(file in path_str for file in [
                    "LICENSE", ".gitignore", "pyproject.toml"
                ])
            
            mock_exists.side_effect = mock_exists_side_effect
            mock_read_text.return_value = "MIT License"
            
            # Execute the function
            result = analyze_repository_contents("https://github.com/test/repo.git")
            
            # Parse the JSON result
            result_data = json.loads(result)
            
            # Assertions
            assert result_data["readme_content"] == ""
            assert result_data["structure_analysis"]["has_readme"] is False
            assert result_data["structure_analysis"]["has_license"] is True

    def test_analyze_repository_file_read_error(self):
        """Test behavior when file reading fails."""
        with patch("repospector_ai.tools.repo_analysis_tool.Repo") as mock_repo_class, \
             patch("tempfile.mkdtemp") as mock_mkdtemp, \
             patch("shutil.rmtree") as mock_rmtree, \
             patch("pathlib.Path.exists") as mock_exists, \
             patch("pathlib.Path.read_text") as mock_read_text:
            
            mock_temp_dir = "/tmp/test_repo"
            mock_mkdtemp.return_value = mock_temp_dir
            mock_repo = MagicMock()
            mock_repo_class.clone_from.return_value = mock_repo
            
            mock_exists.return_value = True
            mock_read_text.side_effect = PermissionError("Permission denied")
            
            # Execute the function
            result = analyze_repository_contents("https://github.com/test/repo.git")
            
            # Parse the JSON result
            result_data = json.loads(result)
            
            # Should handle the error gracefully
            assert "readme_content" in result_data
            assert "license_content" in result_data
            
            # Verify cleanup was called
            mock_rmtree.assert_called_once_with(mock_temp_dir)

    def test_analyze_repository_cleanup_on_exception(self):
        """Test that cleanup happens even when unexpected exceptions occur."""
        with patch("repospector_ai.tools.repo_analysis_tool.Repo") as mock_repo_class, \
             patch("tempfile.mkdtemp") as mock_mkdtemp, \
             patch("shutil.rmtree") as mock_rmtree:
            
            mock_temp_dir = "/tmp/test_repo"
            mock_mkdtemp.return_value = mock_temp_dir
            mock_repo_class.clone_from.side_effect = Exception("Unexpected error")
            
            # Execute the function
            result = analyze_repository_contents("https://github.com/test/repo.git")
            
            # Parse the JSON result
            result_data = json.loads(result)
            
            # Should return an error
            assert "error" in result_data
            
            # Verify cleanup was called even on unexpected error
            mock_rmtree.assert_called_once_with(mock_temp_dir)

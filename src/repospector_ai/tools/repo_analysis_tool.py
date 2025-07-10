"""
Repository analysis tool for RepoSpector AI.

This module provides a custom LangChain tool for comprehensive GitHub repository
analysis including structure inspection and content extraction.
"""

import json
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

from git import Repo, GitCommandError
from langchain.tools import tool

from repospector_ai.core.config import settings
from repospector_ai.core.logger import get_logger

logger = get_logger(__name__)


def _analyze_project_structure(repo_path: Path) -> Dict[str, bool]:
    """
    Analyze the project structure and identify key files and directories.
    
    Args:
        repo_path: Path to the cloned repository
        
    Returns:
        Dictionary with boolean flags for presence of key files/directories
    """
    structure_analysis = {
        "has_readme": False,
        "has_license": False,
        "has_gitignore": False,
        "has_requirements_txt": False,
        "has_pyproject_toml": False,
        "has_package_json": False,
        "has_dockerfile": False,
        "has_src_directory": False,
        "has_tests_directory": False,
        "has_docs_directory": False,
        "has_ci_cd": False,
    }
    
    try:
        # Check for files in root directory
        root_files = [f.name.lower() for f in repo_path.iterdir() if f.is_file()]
        root_dirs = [d.name.lower() for d in repo_path.iterdir() if d.is_dir()]
        
        # File checks
        structure_analysis["has_readme"] = any(
            f.startswith("readme") for f in root_files
        )
        structure_analysis["has_license"] = any(
            f.startswith("license") or f.startswith("licence") for f in root_files
        )
        structure_analysis["has_gitignore"] = ".gitignore" in root_files
        structure_analysis["has_requirements_txt"] = "requirements.txt" in root_files
        structure_analysis["has_pyproject_toml"] = "pyproject.toml" in root_files
        structure_analysis["has_package_json"] = "package.json" in root_files
        structure_analysis["has_dockerfile"] = "dockerfile" in root_files
        
        # Directory checks
        structure_analysis["has_src_directory"] = "src" in root_dirs
        structure_analysis["has_tests_directory"] = any(
            d in root_dirs for d in ["tests", "test", "__tests__"]
        )
        structure_analysis["has_docs_directory"] = any(
            d in root_dirs for d in ["docs", "doc", "documentation"]
        )
        structure_analysis["has_ci_cd"] = any(
            d in root_dirs for d in [".github", ".gitlab-ci", ".circleci", "ci"]
        )
        
        logger.info(f"Structure analysis completed: {structure_analysis}")
        
    except Exception as e:
        logger.error(f"Error analyzing project structure: {e}")
    
    return structure_analysis


def _read_file_content(file_path: Path, max_size_kb: int = None) -> Optional[str]:
    """
    Safely read file content with size limits.
    
    Args:
        file_path: Path to the file to read
        max_size_kb: Maximum file size in KB to read
        
    Returns:
        File content as string or None if file cannot be read
    """
    if max_size_kb is None:
        max_size_kb = settings.max_file_size_kb
    
    try:
        # Check file size
        if file_path.stat().st_size > max_size_kb * 1024:
            logger.warning(f"File {file_path} exceeds size limit ({max_size_kb}KB)")
            return f"[File too large - {file_path.stat().st_size / 1024:.1f}KB]"
        
        # Read file content
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        logger.debug(f"Successfully read file: {file_path}")
        return content
        
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None


def _find_readme_file(repo_path: Path) -> Optional[Path]:
    """Find README file with various extensions."""
    readme_patterns = ["readme", "readme.md", "readme.txt", "readme.rst"]
    
    for file in repo_path.iterdir():
        if file.is_file() and file.name.lower() in readme_patterns:
            return file
    
    return None


def _find_license_file(repo_path: Path) -> Optional[Path]:
    """Find LICENSE file with various extensions."""
    license_patterns = ["license", "licence", "license.md", "license.txt", "licence.txt"]
    
    for file in repo_path.iterdir():
        if file.is_file() and file.name.lower() in license_patterns:
            return file
    
    return None


@tool
def analyze_repository_contents(github_url: str) -> str:
    """
    Analyze a GitHub repository's structure, files, and content.
    
    This tool clones a GitHub repository and performs comprehensive analysis including:
    - Repository structure inspection (presence of key files and directories)
    - README content extraction and analysis
    - LICENSE content extraction
    - Project metadata collection
    
    Args:
        github_url: The GitHub repository URL to analyze
        
    Returns:
        JSON string containing structured analysis results with keys:
        - readme_content: Full text of README file (if exists)
        - license_content: Full text of LICENSE file (if exists)  
        - structure_analysis: Dictionary with boolean flags for key project files/dirs
        - metadata: Additional repository metadata
    """
    temp_dir = None
    
    try:
        logger.info(f"Starting analysis of repository: {github_url}")
        
        # Validate URL format
        if not github_url.startswith(("https://github.com/", "http://github.com/")):
            error_msg = f"Invalid GitHub URL format: {github_url}"
            logger.error(error_msg)
            return json.dumps({
                "error": error_msg,
                "readme_content": None,
                "license_content": None,
                "structure_analysis": {},
                "metadata": {}
            })
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp(prefix=settings.temp_dir_prefix)
        temp_path = Path(temp_dir)
        
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Clone repository
        try:
            repo = Repo.clone_from(github_url, temp_path, depth=1)
            logger.info(f"Successfully cloned repository to {temp_path}")
        except GitCommandError as e:
            error_msg = f"Failed to clone repository: {e}"
            logger.error(error_msg)
            return json.dumps({
                "error": error_msg,
                "readme_content": None,
                "license_content": None,
                "structure_analysis": {},
                "metadata": {}
            })
        
        # Analyze repository structure
        structure_analysis = _analyze_project_structure(temp_path)
        
        # Read README content
        readme_content = None
        readme_file = _find_readme_file(temp_path)
        if readme_file:
            readme_content = _read_file_content(readme_file)
            logger.info(f"README file found and read: {readme_file.name}")
        else:
            logger.warning("No README file found in repository")
        
        # Read LICENSE content
        license_content = None
        license_file = _find_license_file(temp_path)
        if license_file:
            license_content = _read_file_content(license_file)
            logger.info(f"LICENSE file found and read: {license_file.name}")
        else:
            logger.warning("No LICENSE file found in repository")
        
        # Collect metadata
        metadata = {
            "repository_url": github_url,
            "cloned_successfully": True,
            "temp_directory": str(temp_path),
            "total_files": len(list(temp_path.rglob("*"))),
            "readme_file_name": readme_file.name if readme_file else None,
            "license_file_name": license_file.name if license_file else None,
        }
        
        # Prepare result
        result = {
            "readme_content": readme_content,
            "license_content": license_content,
            "structure_analysis": structure_analysis,
            "metadata": metadata
        }
        
        logger.info("Repository analysis completed successfully")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        error_msg = f"Unexpected error during repository analysis: {e}"
        logger.error(error_msg, exc_info=True)
        return json.dumps({
            "error": error_msg,
            "readme_content": None,
            "license_content": None,
            "structure_analysis": {},
            "metadata": {}
        })
        
    finally:
        # Cleanup temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.error(f"Failed to cleanup temporary directory {temp_dir}: {e}")

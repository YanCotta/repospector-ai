"""
Unit tests for the tasks module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

from repospector_ai.tasks import (
    create_structure_analysis_task,
    create_documentation_review_task,
    create_final_report_task,
    create_crew,
)


class TestTaskCreation:
    """Test task creation functions."""

    @patch("repospector_ai.tasks.Task")
    def test_create_structure_analysis_task(self, mock_task):
        """Test structure analysis task creation."""
        mock_agent = Mock()
        mock_task_instance = Mock()
        mock_task.return_value = mock_task_instance
        
        task = create_structure_analysis_task(mock_agent)
        
        mock_task.assert_called_once()
        args, kwargs = mock_task.call_args
        
        assert "analyze the repository structure" in kwargs["description"].lower()
        assert kwargs["agent"] == mock_agent
        assert kwargs["expected_output"] is not None

    @patch("repospector_ai.tasks.Task")
    def test_create_documentation_review_task(self, mock_task):
        """Test documentation review task creation."""
        mock_agent = Mock()
        mock_context_task = Mock()
        mock_task_instance = Mock()
        mock_task.return_value = mock_task_instance
        
        task = create_documentation_review_task(mock_agent, mock_context_task)
        
        mock_task.assert_called_once()
        args, kwargs = mock_task.call_args
        
        assert "review the documentation quality" in kwargs["description"].lower()
        assert kwargs["agent"] == mock_agent
        assert kwargs["context"] == [mock_context_task]
        assert kwargs["expected_output"] is not None

    @patch("repospector_ai.tasks.Task")
    def test_create_final_report_task(self, mock_task):
        """Test final report task creation."""
        mock_agent = Mock()
        mock_context_tasks = [Mock(), Mock()]
        mock_task_instance = Mock()
        mock_task.return_value = mock_task_instance
        
        task = create_final_report_task(mock_agent, mock_context_tasks)
        
        mock_task.assert_called_once()
        args, kwargs = mock_task.call_args
        
        assert "compile all findings" in kwargs["description"].lower()
        assert kwargs["agent"] == mock_agent
        assert kwargs["context"] == mock_context_tasks
        assert kwargs["expected_output"] is not None
        assert "markdown report" in kwargs["expected_output"].lower()


class TestCrewCreation:
    """Test crew creation and orchestration."""

    @patch("repospector_ai.tasks.Crew")
    @patch("repospector_ai.tasks.create_repo_analyst")
    @patch("repospector_ai.tasks.create_documentation_specialist")
    @patch("repospector_ai.tasks.create_chief_reviewer")
    def test_create_crew_success(self, mock_chief, mock_doc, mock_analyst, mock_crew):
        """Test successful crew creation."""
        # Mock agents
        mock_analyst_agent = Mock()
        mock_doc_agent = Mock()
        mock_chief_agent = Mock()
        
        mock_analyst.return_value = mock_analyst_agent
        mock_doc.return_value = mock_doc_agent
        mock_chief.return_value = mock_chief_agent
        
        # Mock crew instance
        mock_crew_instance = Mock()
        mock_crew.return_value = mock_crew_instance
        
        github_url = "https://github.com/test/repo"
        crew = create_crew(github_url)
        
        # Verify agents were created
        mock_analyst.assert_called_once()
        mock_doc.assert_called_once()
        mock_chief.assert_called_once()
        
        # Verify crew was created with agents and tasks
        mock_crew.assert_called_once()
        args, kwargs = mock_crew.call_args
        
        assert "agents" in kwargs
        assert "tasks" in kwargs
        assert len(kwargs["agents"]) == 3
        assert len(kwargs["tasks"]) == 3
        assert kwargs["verbose"] is True

    def test_create_crew_invalid_url(self):
        """Test crew creation with invalid GitHub URL."""
        invalid_urls = [
            "",
            "not-a-url",
            "https://google.com",
            "ftp://github.com/test/repo",
        ]
        
        for url in invalid_urls:
            with pytest.raises((ValueError, AssertionError)):
                create_crew(url)

    @patch("repospector_ai.tasks.logger")
    def test_create_crew_logs_creation(self, mock_logger):
        """Test that crew creation is properly logged."""
        with patch("repospector_ai.tasks.Crew"), \
             patch("repospector_ai.tasks.create_repo_analyst"), \
             patch("repospector_ai.tasks.create_documentation_specialist"), \
             patch("repospector_ai.tasks.create_chief_reviewer"):
            
            github_url = "https://github.com/test/repo"
            crew = create_crew(github_url)
            
            # Verify logging calls
            assert mock_logger.info.called


class TestTaskIntegration:
    """Test task integration and workflow."""

    @patch("repospector_ai.tasks.create_repo_analyst")
    @patch("repospector_ai.tasks.create_documentation_specialist") 
    @patch("repospector_ai.tasks.create_chief_reviewer")
    def test_task_context_flow(self, mock_chief, mock_doc, mock_analyst):
        """Test that tasks are properly connected with context."""
        # Setup mocks
        mock_analyst_agent = Mock()
        mock_doc_agent = Mock() 
        mock_chief_agent = Mock()
        
        mock_analyst.return_value = mock_analyst_agent
        mock_doc.return_value = mock_doc_agent
        mock_chief.return_value = mock_chief_agent
        
        with patch("repospector_ai.tasks.Crew") as mock_crew, \
             patch("repospector_ai.tasks.Task") as mock_task:
            
            mock_task_instances = [Mock(), Mock(), Mock()]
            mock_task.side_effect = mock_task_instances
            
            github_url = "https://github.com/test/repo"
            crew = create_crew(github_url)
            
            # Verify tasks are created in correct order with context
            assert mock_task.call_count == 3
            
            # Check that documentation task has structure task as context
            doc_task_call = mock_task.call_args_list[1]
            doc_kwargs = doc_task_call[1]
            assert "context" in doc_kwargs
            assert doc_kwargs["context"] == [mock_task_instances[0]]
            
            # Check that final task has both previous tasks as context
            final_task_call = mock_task.call_args_list[2]
            final_kwargs = final_task_call[1]
            assert "context" in final_kwargs
            assert len(final_kwargs["context"]) == 2

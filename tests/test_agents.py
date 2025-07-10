"""
Unit tests for the agents module.
"""

import pytest
from unittest.mock import Mock, patch

from repospector_ai.agents import (
    create_repo_analyst,
    create_documentation_specialist,
    create_chief_reviewer,
)


class TestAgentCreation:
    """Test agent creation functions."""

    @patch("repospector_ai.agents.Agent")
    @patch("repospector_ai.agents.analyze_repository_contents")
    def test_create_repo_analyst(self, mock_tool, mock_agent):
        """Test RepoAnalyst agent creation."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        agent = create_repo_analyst()
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        assert kwargs["role"] == "Senior Software Engineer specializing in code repository structure"
        assert "rigorously analyze" in kwargs["goal"].lower()
        assert "thousands of repositories" in kwargs["backstory"]
        assert kwargs["verbose"] is True
        assert kwargs["allow_delegation"] is False
        assert kwargs["tools"] == [mock_tool]

    @patch("repospector_ai.agents.Agent")
    @patch("repospector_ai.agents.SerpAPIWrapper")
    def test_create_documentation_specialist(self, mock_serp, mock_agent):
        """Test DocumentationSpecialist agent creation."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        mock_serp_instance = Mock()
        mock_serp.return_value = mock_serp_instance
        
        agent = create_documentation_specialist()
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        assert kwargs["role"] == "Technical Writer and Documentation Expert"
        assert "scrutinize" in kwargs["goal"].lower()
        assert "great code is useless without great documentation" in kwargs["backstory"]
        assert kwargs["verbose"] is True
        assert kwargs["allow_delegation"] is False

    @patch("repospector_ai.agents.Agent")
    def test_create_chief_reviewer(self, mock_agent):
        """Test ChiefReviewer agent creation."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        agent = create_chief_reviewer()
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        assert kwargs["role"] == "Principal AI Engineer and Project Lead"
        assert "synthesize" in kwargs["goal"].lower()
        assert "final gatekeeper for quality" in kwargs["backstory"]
        assert kwargs["verbose"] is True
        assert kwargs["allow_delegation"] is False
        assert kwargs["tools"] == []

    @patch("repospector_ai.agents.settings")
    def test_agents_use_correct_llm_model(self, mock_settings):
        """Test that agents use the configured LLM model."""
        mock_settings.openai_model_name = "gpt-4"
        
        with patch("repospector_ai.agents.Agent") as mock_agent:
            create_repo_analyst()
            
            # Check that the LLM configuration is passed
            args, kwargs = mock_agent.call_args
            assert "llm" in kwargs or len(args) > 0

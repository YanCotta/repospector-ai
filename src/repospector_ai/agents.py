"""
CrewAI agents for RepoSpector AI.

This module defines the expert AI agents responsible for comprehensive
GitHub repository analysis and review.
"""

from typing import List

from crewai import Agent
from langchain_community.utilities import SerpAPIWrapper
from langchain_openai import ChatOpenAI

from repospector_ai.core.config import settings
from repospector_ai.core.logger import get_logger
from repospector_ai.tools.repo_analysis_tool import analyze_repository_contents

logger = get_logger(__name__)


def _create_llm() -> ChatOpenAI:
    """Create and configure the LLM for agents."""
    return ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        openai_api_key=settings.openai_api_key,
    )


def create_repo_analyst() -> Agent:
    """
    Create the Repository Analyst agent.
    
    This agent specializes in analyzing repository structure, identifying
    missing components, and evaluating adherence to professional standards.
    
    Returns:
        Configured RepoAnalyst agent
    """
    logger.info("Creating RepoAnalyst agent")
    
    return Agent(
        role="Senior Software Engineer specializing in code repository structure",
        goal=(
            "Rigorously analyze the structure, files, and metadata of a given "
            "GitHub repository to assess its adherence to professional standards"
        ),
        backstory=(
            "You've reviewed thousands of repositories at top tech companies like "
            "Google, Meta, and Microsoft. You have an eagle eye for identifying "
            "missing documentation, poor structure, and lack of essential "
            "configuration files. You understand what separates amateur projects "
            "from professional-grade repositories. Your analysis is thorough, "
            "objective, and always focused on actionable improvements."
        ),
        tools=[analyze_repository_contents],
        llm=_create_llm(),
        verbose=settings.crew_verbose,
        allow_delegation=False,
        max_iter=3,
        memory=True,
    )


def create_documentation_specialist() -> Agent:
    """
    Create the Documentation Specialist agent.
    
    This agent focuses on evaluating README files, documentation quality,
    and overall project presentation.
    
    Returns:
        Configured DocumentationSpecialist agent
    """
    logger.info("Creating DocumentationSpecialist agent")
    
    # Configure SerpAPI if available
    tools = []
    if settings.serpapi_api_key:
        try:
            serp_tool = SerpAPIWrapper(serpapi_api_key=settings.serpapi_api_key)
            tools.append(serp_tool)
            logger.info("SerpAPI tool configured for DocumentationSpecialist")
        except Exception as e:
            logger.warning(f"Failed to configure SerpAPI: {e}")
    
    return Agent(
        role="Technical Writer and Documentation Expert",
        goal=(
            "Scrutinize the repository's README file for clarity, completeness, "
            "and persuasiveness. Evaluate it against the 'Professional' and "
            "'Elite' tiers of modern repository standards"
        ),
        backstory=(
            "You believe that great code is useless without great documentation. "
            "You've written documentation for major open-source projects and "
            "enterprise software. You know how to transform confusing READMEs "
            "into compelling entry points for new developers and users. You "
            "understand the psychology of first impressions and how documentation "
            "affects adoption. Your reviews are detailed, constructive, and "
            "always include specific examples of improvements."
        ),
        tools=tools,
        llm=_create_llm(),
        verbose=settings.crew_verbose,
        allow_delegation=False,
        max_iter=3,
        memory=True,
    )


def create_chief_reviewer() -> Agent:
    """
    Create the Chief Reviewer agent.
    
    This agent synthesizes findings from other agents and creates the final
    comprehensive report with prioritized recommendations.
    
    Returns:
        Configured ChiefReviewer agent
    """
    logger.info("Creating ChiefReviewer agent")
    
    return Agent(
        role="Principal AI Engineer and Project Lead",
        goal=(
            "Synthesize the analyses from the engineer and technical writer into "
            "a single, comprehensive, and actionable report. Prioritize suggestions "
            "and provide constructive, high-level feedback"
        ),
        backstory=(
            "You are the final gatekeeper for quality at a top-tier technology "
            "company. You've led teams that shipped products used by millions. "
            "You don't just point out flaws; you provide a clear, prioritized "
            "path to excellence. Your feedback is encouraging and immediately "
            "useful. You understand that great software is built iteratively, "
            "and you help developers understand what to focus on first. You "
            "balance technical excellence with practical considerations, always "
            "keeping the end user and maintainability in mind."
        ),
        tools=[],  # ChiefReviewer uses reasoning, not tools
        llm=_create_llm(),
        verbose=settings.crew_verbose,
        allow_delegation=False,
        max_iter=3,
        memory=True,
    )


def get_all_agents() -> List[Agent]:
    """
    Get all configured agents for the repository analysis crew.
    
    Returns:
        List of all agents in the correct order for workflow
    """
    agents = [
        create_repo_analyst(),
        create_documentation_specialist(),
        create_chief_reviewer(),
    ]
    
    logger.info(f"Created {len(agents)} agents for repository analysis")
    return agents

"""
CrewAI tasks and workflow orchestration for RepoSpector AI.

This module defines the specific tasks for each agent and provides
the crew creation and management functionality.
"""

from typing import Any

from crewai import Crew, Task
from crewai.process import Process

from repospector_ai.agents import (
    create_chief_reviewer,
    create_documentation_specialist,
    create_repo_analyst,
)
from repospector_ai.core.config import settings
from repospector_ai.core.logger import get_logger

logger = get_logger(__name__)


def create_structure_analysis_task(repo_analyst: Any) -> Task:
    """
    Create the repository structure analysis task.

    Args:
        repo_analyst: The RepoAnalyst agent

    Returns:
        Configured Task for structure analysis
    """
    return Task(
        description=(
            "Perform a comprehensive structural analysis of the GitHub repository "
            "using your repository analysis tool. Your analysis must include:\n\n"
            "1. **Repository Structure Assessment**: Use the analyze_repository_contents "
            "tool to examine the repository and extract structured data about its "
            "organization, files, and content.\n\n"
            "2. **Professional Standards Evaluation**: Assess the presence and quality of:\n"
            "   - Documentation files (README, LICENSE, CONTRIBUTING)\n"
            "   - Configuration files (requirements.txt, pyproject.toml, package.json)\n"
            "   - Project organization (src/, tests/, docs/ directories)\n"
            "   - Development infrastructure (.gitignore, CI/CD, Docker)\n\n"
            "3. **Structured Output**: Your output must be the complete JSON data "
            "returned by the analyze_repository_contents tool, along with your "
            "professional assessment of what the structure reveals about the "
            "project's maturity and maintainability.\n\n"
            "Focus on being thorough and objective. The structured data you provide "
            "will be used by other agents for deeper analysis."
        ),
        agent=repo_analyst,
        expected_output=(
            "A comprehensive analysis containing the complete JSON output from the "
            "repository analysis tool, plus your professional evaluation of the "
            "repository's structural quality, missing components, and adherence to "
            "industry best practices."
        ),
    )


def create_documentation_review_task(
    documentation_specialist: Any, structure_task: Any
) -> Task:
    """
    Create the documentation review task.

    Args:
        documentation_specialist: The DocumentationSpecialist agent
        structure_task: The structure analysis task (for context)

    Returns:
        Configured Task for documentation review
    """
    return Task(
        description=(
            "Conduct an expert-level review of the repository's documentation, "
            "focusing primarily on the README content provided in the context from "
            "the structure analysis. Your review must cover:\n\n"
            "1. **README Quality Assessment**:\n"
            "   - Project description clarity and completeness\n"
            "   - Installation and usage instructions\n"
            "   - Code examples and demonstrations\n"
            "   - Project structure explanation\n"
            "   - Contribution guidelines and community information\n"
            "   - Professional presentation and formatting\n\n"
            "2. **Documentation Best Practices**:\n"
            "   - Compare against modern repository standards\n"
            "   - Evaluate user experience for new developers\n"
            "   - Assess information architecture and organization\n"
            "   - Check for missing critical sections\n\n"
            "3. **Improvement Recommendations**:\n"
            "   - Specific, actionable suggestions for enhancement\n"
            "   - Examples of excellent documentation patterns\n"
            "   - Prioritized list of missing elements\n\n"
            "If SerpAPI is available, you may research best practices and examples "
            "of excellent repository documentation for comparison."
        ),
        agent=documentation_specialist,
        context=[structure_task],
        expected_output=(
            "A detailed documentation review with specific feedback on README quality, "
            "missing documentation elements, and prioritized recommendations for "
            "improvement. Include examples and references to best practices where applicable."
        ),
    )


def create_final_report_task(
    chief_reviewer: Any, structure_task: Any, documentation_task: Any
) -> Task:
    """
    Create the final comprehensive report task.

    Args:
        chief_reviewer: The ChiefReviewer agent
        structure_task: The structure analysis task (for context)
        documentation_task: The documentation review task (for context)

    Returns:
        Configured Task for final report generation
    """
    return Task(
        description=(
            "Synthesize all findings from the repository structure analysis and "
            "documentation review into a single, elegant, and actionable report. "
            "Your report must be formatted in Markdown and include these exact sections:\n\n"
            "# Repository Analysis Report\n\n"
            "## Overall Score & Summary\n"
            "- Provide an overall quality score (1-10) with justification\n"
            "- Brief executive summary of the repository's current state\n"
            "- Key strengths and primary areas for improvement\n\n"
            "## ✅ What's Good\n"
            "- List and explain the repository's strengths\n"
            "- Highlight professional elements already in place\n"
            "- Acknowledge good practices and quality indicators\n\n"
            "## ⚠️ Areas for Improvement\n"
            "- Identify specific issues and missing components\n"
            "- Explain the impact of each issue on usability/maintainability\n"
            "- Provide context for why each improvement matters\n\n"
            "## 🚀 Action Plan\n"
            "- Prioritized list of recommendations (High/Medium/Low priority)\n"
            "- Specific, actionable steps for each recommendation\n"
            "- Estimated effort level and expected impact\n"
            "- Quick wins vs. long-term improvements\n\n"
            "The tone must be professional, constructive, and encouraging. Focus on "
            "helping the repository owner understand not just what to improve, but "
            "why and how to improve it."
        ),
        agent=chief_reviewer,
        context=[structure_task, documentation_task],
        expected_output=(
            "A comprehensive Markdown report following the specified format with "
            "clear sections for score/summary, strengths, areas for improvement, "
            "and prioritized action plan. The report should be immediately actionable "
            "and professionally presented."
        ),
    )


def create_crew(github_url: str) -> Crew:
    """
    Create and configure the repository analysis crew.

    Args:
        github_url: The GitHub repository URL to analyze

    Returns:
        Configured Crew ready for execution
    """
    logger.info(f"Creating crew for repository analysis: {github_url}")

    # Create agents
    repo_analyst = create_repo_analyst()
    documentation_specialist = create_documentation_specialist()
    chief_reviewer = create_chief_reviewer()

    # Create tasks
    structure_task = create_structure_analysis_task(repo_analyst)
    documentation_task = create_documentation_review_task(
        documentation_specialist, structure_task
    )
    final_report_task = create_final_report_task(
        chief_reviewer, structure_task, documentation_task
    )

    # Configure crew
    crew = Crew(
        agents=[repo_analyst, documentation_specialist, chief_reviewer],
        tasks=[structure_task, documentation_task, final_report_task],
        process=Process.sequential,
        verbose=settings.crew_verbose,
        memory=True,
        embedder={
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small",
                "api_key": settings.openai_api_key,
            },
        },
    )

    logger.info("Repository analysis crew created successfully")
    return crew


def get_crew_tasks() -> list[str]:
    """
    Get a list of task names for monitoring and debugging.

    Returns:
        List of task names in execution order
    """
    return [
        "Repository Structure Analysis",
        "Documentation Review",
        "Final Report Generation",
    ]

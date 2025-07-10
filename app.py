"""
Streamlit web interface for RepoSpector AI.
"""

import streamlit as st
import os
import tempfile
import shutil
from typing import Optional
import traceback

# Configure page
st.set_page_config(
    page_title="🔍 RepoSpector AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    """Load custom CSS styling."""
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-box {
        background: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .error-box {
        background: #f8d7da;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    load_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 RepoSpector AI</h1>
        <p>AI-Powered GitHub Repository Analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        openai_api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Enter your OpenAI API key for AI analysis"
        )
        
        # Optional SerpAPI key
        serpapi_key = st.text_input(
            "SerpAPI Key (Optional)",
            type="password",
            value=os.getenv("SERPAPI_API_KEY", ""),
            help="Optional: For enhanced web search capabilities"
        )
        
        st.markdown("---")
        
        # About section
        st.markdown("""
        ### 📖 About
        RepoSpector AI uses three specialized AI agents:
        
        🤖 **RepoAnalyst**: Analyzes code structure and architecture
        
        📝 **DocumentationSpecialist**: Reviews README and documentation
        
        👨‍💼 **ChiefReviewer**: Synthesizes findings into actionable reports
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Repository Analysis")
        
        # GitHub URL input
        github_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repository-name",
            help="Enter the full GitHub repository URL you want to analyze"
        )
        
        # Analysis button
        if st.button("🚀 Analyze Repository", type="primary", use_container_width=True):
            if not github_url:
                st.error("Please enter a GitHub repository URL")
            elif not openai_api_key:
                st.error("Please provide your OpenAI API key in the sidebar")
            else:
                analyze_repository(github_url, openai_api_key, serpapi_key)
    
    with col2:
        st.header("📊 Features")
        
        st.markdown("""
        <div class="feature-box">
            <h4>🏗️ Structure Analysis</h4>
            <p>Comprehensive code architecture review</p>
        </div>
        
        <div class="feature-box">
            <h4>📚 Documentation Review</h4>
            <p>README and documentation quality assessment</p>
        </div>
        
        <div class="feature-box">
            <h4>⭐ Best Practices</h4>
            <p>Industry standard compliance check</p>
        </div>
        
        <div class="feature-box">
            <h4>📈 Actionable Insights</h4>
            <p>Prioritized improvement recommendations</p>
        </div>
        """, unsafe_allow_html=True)

def analyze_repository(github_url: str, openai_api_key: str, serpapi_key: Optional[str] = None):
    """Analyze the repository using CrewAI agents."""
    
    # Set environment variables
    os.environ["OPENAI_API_KEY"] = openai_api_key
    if serpapi_key:
        os.environ["SERPAPI_API_KEY"] = serpapi_key
    
    try:
        # Import here to avoid issues if dependencies aren't loaded
        from repospector_ai.tasks import create_crew
        
        with st.spinner("🔄 Initializing AI agents..."):
            crew = create_crew(github_url)
        
        with st.spinner("🤖 AI agents are analyzing the repository... This may take a few minutes."):
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Update progress (simulated)
            status_text.text("📥 Cloning repository...")
            progress_bar.progress(20)
            
            status_text.text("🔍 Analyzing code structure...")
            progress_bar.progress(40)
            
            status_text.text("📖 Reviewing documentation...")
            progress_bar.progress(60)
            
            status_text.text("⚡ Generating final report...")
            progress_bar.progress(80)
            
            # Run the crew
            result = crew.kickoff()
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
        
        # Display results
        st.success("🎉 Repository analysis completed successfully!")
        
        # Show the report
        st.header("📋 Analysis Report")
        
        # Display the markdown report
        if isinstance(result, str):
            st.markdown(result)
        else:
            st.markdown(str(result))
        
        # Download button for the report
        if isinstance(result, str):
            st.download_button(
                label="📥 Download Report",
                data=result,
                file_name=f"repository_review_{github_url.split('/')[-1]}.md",
                mime="text/markdown"
            )
        
        st.markdown("""
        <div class="success-box">
            <h4>✅ Analysis Complete</h4>
            <p>Your repository has been thoroughly analyzed by our AI agents. 
            Use the recommendations above to improve your project's quality and professionalism.</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"❌ An error occurred during analysis: {str(e)}")
        
        # Show detailed error in expander for debugging
        with st.expander("🔧 Error Details (for debugging)"):
            st.code(traceback.format_exc())
        
        st.markdown("""
        <div class="error-box">
            <h4>🚨 Troubleshooting Tips</h4>
            <ul>
                <li>Ensure the GitHub URL is valid and publicly accessible</li>
                <li>Check that your OpenAI API key is correct</li>
                <li>Verify your internet connection</li>
                <li>Try with a smaller repository if the analysis times out</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

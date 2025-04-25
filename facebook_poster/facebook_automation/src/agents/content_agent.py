from crewai import Agent
from ..tools.gemini_utils import generate_content
import yaml
import os

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

class ContentAgent:
    """Factory for creating CrewAI agents for content generation."""
    
    @staticmethod
    def create_content_creator():
        """Create an agent that generates content."""
        return Agent(
            role="Content Creator",
            goal="Create engaging and relevant content for Facebook posts",
            backstory="I am an expert content creator with a knack for creating viral, engaging content that resonates with audiences. I understand the Facebook algorithm and create content optimized for engagement.",
            verbose=True,
            allow_delegation=False,
            tools=[generate_content_tool],
        )
    
    @staticmethod
    def create_content_editor():
        """Create an agent that refines and edits content."""
        return Agent(
            role="Content Editor",
            goal="Refine and improve content for maximum engagement and clarity",
            backstory="I am a professional editor who ensures content is polished, error-free, and aligned with brand voice. I optimize content for engagement and clarity.",
            verbose=True,
            allow_delegation=False,
            tools=[refine_content_tool],
        )

# Tool definitions
def generate_content_tool(category, style, max_length, include_hashtags=True, max_hashtags=3):
    """Generate content for a Facebook post."""
    prompt = f"""
    Create an engaging Facebook post about {category}.
    Style: {style}
    Maximum length: {max_length} characters
    
    The post should be attention-grabbing and designed to maximize engagement on Facebook.
    
    {f'Include up to {max_hashtags} relevant hashtags.' if include_hashtags else 'Do not include hashtags.'}
    
    Format: Return only the post text with no additional commentary.
    """
    
    content = generate_content(prompt, max_tokens=1024)
    return content

def refine_content_tool(content, brand_voice="professional"):
    """Refine and improve content."""
    prompt = f"""
    Refine and improve the following Facebook post while maintaining its core message.
    Make sure it aligns with a {brand_voice} brand voice.
    
    Original post:
    "{content}"
    
    Ensure the post is engaging, clear, and optimized for Facebook. Fix any grammar or style issues.
    Return only the improved post text with no additional commentary.
    """
    
    refined_content = generate_content(prompt, max_tokens=1024)
    return refined_content
from crewai import Task
import yaml
import random

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

class FacebookTasks:
    """Factory for creating CrewAI tasks for Facebook automation."""
    
    @staticmethod
    def create_content_task(content_creator):
        """Create a task for generating content."""
        # Get a random category from config
        categories = config["content"]["categories"]
        category = random.choice(categories)
        
        return Task(
            description=f"Create an engaging Facebook post about {category}",
            expected_output="A complete, engaging Facebook post ready for publishing",
            agent=content_creator,
            context={
                "category": category,
                "style": config["content"]["style"],
                "max_length": config["content"]["max_length"],
                "include_hashtags": config["content"]["include_hashtags"],
                "max_hashtags": config["content"]["max_hashtags"]
            }
        )
    
    @staticmethod
    def create_editing_task(content_editor, content):
        """Create a task for editing content."""
        return Task(
            description="Edit and refine the generated content to ensure it's engaging and error-free",
            expected_output="A polished Facebook post ready for publishing",
            agent=content_editor,
            context={
                "content": content,
                "brand_voice": config["content"]["style"]
            }
        )
    
    @staticmethod
    def create_posting_task(posting_agent, content):
        """Create a task for posting content to Facebook."""
        return Task(
            description="Post the finalized content to Facebook",
            expected_output="Confirmation of successful posting with post ID",
            agent=posting_agent,
            context={
                "content": content,
                "post_type": random.choice(config["facebook"]["post_types"])
            }
        )
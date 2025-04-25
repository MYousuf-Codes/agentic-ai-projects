import os
import yaml
import logging
import schedule
import time
from datetime import datetime
from dotenv import load_dotenv

from crewai import Crew
from agents.content_agent import ContentAgent
from tasks.facebook_tasks import FacebookTasks
from tools.facebook_tools import FacebookTools

# Load environment variables
load_dotenv()

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config["logging"]["level"]),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=config["logging"]["file"]
)
logger = logging.getLogger(__name__)

def create_and_post_content():
    """Main function to create and post content to Facebook."""
    logger.info("Starting content creation and posting process")
    
    try:
        # Initialize Facebook tools
        facebook_tools = FacebookTools()
        
        # Verify Facebook connection
        if not facebook_tools.verify_connection():
            logger.error("Failed to connect to Facebook. Check credentials.")
            return
        
        # Create agents
        content_creator = ContentAgent.create_content_creator()
        content_editor = ContentAgent.create_content_editor()
        
        # Create posting agent
        posting_agent = Agent(
            role="Social Media Manager",
            goal="Post content to Facebook at optimal times",
            backstory="I am a social media manager responsible for posting content to maximize engagement and reach.",
            tools=[facebook_tools.post_to_facebook],
            verbose=True
        )
        
        # Create tasks
        content_task = FacebookTasks.create_content_task(content_creator)
        
        # Form the crew
        crew = Crew(
            agents=[content_creator, content_editor, posting_agent],
            tasks=[content_task],
            verbose=True
        )
        
        # Execute the crew workflow
        result = crew.kickoff()
        
        # Get the generated content
        generated_content = result
        
        # Edit the content
        editing_task = FacebookTasks.create_editing_task(content_editor, generated_content)
        edited_content = crew.process(editing_task)
        
        # Post to Facebook
        post_task = FacebookTasks.create_posting_task(posting_agent, edited_content)
        posting_result = crew.process(post_task)
        
        logger.info(f"Successfully completed posting process: {posting_result}")
        
    except Exception as e:
        logger.error(f"Error in content creation and posting process: {e}")

def setup_schedule():
    """Set up the scheduling based on configuration."""
    frequency = config["facebook"]["post_frequency"]
    post_time = config["facebook"]["post_time"]
    
    if frequency == "hourly":
        schedule.every().hour.at(":00").do(create_and_post_content)
    elif frequency == "daily":
        schedule.every().day.at(post_time).do(create_and_post_content)
    elif frequency == "weekly":
        schedule.every().monday.at(post_time).do(create_and_post_content)
    else:
        logger.error(f"Unknown frequency: {frequency}")
        return False
    
    return True

if __name__ == "__main__":
    # Check if the critical environment variables are set
    required_vars = ["FACEBOOK_ACCESS_TOKEN", "FACEBOOK_PAGE_ID", "GEMINI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and make sure all required variables are set.")
        exit(1)
    
    # Set up scheduling
    if config["scheduling"]["enabled"]:
        if setup_schedule():
            print(f"Scheduled to run {config['facebook']['post_frequency']} at {config['facebook']['post_time']}")
            logger.info(f"Scheduled to run {config['facebook']['post_frequency']} at {config['facebook']['post_time']}")
            
            # Run the scheduler
            while True:
                schedule.run_pending()
                time.sleep(60)
        else:
            print("Failed to set up scheduling. Check configuration.")
    else:
        # Run once immediately
        print("Running once immediately (scheduling disabled)")
        create_and_post_content()
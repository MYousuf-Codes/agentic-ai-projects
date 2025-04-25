import os
import requests
import facebook
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/facebook_automation.log'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class FacebookTools:
    def __init__(self):
        """Initialize Facebook Graph API client."""
        self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.page_id = os.getenv("FACEBOOK_PAGE_ID")
        
        if not self.access_token or not self.page_id:
            logger.error("Facebook credentials not found in environment variables")
            raise ValueError("Facebook credentials not found in environment variables")
        
        try:
            self.graph = facebook.GraphAPI(access_token=self.access_token, version="3.1")
            logger.info("Facebook Graph API initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Facebook Graph API: {e}")
            raise

    def post_to_facebook(self, message, image_url=None):
        """Post content to Facebook page."""
        try:
            if image_url:
                # Post with image
                response = self.graph.put_photo(
                    image=requests.get(image_url).content,
                    message=message,
                )
                post_id = response["id"]
                logger.info(f"Posted to Facebook with image: {post_id}")
            else:
                # Text-only post
                response = self.graph.put_object(
                    parent_object=self.page_id,
                    connection_name="feed",
                    message=message,
                )
                post_id = response["id"]
                logger.info(f"Posted to Facebook: {post_id}")
            
            return post_id
        except Exception as e:
            logger.error(f"Failed to post to Facebook: {e}")
            return None
            
    def verify_connection(self):
        """Verify connection to Facebook Graph API."""
        try:
            account_info = self.graph.get_object(id=self.page_id)
            logger.info(f"Successfully connected to Facebook page: {account_info.get('name', 'Unknown')}")
            return True
        except Exception as e:
            logger.error(f"Failed to verify Facebook connection: {e}")
            return False
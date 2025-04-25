import os
import streamlit as st
import time
import json
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import urllib.parse
import webbrowser
import requests

# Set up configuration for Streamlit
st.set_page_config(page_title="AI Video Assistant", layout="wide")

# Function to set up WebDriver for visualization
def initialize_webdriver():
    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--ignore-certificate-errors")
        
        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Set window size explicitly to ensure screenshots work
        driver.set_window_size(1366, 768)
        
        # Test connection by loading a simple page
        try:
            driver.get("https://www.google.com")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            st.success("Browser initialized successfully!")
            return driver
        except Exception as e:
            st.error(f"Connection test failed: {str(e)}")
            driver.quit()
            return None
            
    except Exception as e:
        st.error(f"Error initializing WebDriver: {str(e)}")
        return None

# Initialize session states
if 'driver' not in st.session_state:
    st.session_state.driver = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# Main content area
st.title("AI Video Assistant")
st.write("I can help you search for videos, open websites, and answer questions!")

# Settings section
with st.expander("Settings", expanded=False):
    st.session_state.api_key = st.text_input("Gemini API Key", type="password", value=st.session_state.api_key)
    if st.button("Initialize Browser"):
        if st.session_state.driver is None:
            with st.spinner("Initializing browser..."):
                st.session_state.driver = initialize_webdriver()
            if st.session_state.driver:
                st.success("Browser initialized successfully!")
        else:
            st.info("Browser is already initialized.")

# Function to detect and extract URLs from text
def extract_urls(text):
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return re.findall(url_pattern, text)

# Function to check if URL is a YouTube link
def is_youtube_url(url):
    return 'youtube.com' in url or 'youtu.be' in url

# Function to extract YouTube video ID
def extract_youtube_id(url):
    if 'youtube.com/watch' in url:
        query = urllib.parse.urlparse(url).query
        params = urllib.parse.parse_qs(query)
        return params.get('v', [''])[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    return None

# Function to search for YouTube videos
def search_youtube(query):
    try:
        # If we have a browser, search directly
        if st.session_state.driver:
            try:
                # Go to YouTube
                st.session_state.driver.get("https://www.youtube.com")
                time.sleep(2)
                
                # Find and click the search box
                search_box = WebDriverWait(st.session_state.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input#search"))
                )
                
                # Clear the search box and type the query
                search_box.clear()
                search_box.send_keys(query)
                search_box.send_keys(Keys.RETURN)
                st.info(f"Searching for: {query}")
                time.sleep(3)
                
                # Take screenshot of search results
                safe_screenshot(st.session_state.driver, "youtube_search.png")
                
                # Try to find and click the first video
                try:
                    # Wait for the first video to be clickable
                    first_video = WebDriverWait(st.session_state.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a#video-title"))
                    )
                    
                    # Get video details before clicking
                    video_title = first_video.get_attribute("title")
                    video_url = first_video.get_attribute("href")
                    video_id = extract_youtube_id(video_url)
                    
                    # Click the video to play it
                    first_video.click()
                    st.success(f"Playing: {video_title}")
                    time.sleep(3)
                    
                    # Take screenshot of the playing video
                    safe_screenshot(st.session_state.driver, "youtube_playing.png")
                    
                    return {
                        "title": video_title,
                        "url": video_url,
                        "id": video_id
                    }
                except Exception as e:
                    st.warning(f"Could not play video: {str(e)}")
                    # If we can't play the video, at least return the search results
                    search_term = urllib.parse.quote(query)
                    return {
                        "title": f"Search results for: {query}",
                        "url": f"https://www.youtube.com/results?search_query={search_term}",
                        "id": None
                    }
            except Exception as e:
                st.error(f"Error accessing YouTube: {str(e)}")
                # Try to reinitialize the browser
                st.session_state.driver = initialize_webdriver()
                if st.session_state.driver:
                    return search_youtube(query)  # Retry the search
                return None
        
        # Fallback: use a general search term
        st.warning("Using general search results")
        search_term = urllib.parse.quote(query)
        return {
            "title": f"Search results for: {query}",
            "url": f"https://www.youtube.com/results?search_query={search_term}",
            "id": None
        }
    except Exception as e:
        st.error(f"Error searching YouTube: {str(e)}")
        return None

# Function to open URL in browser
def open_url(url):
    if st.session_state.driver:
        try:
            # Ensure URL has proper format
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            # Try to open the URL
            st.session_state.driver.get(url)
            time.sleep(2)
            
            # Verify the page loaded
            try:
                WebDriverWait(st.session_state.driver, 10).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
                safe_screenshot(st.session_state.driver, "opened_link.png")
                return True
            except Exception as e:
                st.warning(f"Page loaded but might be incomplete: {str(e)}")
                return True
                
        except Exception as e:
            st.error(f"Error opening URL in WebDriver: {str(e)}")
            # Try to reinitialize the browser
            st.session_state.driver = initialize_webdriver()
            if st.session_state.driver:
                return open_url(url)  # Retry opening the URL
            return False
    else:
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            st.error(f"Error opening URL: {str(e)}")
            return False

# Function to take screenshot safely with fallback
def safe_screenshot(driver, filename):
    try:
        driver.save_screenshot(filename)
        st.image(filename, caption=f"Screenshot: {filename}")
        return True
    except Exception as e:
        st.warning(f"Could not take screenshot: {str(e)}")
        return False

# Function to set up Gemini
def setup_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"Error setting up Gemini: {str(e)}")
        return False

# Function to generate response using Gemini
def generate_response(prompt, api_key):
    try:
        # Configure Gemini
        setup_gemini(api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate the response
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating response with Gemini: {str(e)}")
        return f"Error generating response: {str(e)}"

# Function to handle YouTube video playback
def play_youtube_video(video_id):
    try:
        if st.session_state.driver:
            # Navigate to the video
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            st.session_state.driver.get(video_url)
            time.sleep(2)
            
            # Wait for the video player to load
            WebDriverWait(st.session_state.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "video.html5-main-video"))
            )
            
            # Take screenshot of the playing video
            safe_screenshot(st.session_state.driver, "youtube_playing.png")
            
            # Embed the video in the chat
            st.video(video_url)
            return True
    except Exception as e:
        st.error(f"Error playing YouTube video: {str(e)}")
        return False

# Function to handle chat messages
def handle_chat_message(message):
    # Check for YouTube video links
    youtube_links = re.findall(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)', message)
    if youtube_links:
        for video_id in youtube_links:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Playing YouTube video..."
            })
            play_youtube_video(video_id)
        return

    # Check for general URLs
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', message)
    if urls:
        for url in urls:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Opening link: {url}"
            })
            open_url(url)
        return

    # Check for video search commands
    if re.match(r'^(search|find|show|play)\s+(videos?|youtube)\s+(of|about|for)\s+', message.lower()):
        search_term = re.sub(r'^(search|find|show|play)\s+(videos?|youtube)\s+(of|about|for)\s+', '', message.lower())
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Searching for videos about: {search_term}"
        })
        
        # Initialize WebDriver if not already done
        if st.session_state.driver is None:
            with st.spinner("Initializing browser..."):
                st.session_state.driver = initialize_webdriver()
        
        # Search for videos
        video = search_youtube(search_term)
        if video:
            if video["id"]:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Now playing: {video['title']}"
                })
                play_youtube_video(video["id"])
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Here are search results for '{search_term}'. You can check them in the browser."
                })
                if st.session_state.driver:
                    open_url(video["url"])
        return

    # Check for website opening commands
    if message.lower().startswith("open "):
        url = message[5:].strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Opening {url}..."
        })
        
        # Initialize WebDriver if not already done
        if st.session_state.driver is None:
            with st.spinner("Initializing browser..."):
                st.session_state.driver = initialize_webdriver()
        
        if st.session_state.driver:
            open_url(url)
        else:
            st.warning("Could not initialize browser. Please try again.")
        return

    # Generate AI response for other messages
    if st.session_state.api_key:
        with st.spinner("Thinking..."):
            response = generate_response(message, st.session_state.api_key)
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            # Check if the response contains URLs
            response_urls = extract_urls(response)
            if response_urls:
                for url in response_urls:
                    if is_youtube_url(url):
                        video_id = extract_youtube_id(url)
                        if video_id:
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": f"Here's the YouTube video I mentioned:"
                            })
                            play_youtube_video(video_id)
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Please enter your Gemini API key in the settings to enable AI responses."
        })

# Chat Interface
def chat_interface():
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Helper message about commands
    st.markdown("""
    **Commands you can try:**
    - **Search videos of [topic]** - Search for YouTube videos
    - **Open [website]** - Visit a website
    - **[paste a YouTube link]** - Play the video
    - **[paste any URL]** - Open the link
    - **[ask a question]** - Get AI assistance
    """)
    
    # Chat input
    if prompt := st.chat_input("What would you like me to help you with?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Handle the message
        handle_chat_message(prompt)

# Main application flow
def main():
    chat_interface()

if __name__ == "__main__":
    main()
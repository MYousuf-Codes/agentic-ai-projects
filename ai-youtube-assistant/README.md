# Streamlit Gemini Web Assistant

This application creates a chat interface using Streamlit that:
1. Takes user prompts
2. Uses Google's Gemini LLM to understand the request
3. Performs web-based tasks using Selenium WebDriver
4. Shows the visual results of those actions

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Google API key for Gemini LLM

### Installation

1. Clone this repository:
```
git clone <repository-url>
cd streamlit-gemini-web-assistant
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Get a Google Gemini API key:
   - Go to https://makersuite.google.com/
   - Sign up and create an API key

### Running the Application

1. Start the Streamlit app:
```
streamlit run main.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. In the sidebar, enter your Google Gemini API key and click "Initialize"

4. Start chatting with the assistant in the input field

## Usage Examples

You can ask the assistant to perform various web tasks, such as:

- "Search for the latest news about artificial intelligence"
- "Go to Wikipedia and find information about quantum computing"
- "Check the weather forecast for New York City"
- "Show me the homepage of NASA"

The assistant will use Google's Gemini to interpret your request, navigate to the appropriate website using Selenium, and show you a screenshot of the result.

## Technical Details

This application uses:
- **Streamlit**: For the web interface
- **Google Gemini**: For natural language understanding
- **Selenium WebDriver**: For web automation and screenshots
- **Chrome**: As the headless browser for web navigation

## Limitations

- The current implementation is simplified and may not handle complex web interactions
- Due to security restrictions, some websites may block automated access
- The application requires a stable internet connection
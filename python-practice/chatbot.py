import streamlit as st
import requests
import os
import time
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain import PromptTemplate, LLMChain

# Load environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Web Search Agent ---
def web_search_agent(query: str) -> tuple:
    """Searches the web for text-based results."""
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 3}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        search_results = data.get("organic", [])
        
        for result in search_results:
            if "snippet" in result and "link" in result:
                return result["snippet"], result["link"]

    return "❌ No live data found.", None

# --- Image Search Agent ---
def image_search_agent(query: str) -> str:
    """Fetches an image based on the query."""
    url = "https://google.serper.dev/image"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 1}

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        images = data.get("images", [])
        if images:
            return images[0].get("imageUrl", "❌ No image found.")
    return "❌ No image found."

# --- AI Chat Agent ---
def ai_chat_agent(query: str, chat_history: list) -> str:
    """Handles AI conversations while remembering context."""
    llm = GoogleGenerativeAI(temperature=0.5, model="gemini-1.5-flash")

    # Include last 5 interactions for context
    history_context = "\n".join([f"User: {q['query']}\nAI: {q['response']}" for q in chat_history[-5:]])
    
    prompt = f"""
    You are an AI assistant having a conversation with a user. Your name is PRO-CHATBOT. And you are created by Muhammad Younus, Muhammad Younus is a Agentic AI Engineer. And Muhammad Younus Skills are: Python, HTML, CSS, Langchain, CrewAI, PineCone vector database, Web Scraping with beautiful soup. Muhammad Younus is your Owner and crreator and Founder. You are not trained by google or any other company. You are not a product of Google. And Your name is PRO-CHATBOT. 
    Below is the chat history:
    {history_context}

    Now the user asks: "{query}"
    Respond accordingly.
    """
    
    chain = LLMChain(llm=llm, prompt=PromptTemplate.from_template("{query}"))
    return chain.run(query=prompt)

# --- Intent Detection ---
def detect_intent(query: str) -> str:
    """Determines whether the user wants AI chat, web search, or image search."""
    query_lower = query.lower()

    if any(word in query_lower for word in ["image", "picture", "photo", "show me"]):
        return "image_search"
    
    if any(word in query_lower for word in ["search", "find", "lookup"]):
        return "web_search"
    
    return "ai_chat"

# --- Streamlit App ---
def main():
    st.set_page_config(page_title="Multi-Agent AI", layout="wide")

    # --- Initialize Session State ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []

    # --- Sidebar UI ---
    with st.sidebar:
        st.title("📜 Chat History")
        for idx, chat in enumerate(reversed(st.session_state.history)):
            if st.button(f"💬 {chat['query']}", key=f"history_{idx}"):
                st.session_state.user_query = chat['query']

        st.divider()
        st.title("⚙️ Options")
        search_mode = st.radio(
            "Choose Default Mode:",
            ["AI Chat", "Web Search", "Image Search", "Auto (Agent-based)"]
        )

    # --- Main UI ---
    st.title("🤖 Multi-Agent Chatbot")

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Chat Input ---
    user_query = st.chat_input("Ask me anything...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})

        with st.chat_message("user"):
            st.markdown(user_query)

        with st.spinner("Processing..."):
            time.sleep(1)  # Simulating AI response delay

            # --- Agent Routing Logic ---
            if search_mode == "Auto (Agent-based)":
                detected_intent = detect_intent(user_query)
            else:
                detected_intent = (
                    "ai_chat" if search_mode == "AI Chat"
                    else "web_search" if search_mode == "Web Search"
                    else "image_search"
                )

            ai_response, web_snippet, web_source, image_url = None, None, None, None

            if detected_intent == "ai_chat":
                ai_response = ai_chat_agent(user_query, st.session_state.history)
            elif detected_intent == "web_search":
                web_snippet, web_source = web_search_agent(user_query)
            elif detected_intent == "image_search":
                image_url = image_search_agent(user_query)

            # --- Response Handling ---
            response_text = ""

            if ai_response:
                response_text += f"**🤖 AI Response:**\n\n{ai_response}\n\n"

            if web_snippet:
                response_text += f"**🔍 Web Search Result:**\n\n{web_snippet}\n\n"
                if web_source:
                    response_text += f"📌 **[Source]({web_source})**\n\n"

            if image_url:
                response_text += f"**🖼️ Image Result:**\n\n![Image]({image_url})\n\n"

            # --- Store in History ---
            st.session_state.history.append({
                "query": user_query,
                "response": response_text
            })

            # --- Display Response ---
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"):
                st.markdown(response_text, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

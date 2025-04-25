import chainlit as cl
import requests
import os
import time
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Web Search Function
def web_search(query: str) -> str:
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 3}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        search_results = data.get("organic", [])
        if search_results:
            for result in search_results:
                if "snippet" in result:
                    return f"{result['snippet']} (Source: {result['link']})"
            return f"More info: {search_results[0]['link']}"
    return "❌ No live data found."

# Image Search Function
def image_search(query: str) -> str:
    url = "https://google.serper.dev/images"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 1}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "images" in data and len(data["images"]) > 0:
            return data["images"][0]["imageUrl"]
    return None

# AI Response Generation
def generate_answer(query: str, live_data: str) -> str:
    prompt_template = """
    You are an AI assistant with access to real-time web search results.
    Your task is to extract and present a **clear and concise answer** from the web data.
    Avoid speculation—**answer only if the data is available**.
    
    **Live Web Data:**
    {live_data}
    
    **Query:** {query}
    **Direct Answer:**
    """
    
    prompt = PromptTemplate.from_template(prompt_template)
    llm = GoogleGenerativeAI(temperature=0.5, model="gemini-1.5-flash")
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain.invoke({"query": query, "live_data": live_data})

# Chainlit Chatbot
@cl.on_message
async def handle_message(message: cl.Message):
    query = message.content
    await cl.Message(content="🔄 Fetching real-time data... Please wait.").send()
    time.sleep(1)  # Simulate processing delay
    
    live_data = web_search(query)
    final_answer = generate_answer(query, live_data)
    image_url = image_search(query)
    
    response_text = f"✅ **Answer:** {final_answer}\n\n"
    if live_data:
        response_text += f"📌 **Source:** {live_data}\n\n"
    
    elements = []
    if image_url:
        elements.append(cl.Image(name="Related Image", url=image_url, display="inline"))

    await cl.Message(content=response_text, elements=elements).send()

# Start the Chainlit app
if __name__ == "__main__":
    cl.run()

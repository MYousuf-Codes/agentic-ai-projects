# !pip install chainlit google-generativeai python-dotenv

import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # Adjust the model name if needed

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content.strip()
    
    # If the message starts with "summarize:", summarize the text that follows
    if user_input.lower().startswith("summarize:"):
        text_to_summarize = user_input[len("summarize:"):].strip()
        prompt = f"Summarize the following text:\n{text_to_summarize}"
        response = model.generate_content(prompt)
        summary = response.text.strip()
        await cl.Message(content=f"**Summary:**\n{summary}").send()
    else:
        # Otherwise, generate a conversational response
        prompt = f"Answer the following query in a conversational style:\n{user_input}"
        response = model.generate_content(prompt)
        reply = response.text.strip()
        await cl.Message(content=reply).send()

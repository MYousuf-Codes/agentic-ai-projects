import nest_asyncio
nest_asyncio.apply()  # Enable nested event loops

import os
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_default_openai_client

# Set your API keys (update with your own keys or use Colab userdata)
gemini_api_key = "AIzaSyCqwuqDETRE8PWjntKQOYdtoHaT1ON9fKE"

# Initialize the external client to access Gemini via Google's API
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

# Set up the language model using the Gemini model for chat completions
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Create an Agent with your desired instructions. This agent will act as a Math Tutor.
agent = Agent(
    name="Math Tutor",
    instructions=(
        "You are a helpful Math Tutor. Your user will be a student. "
        "Talk to the user in a friendly manner, like a best friend, and motivate them to keep learning. "
        "You should only answer, explain, and solve math problems. If the user asks anything else, do not respond. "
        "You can also use a web searching tool for giving links to relevant YouTube lectures."
    ),
    model=model,
)

# Chainlit callback for chat start: show a welcome message.
@cl.on_chat_start
async def start():
    await cl.Message(content="Hello, I am your Math Tutor. Ask me a math problem!").send()

# Chainlit callback for each user message
@cl.on_message
async def main(message: str):
    try:
        # Run the agent synchronously with the user input
        result = Runner.run_sync(agent, message)
        # Send back the agent's final output to the user
        await cl.Message(content=result.final_output).send()
    except Exception as e:
        await cl.Message(content=f"Oops, something went wrong: {str(e)}").send()

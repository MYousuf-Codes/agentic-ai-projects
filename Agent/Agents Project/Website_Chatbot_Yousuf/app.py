import chainlit as cl
import os
from uuid import uuid4
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone

# Initialize Pinecone
PINECONE_API_KEY = "pcsk_3ftPjY_DXuxCvSoayQmWiAHHhqbvfg7sheC7sRji3EKp31QMA79eAZwbGzBYkNBFsArch7"
PINECONE_ENVIRONMENT = "CHATBOT_PINECONE_API_KEY"

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "chatbot"

# Check if the index already exists before attempting to create it.
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec={"cloud": "aws", "region": "us-east-1"}
    )

index = pc.Index(index_name)

os.environ['GOOGLE_API_KEY'] = "AIzaSyCqwuqDETRE8PWjntKQOYdtoHaT1ON9fKE"

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Define the documents
documents = [
    # ... (your existing documents here)
]

# Add documents to vector store
uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! I'm MYousuf-Codes Chatbot. How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    # Get relevant documents
    vector_results = vector_store.similarity_search(message.content, k=2)
    
    # Generate response
    response = llm.invoke(f"""USER : {message.content},
    ChatBot : {vector_results}, {documents} """)
    
    # Send response
    await cl.Message(content=response.content).send() 
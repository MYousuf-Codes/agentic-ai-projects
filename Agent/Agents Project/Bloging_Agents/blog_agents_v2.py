import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from datetime import datetime
import aiohttp
import json

# Initialize Google Gemini
gemini_api_key = os.environ['GOOGLE_API_KEY'] = "AIzaSyCqwuqDETRE8PWjntKQOYdtoHaT1ON9fKE"

# Initialize external client for Gemini
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Initialize model configuration
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure run settings
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

async def search_web(query: str) -> str:
    """Custom web search function using aiohttp"""
    async with aiohttp.ClientSession() as session:
        # Using Brave Search API (free tier)
        url = f"https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": "YOUR_BRAVE_API_KEY"  # Replace with your Brave API key
        }
        params = {
            "q": query,
            "count": 5
        }
        
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                results = data.get("web", {}).get("results", [])
                return "\n".join([f"{result.get('title', '')}: {result.get('description', '')}" for result in results])
            return "No results found"

# Create the research agent
research_agent = Agent(
    name="Research Agent",
    instructions="""You are a research agent specialized in tech trends. Your task is to:
    1. Analyze current trends in programming, AI, AI tools, and technology
    2. Identify emerging technologies and developments
    3. Return a list of 5 potential blog topics with brief descriptions
    4. Focus on recent and relevant topics
    """,
    model=model,
)

# Create the topic selection agent
selection_agent = Agent(
    name="Selection Agent",
    instructions="""You are a topic selection expert. Your task is to:
    1. Review the topics provided by the research agent
    2. Select the most engaging and relevant topic
    3. Provide a detailed outline for the blog post
    4. Consider SEO and audience engagement
    """,
    model=model,
)

# Create the writing agent
writing_agent = Agent(
    name="Writing Agent",
    instructions="""You are a professional tech blogger. Your task is to:
    1. Write an engaging blog post based on the selected topic and outline
    2. Include relevant examples and code snippets
    3. Make the content informative and easy to understand
    4. Use proper headings and formatting
    5. Include SEO-friendly meta descriptions
    """,
    model=model,
)

# Create the review agent
review_agent = Agent(
    name="Review Agent",
    instructions="""You are a content review expert. Your task is to:
    1. Review the blog post for accuracy and engagement
    2. Suggest improvements for better readability
    3. Ensure proper formatting and structure
    4. Add interactive elements if needed
    5. Check for SEO optimization
    """,
    model=model,
)

# Create the image agent
image_agent = Agent(
    name="Image Agent",
    instructions="""You are an image research expert. Your task is to:
    1. Suggest relevant image concepts based on the blog content
    2. Provide detailed image descriptions
    3. Include image style and composition suggestions
    4. Ensure images would be high-quality and relevant
    """,
    model=model,
)

# Create the finalization agent
finalization_agent = Agent(
    name="Finalization Agent",
    instructions="""You are a content finalization expert. Your task is to:
    1. Combine the reviewed blog post with the image suggestions
    2. Ensure proper formatting and structure
    3. Create a final version ready for publishing
    4. Save the content in a text file
    5. Include proper metadata and SEO elements
    """,
    model=model,
)

async def create_blog():
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Step 1: Research trending topics
            research_result = await Runner.run(
                research_agent, 
                input="Find trending topics in programming, AI, and tech",
                run_config=config
            )
            topics = research_result.final_output
            
            # Step 2: Select the best topic
            selection_result = await Runner.run(
                selection_agent, 
                input=f"Select the best topic from these: {topics}",
                run_config=config
            )
            selected_topic = selection_result.final_output
            
            # Step 3: Write the blog post
            writing_result = await Runner.run(
                writing_agent, 
                input=f"Write a blog post about: {selected_topic}",
                run_config=config
            )
            blog_content = writing_result.final_output
            
            # Step 4: Review and improve the blog
            review_result = await Runner.run(
                review_agent, 
                input=f"Review and improve this blog post: {blog_content}",
                run_config=config
            )
            improved_content = review_result.final_output
            
            # Step 5: Find relevant image
            image_result = await Runner.run(
                image_agent, 
                input=f"Suggest images for this blog post: {improved_content}",
                run_config=config
            )
            image_suggestion = image_result.final_output
            
            # Step 6: Finalize and save
            final_result = await Runner.run(
                finalization_agent, 
                input=f"Finalize this blog post with image suggestions: {improved_content}\nImage Suggestions: {image_suggestion}",
                run_config=config
            )
            final_content = final_result.final_output
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"blog_{timestamp}.txt"
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_content)
                
            return f"Blog created successfully! Saved as {filename}"
            
        except Exception as e:
            print(f"Error occurred (attempt {retry_count + 1}/{max_retries}): {str(e)}")
            retry_count += 1
            if retry_count == max_retries:
                return "Failed to create blog after maximum retries"
            continue

async def main():
    result = await create_blog()
    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 
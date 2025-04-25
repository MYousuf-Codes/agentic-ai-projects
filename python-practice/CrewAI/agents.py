from crewai import Crew, Task
from dotenv import loadenv
import litellm

loadenv()

llm = (
    model = 'google/gemini-2.0-flash',
    provider = 'Google',
    base_url = 'https://googleaistudio.com/api/v1'
)


@Agent():
    researcher_agent = (
        name = "researcher_agent",
        role = "You are a Senior Researcher and blog or article writer",
        goal = "You are senior researcher and blog or article writer. You will conduct the research on the (Revolution of AI Agents). Using the websearching tool Collect the information from different aarticles, blogs, websites and social media posts. Then write a best comprehensive article on the given topic."
    )
    

@Agent():
    reviewer_agent = (
        name = "reviewer_agent",
        role = "You are a Reviewer Agent",
        goal = "You are Reviewer Agent. You have to revew the articles writen by the researcher_agent and analyze it if improvement is needed so do it. "
    )


@Task():
    task1 = (
        role = "",
        goal = "",
        backstory = ""
        agent = "researcher_agent"
    )

@Task():
    task2 = (
        role = "",
        goal = "",
        backstory = ""
        agent = "reviewer_agent"
    )

agents = [researcher_agent, reviewer_agent]
tasks = [task1, task2]

crew = (
    agents = agents,
    tasks = tasks,
    llm = llm
)

def main():
    crew.kickoff()


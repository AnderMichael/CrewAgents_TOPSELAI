import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import FileReadTool
from tools import pdf_tool, fastapi_tool, scipy_tool
from crewai_tools import FileWriterTool

load_dotenv()

llm = LLM(model="gpt-4o-mini")
current_dir = os.path.dirname(os.path.abspath(__file__))


# Define the Analyzer Agent with the necessary tools
analyzer_agent = Agent(
    role="Senior Python Developer",
    goal="Perform thorough and concise code planning and explanations.",
    backstory=(
        "You are a senior Python developer with extensive experience in software architecture, "
        "programming best practices, and code reviews. Your planning and explanations should be "
        "based on code documentation and PDF papers. You always use your tools to accelerate development."
    ),
    llm=llm,
    tools=[pdf_tool, fastapi_tool, scipy_tool],
)

# Define the Coder Agent
coder_agent = Agent(
    role="Senior Python Developer",
    goal=(
        "Craft well-designed and thought-out code. You can design a FastAPI app with SciPy. "
        "Also perform thorough and concise code reviews."
    ),
    backstory=(
        "You are a senior Python developer with extensive experience in software architecture, "
        "programming best practices, and code reviews. You can implement whatever has a planning "
        "and explanation."
    ),
    allow_code_execution=True,
    llm=llm,
)

# Define Tasks

# Task 1: Summarize Chapter 7
summarize_chapter5_task = Task(
    description=(
        "Read and summarize everything about  chapter 7 'Geometría Computacional' from the PDF. "
        "Provide a concise summary highlighting the key functions and concepts."
    ),
    expected_output=(
        "A concise summary of  chapter 7 'Geometría Computacional', highlighting key functions and concepts "
        "that can be implemented in a FastAPI app."
    ),
    agent=analyzer_agent,
    output_file="summary.md",
    tools=[pdf_tool, FileWriterTool(file_path=os.path.join(current_dir, "summary.md"))],
)

# Task 2: Create analysis.md using the summary
create_analysis_md_task = Task(
    description=(
        "Using the summary of chapter 7 'Geometría Computacional', create a detailed analysis.md file "
        "with explanations of code implementation plans for a FastAPI app integrated with SciPy, use the docs."
    ),
    expected_output=(
        "A well-structured 'analysis.md' file containing detailed plans and explanations for implementing "
        "the functions from chapter 7 'Geometría Computacional' in a FastAPI app using SciPy. Detail imports at header, functions at body (with descriptions) and main run at the end."
    ),
    agent=analyzer_agent,
    output_file="analysis.md",
    tools=[
        FileReadTool(file_path=os.path.join(current_dir, "summary.md")),
        FileWriterTool(file_path=os.path.join(current_dir, "analysis.md")),
        fastapi_tool,
        scipy_tool,
    ],  # Assuming FileWriteTool exists
)

# Task 3: Generate the FastAPI app
generate_fastapi_app_task = Task(
    description=(
        "Generate a FastAPI app in one file, given the code planning and explanations in analysis.md. Don't forget the run code to start the app in localhost:8000."
        "Implement all the functions of chapter 7 'Geometría Computacional'."
    ),
    expected_output=(
        "A valid and well-written Python file 'main.py' with the described functionality implemented. "
        "Don't include ticks at the beginning or end of the file."
    ),
    agent=coder_agent,
    output_file="main.py",
    tools=[FileReadTool(file_path=os.path.join(current_dir, "analysis.md"))],
)

# Define the development crew with task sequencing
dev_crew = Crew(
    agents=[analyzer_agent, coder_agent],
    tasks=[
        summarize_chapter5_task,  # Execute first
        create_analysis_md_task,  # Execute second, depends on the first
        generate_fastapi_app_task,  # Execute third, depends on the second
    ],
    verbose=True,
)

# Kickoff the crew
result = dev_crew.kickoff()

print(result)

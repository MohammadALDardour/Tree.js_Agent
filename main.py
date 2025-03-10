import os
import logging
from textwrap import dedent
from crewai import Crew, Process, LLM
from dotenv import load_dotenv

from langchain_community.llms import OpenAI , Ollama
# Import our custom agent and task classes
from agents import teachAgents
from tasks import techerTasks

# Import file I/O tool (if needed)
#from tools.file_io import save_and_execute

# Load environment variables
load_dotenv()

# # Initialize the language model
llm = Ollama(
   model="deepseek-r1:7b",
   base_url="http://localhost:11434"
)
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example PDF path (update as needed)
pdf_path = "/home/mohammad/Projects/AI_teacher/site/Ch4.pdf"

class TeachCrew:
    def __init__(self, chapter, age, pdf, subject, complexity, interactive, theme, var1, var2):
        self.chapter = chapter
        self.age = int(age)
        self.pdf = pdf
        self.subject = subject
        self.complexity = complexity
        # interactive is a boolean value
        self.interactive = interactive  
        self.theme = theme
        self.var1 = var1
        self.var2 = var2

    def run(self):
        try:
            # Initialize agents and tasks
            agents_instance = teachAgents()
            tasks_instance = techerTasks()

            # Create a single agent for three.js script creation
            threejs_agent = agents_instance.agent_three_js_creator()

            # Define the three.js script generation task
            threejs_task = tasks_instance.task_generate_html_three_js(
                agent=threejs_agent,
                subject=self.subject,
                complexity=self.complexity,
                interactive=self.interactive,
                theme=self.theme
            )

            # Initialize Crew with one agent and one task
            crew = Crew(
                agents=[threejs_agent],
                tasks=[threejs_task],
                manager_llm=llm,
                verbose=True
            )

            # Execute Crew and return the result
            result = crew.kickoff()
            return result

        except Exception as e:
            logger.error(f"An error occurred in TeachCrew.run(): {e}")
            return None

if __name__ == "__main__":
    print("## Welcome to the Interactive Three.js Learning Material Generator")
    print("------------------------------------------------------------------")

    try:
        # Get user inputs with validation
        chapter = input("Enter the chapter to be explained: ").strip()
        age = int(input("Enter the student's age: "))
        if age <= 0:
            raise ValueError("Age must be a positive number")
        
        var1 = input("Enter any specific focus variable or concept: ").strip()
        var2 = input("Enter any additional information or emphasis: ").strip()

        # For the three.js task, ask for additional parameters
        subject = input("Enter the subject (e.g., 'Quantum Mechanics - Chapter 1'): ").strip()
        complexity = input("Enter the complexity level (Beginner/Intermediate/Advanced): ").strip()
        interactive_input = input("Should the animation be interactive? (yes/no): ").strip().lower()
        interactive = True if interactive_input == "yes" else False
        theme = input("Enter the design theme (e.g., Futuristic, Minimalistic, Vibrant): ").strip()

        # Use the predefined PDF path (update if needed)
        pdf_file = pdf_path

        # Create and run the teaching crew
        teach_crew = TeachCrew(chapter, age, pdf_file, subject, complexity, interactive, theme, var1, var2)
        result = teach_crew.run()

        if result:
            print("\n###############################")
            print("## Generated Three.js Script:")
            print("###############################\n")
            print(result)
        else:
            print("Failed to generate the three.js script.")

    except ValueError as ve:
        print(f"Invalid input: {ve}. Please try again.")
    except Exception as ex:
        print(f"An error occurred: {ex}. Please try again.")

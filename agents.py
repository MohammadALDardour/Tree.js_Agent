import os
import logging
from textwrap import dedent
from crewai import Agent, LLM
from tools.animation_tool import ThreeJSGeneratorTool
from tools.QueryEngine import PDFExtractionTools

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class teachAgents:
    def __init__(self):
        # Configure the LLM with the correct provider and model
        try:
            self.llm = LLM(
                base_url="http://localhost:11434",  # Ensure this matches your Ollama server's URL
                model="ollama/deepseek-r1:7b",     # Use the desired model
            )
            logger.info("LLM initialized successfully.")
        except Exception as e:
            logger.error(f"LLM initialization error: {e}")
            raise

    def agent_three_js_creator(self):
        """
        Create and return an Agent that specializes in generating fully functional HTML pages 
        with embedded Three.js scripts for educational animations.

        This agent is responsible for:
        - Extracting educational content from PDFs to structure the lesson.
        - Generating a complete HTML file with a Three.js-powered interactive visualization.
        - Setting up a responsive Three.js environment including a scene, camera, lighting, 
            interactive controls, and objects relevant to the lesson topic.
        - Ensuring modularity so the generated script can be expanded or customized easily.
        """
        try:
            agent = Agent(
                role="Professional Three.js HTML Page Creator",
                backstory=dedent(
                    """
                    You are an expert in creating interactive and visually appealing educational web pages 
                    using Three.js. Your goal is to make complex topics engaging through dynamic animations 
                    and interactive visualizations.

                    Your work is inspired by 3Blue1Brown, blending storytelling with technical visuals 
                    to enhance comprehension. Your animations are smooth, well-structured, and optimized 
                    for a seamless learning experience.
                    """
                ),
                goal=dedent(
                    """
                    Your primary task is to generate a **complete, self-contained HTML file** 
                    with an interactive Three.js visualization.

                    The HTML file should:
                    - Include all necessary `<script>` tags and styles.
                    - Initialize a Three.js scene, camera, renderer, and canvas.
                    - Set up lighting, materials, and relevant 3D objects.
                    - Implement interactive elements (e.g., mouse controls, animations).
                    - Be **clean, modular, and documented** for easy customization.
                    - Ensure compatibility across browsers and mobile devices.
                    """
                ),
                tools=[
                    # PDF Extraction Tools to analyze and extract educational content
                    PDFExtractionTools.extract_text_from_pdf,
                    PDFExtractionTools.index_text,
                    PDFExtractionTools.extract_and_index,
                    # Three.js Generator Tool for creating structured HTML + JS output
                    ThreeJSGeneratorTool()
                ],
                allow_delegation=False,
                verbose=True,
                llm=self.llm,
                max_iter=2
            )
            logger.info("Three.js HTML Page Creator Agent initialized successfully.")
            return agent
        except Exception as e:
            logger.error(f"Error initializing the Three.js HTML Page Creator Agent: {e}")
            raise

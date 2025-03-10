import textwrap
from crewai import Task
from textwrap import dedent

class techerTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def task_generate_html_three_js(self, agent, subject, complexity, interactive, theme):
        """
        Task: Generate a full HTML file with embedded Three.js initialization.
        
        This task requires creating a **complete HTML page** that includes:
          - A properly structured Three.js scene (canvas, camera, renderer).
          - Dynamic animations to visually explain the given subject.
          - Interactive features if enabled (e.g., camera controls, user input).
          - A clean and modular structure to allow customization.

        Parameters:
            agent (str): The agent who will perform the task.
            subject (str): The subject of the lesson (e.g., "Quantum Mechanics", "Algebra", etc.).
            complexity (str): The target complexity level (e.g., "Beginner", "Intermediate", "Advanced").
            interactive (bool): Whether the page should include interactive elements.
            theme (str): The design theme of the animation (e.g., "Futuristic", "Minimalistic", "Vibrant").

        Expected Output:
            A complete **self-contained HTML file** that sets up a Three.js environment, initializes a scene, 
            and displays a simple animated object related to the subject matter.
        """
        task_description = dedent(f"""
        Your task is to generate a **fully functional HTML page** that initializes a Three.js scene 
        and includes dynamic animations related to the subject **{subject}**.

        **Project Overview:**
        - **Subject:** {subject}
        - **Complexity Level:** {complexity}
        - **Interactivity:** {"Enabled" if interactive else "Static"}
        - **Theme:** {theme}

        **Requirements:**
        1. **HTML Structure:**
           - Create a well-formed HTML document with a `<canvas>` element for rendering the Three.js scene.
           - Ensure that the Three.js library is correctly included via a `<script>` tag.

        2. **JavaScript (Three.js) Initialization:**
           - Set up a basic Three.js environment, including:
             - **Scene**
             - **Camera** (PerspectiveCamera)
             - **Renderer** (linked to the `<canvas>` element)
             - **Light sources** (to enhance visibility)
             - **Basic object(s)** (e.g., rotating cube, floating sphere, or something subject-related)
           - Implement a simple animation loop to bring the scene to life.

        3. **Interactive Elements (if enabled):**
           - If interactivity is enabled, include:
             - **OrbitControls** for mouse movement (zoom, rotate, pan).
             - Event listeners for user interactions (clicking, hovering).
             - Dynamic object transformations or color changes based on input.

        4. **Aesthetic & Design:**
           - Apply CSS to make the page visually appealing and aligned with the theme `{theme}`.
           - Ensure smooth animations and transitions.

        5. **Code Quality:**
           - Ensure the JavaScript code is modular, well-commented, and easy to modify.
           - Provide explanations or inline comments for key logic.

        **Output:**
        A complete HTML page that, when opened in a browser, renders a Three.js scene with animations and interactive elements (if enabled).

        **Tip:** {self.__tip_section()}
        """)

        return Task(
            description=task_description,
            agent=agent,
            expected_output="A self-contained HTML file that sets up a complete Three.js environment with animations and interactive features."
        )

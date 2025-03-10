from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os
import logging
from typing import Optional, Literal
import textwrap

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Define the input schema for the tool
class ThreeJSToolInput(BaseModel):
    """Input schema for the HTML + Three.js Generator Tool."""
    concept: str = Field(..., description="The concept to visualize using Three.js.")
    output_dir: Optional[str] = Field(
        default=None,
        description="Directory where the generated HTML file will be saved. Defaults to 'threejs_html' in the current directory.",
    )

class ThreeJSGeneratorTool(BaseTool):
    """Tool that generates complete HTML files embedding Three.js visualizations using standardized templates."""
    
    # Annotate the fields to avoid Pydantic errors
    name: Literal["threejs_generator_tool"] = "threejs_generator_tool"
    description: str = "Generate complete HTML files with embedded Three.js visualization scripts based on structured templates."
    args_schema: type[BaseModel] = ThreeJSToolInput  # Use the structured input schema

    def __init__(self):
        super().__init__()
        # Updated template to generate a full HTML file with embedded Three.js code.
        self._template = textwrap.dedent("""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{concept} Visualization</title>
            <style>
                /* Basic styling for a full-screen canvas */
                body {{ margin: 0; overflow: hidden; }}
            </style>
        </head>
        <body>
            <!-- The Three.js canvas will be appended automatically -->
            <script type="module">
                // Import Three.js and OrbitControls from a CDN
                import * as THREE from 'https://unpkg.com/three@0.152.0/build/three.module.js';
                import {{ OrbitControls }} from 'https://unpkg.com/three@0.152.0/examples/jsm/controls/OrbitControls.js';

                // THREE.js Visualization: {concept}
                // Generated using HTML template v1.0
                class {class_name} {{
                    constructor() {{
                        // Scene setup
                        this.scene = new THREE.Scene();
                        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                        this.renderer = new THREE.WebGLRenderer({{ antialias: true }});

                        // Standard initialization
                        this.initScene();
                        this.setupLighting();
                        this.createBaseGeometry();
                        this.addControls();
                        this.setupResizeHandler();
                    }}

                    initScene() {{
                        // Configure renderer and camera
                        this.renderer.setSize(window.innerWidth, window.innerHeight);
                        this.renderer.setClearColor(0xf0f0f0);
                        document.body.appendChild(this.renderer.domElement);
                        this.camera.position.z = 5;
                    }}

                    setupLighting() {{
                        // Standard three-point lighting setup
                        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
                        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                        directionalLight.position.set(5, 5, 5);

                        this.scene.add(ambientLight);
                        this.scene.add(directionalLight);
                    }}

                    createBaseGeometry() {{
                        // Core visualization components: a rotating cube
                        const geometry = new THREE.BoxGeometry(1, 1, 1);
                        const material = new THREE.MeshPhongMaterial({{
                            color: 0x00ff00,
                            specular: 0x111111,
                            shininess: 100
                        }});

                        this.mesh = new THREE.Mesh(geometry, material);
                        this.scene.add(this.mesh);
                    }}

                    addControls() {{
                        // Interactive controls
                        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
                        this.controls.enableDamping = true;
                        this.controls.dampingFactor = 0.05;
                    }}

                    setupResizeHandler() {{
                        // Responsive window handling
                        window.addEventListener('resize', () => {{
                            this.camera.aspect = window.innerWidth / window.innerHeight;
                            this.camera.updateProjectionMatrix();
                            this.renderer.setSize(window.innerWidth, window.innerHeight);
                        }});
                    }}

                    animate() {{
                        // Animation loop with proper frame rate handling
                        requestAnimationFrame(() => this.animate());
                        this.controls.update();

                        // Base rotation animation
                        this.mesh.rotation.x += 0.01;
                        this.mesh.rotation.y += 0.01;

                        this.renderer.render(this.scene, this.camera);
                    }}
                }}

                // Initialize and start visualization
                const visualization = new {class_name}();
                visualization.animate();
            </script>
        </body>
        </html>
        """)

    def _run(self, concept: str, output_dir: Optional[str] = None) -> str:
        """
        Generate an HTML file with embedded Three.js code following strict coding standards and template rules.
        
        Args:
            concept (str): The visualization concept to implement.
            output_dir (Optional[str]): Directory to save the generated HTML file. Defaults to 'threejs_html'.
            
        Returns:
            str: Generated HTML code with standardized structure.
        """
        try:
            # Generate a valid class name from the concept
            class_name = concept.replace(' ', '').replace('-', '') + 'Visualization'
            if class_name[0].isdigit():
                class_name = 'Viz' + class_name

            # Insert into the HTML template
            generated_code = self._template.format(
                concept=concept,
                class_name=class_name
            )

            # Determine output directory and ensure it exists
            output_dir = output_dir or os.path.join(os.getcwd(), "threejs_html")
            os.makedirs(output_dir, exist_ok=True)

            # Save the generated HTML file
            output_path = os.path.join(output_dir, f"{class_name}.html")
            with open(output_path, 'w', encoding="utf-8") as f:
                f.write(generated_code)
            
            logger.info(f"HTML file with Three.js visualization generated at {output_path}")
            return generated_code
            
        except Exception as e:
            logger.error(f"HTML generation failed: {e}")
            return f"Error generating HTML: {str(e)}"

    def _arun(self, concept: str, output_dir: Optional[str] = None):
        raise NotImplementedError("Async version not implemented")

    # Optional: Custom caching mechanism
    def cache_function(self, args: dict, result: str) -> bool:
        """
        Cache the result only if the generated HTML is longer than 500 characters.
        """
        return len(result) > 500

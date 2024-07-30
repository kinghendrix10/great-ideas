# File: data_analysis_app/agents/business_model_canvas_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput
import matplotlib.pyplot as plt
import io

class BusinessModelCanvasCreator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.canvas_prompt = BasicPrompt()
        self.structure_output = dspy.ChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        canvas_content = self.canvas_prompt(
            input_description="A business idea for creating a Business Model Canvas",
            output_description="Content for each section of the Business Model Canvas",
            context=f"""
            Use all previous analyses to create a comprehensive Business Model Canvas:
            {previous_analyses}
            Provide concise content for key partners, activities, resources, value propositions, customer relationships, channels, customer segments, cost structure, and revenue streams.
            Ensure the canvas aligns with and synthesizes all previous analyses.
            """,
            query=user_proj,
            search_results=[]  # No search results needed for canvas creation
        )
        
        structured_output = self.structure_output(
            input_description="Business Model Canvas content",
            query=canvas_content.response,
            search_results=[]
        )
        
        canvas_dict = structured_output.response
        
        # Create visual representation
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
        ax.set_facecolor('black')
        ax.axis('off')
        
        # Define the layout of the canvas
        layout = [
            ('Key Partners', 0, 0, 2, 3),
            ('Key Activities', 2, 0, 2, 2),
            ('Value Propositions', 4, 0, 2, 3),
            ('Customer Relationships', 6, 0, 2, 2),
            ('Customer Segments', 8, 0, 2, 3),
            ('Key Resources', 2, 2, 2, 1),
            ('Channels', 6, 2, 2, 1),
            ('Cost Structure', 0, 3, 5, 1),
            ('Revenue Streams', 5, 3, 5, 1)
        ]

        # Draw the canvas
        for (title, x, y, w, h) in layout:
            rect = plt.Rectangle((x, y), w, h, fill=False, ec='white')
            ax.add_patch(rect)
            ax.text(x + w/2, y + h - 0.1, title, ha='center', va='top', color='white', wrap=True)
            ax.text(x + w/2, y + h/2, canvas_dict.get(title.lower().replace(" ", "_"), ""), ha='center', va='center', color='white', wrap=True)

        # Save the figure to a bytes object
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        
        return {
            "description": canvas_dict,
            "image": buf.getvalue()
        }

def create_canvas(user_proj, previous_analyses):
    creator = BusinessModelCanvasCreator()
    return creator(user_proj, previous_analyses)

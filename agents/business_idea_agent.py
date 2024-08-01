# great-ideas/agents/business_idea_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput, BasicChainOfThought
from utils.web_search import web_search

class BusinessIdeaAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.analyze_prompt = BasicChainOfThought(BasicPrompt)
        self.structure_output = BasicChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        search_query = f"recent trends and innovations in {user_proj}"
        search_results = web_search(search_query)

        analysis = self.analyze_prompt(
            input_description="A business idea to be analyzed",
            output_description="A comprehensive analysis of the business idea",
            context="Provide a SWOT analysis, viability score, and recommendations. Incorporate recent trends and innovations from the web search results.",
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Business idea analysis",
            query=analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = BusinessIdeaAnalyzer()
    return analyzer(user_proj, previous_analyses)
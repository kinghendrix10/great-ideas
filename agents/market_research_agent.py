# great-ideas/agents/market_research_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput
from utils.web_search import web_search

class MarketResearchAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.research_prompt = BasicPrompt()
        self.structure_output = dspy.ChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        
        search_query = f"market analysis {user_proj}"
        search_results = web_search(search_query)

        research = self.research_prompt(
            input_description="A business idea for market research",
            output_description="Comprehensive market analysis",
            context=f"""
            Previous business idea analysis: {business_idea}
            Include TAM, SAM, SOM estimates, market trends, growth forecast, and competitive landscape. 
            Use the provided web search results to supplement your analysis with current market data.
            Ensure your analysis aligns with and builds upon the previous business idea analysis.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Market research analysis",
            query=research.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = MarketResearchAnalyzer()
    return analyzer(user_proj, previous_analyses)

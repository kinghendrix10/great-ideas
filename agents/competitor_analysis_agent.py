# great-ideas/agents/competitor_analysis_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput, BasicChainOfThought
from utils.web_search import web_search

class CompetitorAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.competitor_prompt = BasicChainOfThought(BasicPrompt)
        self.structure_output = BasicChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        target_audience = previous_analyses.get('target_audience', {})

        search_query = f"competitors analysis {user_proj}"
        search_results = web_search(search_query)

        competitor_analysis = self.competitor_prompt(
            input_description="A business idea for competitor analysis",
            output_description="Comprehensive competitor analysis",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous target audience analysis: {target_audience}
            Identify key competitors, their strengths and weaknesses, and strategies to differentiate.
            Use the web search results to supplement your analysis with current competitor information.
            Ensure your analysis aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Competitor analysis",
            query=competitor_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = CompetitorAnalyzer()
    return analyzer(user_proj, previous_analyses)

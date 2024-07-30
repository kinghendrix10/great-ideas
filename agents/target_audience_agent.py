# great-ideas/agents/target_audience_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput
from utils.web_search import web_search

class TargetAudienceAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.audience_prompt = BasicPrompt()
        self.structure_output = dspy.ChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})

        search_query = f"target audience demographics psychographics {user_proj}"
        search_results = web_search(search_query)

        audience_analysis = self.audience_prompt(
            input_description="A business idea for target audience analysis",
            output_description="Detailed target audience profile",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Identify and profile the initial target audience, including demographics, psychographics, and engagement strategies.
            Use the web search results to supplement your analysis with current demographic and psychographic data.
            Ensure your analysis aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Target audience analysis",
            query=audience_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = TargetAudienceAnalyzer()
    return analyzer(user_proj, previous_analyses)

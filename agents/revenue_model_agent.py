# great-ideas/agents/revenue_model_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput
from utils.web_search import web_search

class RevenueModelAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.model_prompt = BasicPrompt()
        self.structure_output = dspy.ChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        target_audience = previous_analyses.get('target_audience', {})
        competitor_analysis = previous_analyses.get('competitor_analysis', {})

        search_query = f"successful revenue models {user_proj}"
        search_results = web_search(search_query)

        model_analysis = self.model_prompt(
            input_description="A business idea for revenue model analysis",
            output_description="Suggested revenue models with pros, cons, and estimated streams",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous target audience analysis: {target_audience}
            Previous competitor analysis: {competitor_analysis}
            Provide 2-3 recommended revenue models with detailed analysis.
            Use the web search results to identify successful revenue models in similar industries.
            Ensure your analysis aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Revenue model analysis",
            query=model_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = RevenueModelAnalyzer()
    return analyzer(user_proj, previous_analyses)

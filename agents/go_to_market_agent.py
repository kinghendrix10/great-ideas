# great-ideas/agents/go_to_market_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput
from utils.web_search import web_search

class GoToMarketAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.gtm_prompt = BasicPrompt()
        self.structure_output = dspy.ChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        target_audience = previous_analyses.get('target_audience', {})
        competitor_analysis = previous_analyses.get('competitor_analysis', {})
        revenue_model = previous_analyses.get('revenue_model', {})
        mvp_features = previous_analyses.get('mvp_features', {})

        search_query = f"successful go-to-market strategies {user_proj}"
        search_results = web_search(search_query)

        gtm_analysis = self.gtm_prompt(
            input_description="A business idea for go-to-market strategy analysis",
            output_description="Comprehensive go-to-market strategy",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous target audience analysis: {target_audience}
            Previous competitor analysis: {competitor_analysis}
            Previous revenue model analysis: {revenue_model}
            Previous MVP features analysis: {mvp_features}
            Include target customer segments, marketing channels, pricing strategies, and customer acquisition plan.
            Use the web search results to identify successful go-to-market strategies in similar markets.
            Ensure your strategy aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Go-to-market strategy analysis",
            query=gtm_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = GoToMarketAnalyzer()
    return analyzer(user_proj, previous_analyses)

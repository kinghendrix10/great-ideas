# great-ideas/agents/mvp_features_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput
from utils.web_search import web_search

class MVPFeaturesAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.features_prompt = BasicPrompt()
        self.structure_output = dspy.ChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        target_audience = previous_analyses.get('target_audience', {})
        competitor_analysis = previous_analyses.get('competitor_analysis', {})
        revenue_model = previous_analyses.get('revenue_model', {})

        search_query = f"popular features MVP {user_proj}"
        search_results = web_search(search_query)

        features_analysis = self.features_prompt(
            input_description="A business idea for MVP features analysis",
            output_description="List of core MVP features with prioritization and requirements",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous target audience analysis: {target_audience}
            Previous competitor analysis: {competitor_analysis}
            Previous revenue model analysis: {revenue_model}
            Provide 5-7 core MVP features, prioritize them, and suggest metrics for success.
            Use the web search results to identify popular features in similar products or services.
            Ensure your analysis aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="MVP features analysis",
            query=features_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = MVPFeaturesAnalyzer()
    return analyzer(user_proj, previous_analyses)

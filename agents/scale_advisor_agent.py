# great-ideas/agents/scale_advisor_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput, BasicChainOfThought
from utils.web_search import web_search

class ScaleAdvisorAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.scale_prompt = BasicChainOfThought(BasicPrompt)
        self.structure_output = BasicChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        revenue_model = previous_analyses.get('revenue_model', {})
        go_to_market = previous_analyses.get('go_to_market', {})
        investment_strategy = previous_analyses.get('investment_strategy', {})

        search_query = f"scaling strategies {user_proj}"
        search_results = web_search(search_query)

        scale_analysis = self.scale_prompt(
            input_description="A business idea for scaling advice",
            output_description="Comprehensive scaling strategy and advice",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous revenue model analysis: {revenue_model}
            Previous go-to-market strategy: {go_to_market}
            Previous investment strategy: {investment_strategy}
            Include key milestones, potential challenges, resource requirements, and strategies for maintaining quality during growth.
            Use the web search results to identify successful scaling strategies in similar industries.
            Ensure your advice aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Scaling advice analysis",
            query=scale_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = ScaleAdvisorAnalyzer()
    return analyzer(user_proj, previous_analyses)

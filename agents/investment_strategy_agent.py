# great-ideas/agents/investment_strategy_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput
from utils.web_search import web_search

class InvestmentStrategyAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.strategy_prompt = BasicPrompt()
        self.structure_output = dspy.ChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        revenue_model = previous_analyses.get('revenue_model', {})
        go_to_market = previous_analyses.get('go_to_market', {})

        search_query = f"investment trends {user_proj}"
        search_results = web_search(search_query)

        strategy_analysis = self.strategy_prompt(
            input_description="A business idea for investment strategy analysis",
            output_description="Comprehensive investment strategy",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous revenue model analysis: {revenue_model}
            Previous go-to-market strategy: {go_to_market}
            Include value proposition, financial projections, funding requirements, and exit strategy options.
            Use the web search results to identify recent investment trends in the industry.
            Ensure your strategy aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Investment strategy analysis",
            query=strategy_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = InvestmentStrategyAnalyzer()
    return analyzer(user_proj, previous_analyses)

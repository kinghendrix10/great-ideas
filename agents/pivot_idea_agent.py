# great-ideas/agents/pivot_idea_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput, BasicChainOfThought
from utils.web_search import web_search

class PivotIdeaAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.pivot_prompt = BasicChainOfThought(BasicPrompt)
        self.structure_output = BasicChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        competitor_analysis = previous_analyses.get('competitor_analysis', {})
        revenue_model = previous_analyses.get('revenue_model', {})

        search_query = f"successful business pivots {user_proj}"
        search_results = web_search(search_query)

        pivot_analysis = self.pivot_prompt(
            input_description="A business idea for pivot options analysis",
            output_description="Alternative ideas and pivot options",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous competitor analysis: {competitor_analysis}
            Previous revenue model analysis: {revenue_model}
            Generate related business ideas, pivot options, and evaluate their feasibility.
            Use the web search results to identify successful pivot stories in similar industries.
            Ensure your analysis aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Pivot ideas analysis",
            query=pivot_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = PivotIdeaAnalyzer()
    return analyzer(user_proj, previous_analyses)

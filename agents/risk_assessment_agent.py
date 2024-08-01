# great-ideas/agents/risk_assessment_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput, BasicChainOfThought
from utils.web_search import web_search

class RiskAssessmentAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.risk_prompt = BasicChainOfThought(BasicPrompt)
        self.structure_output = BasicChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        competitor_analysis = previous_analyses.get('competitor_analysis', {})
        investment_strategy = previous_analyses.get('investment_strategy', {})
        scale_advisor = previous_analyses.get('scale_advisor', {})

        search_query = f"business risks {user_proj}"
        search_results = web_search(search_query)

        risk_analysis = self.risk_prompt(
            input_description="A business idea for risk assessment",
            output_description="Comprehensive risk assessment",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous competitor analysis: {competitor_analysis}
            Previous investment strategy: {investment_strategy}
            Previous scaling advice: {scale_advisor}
            Identify key risks, their probability and impact, and provide mitigation strategies.
            Use the web search results to identify recent risk factors affecting similar businesses or industries.
            Ensure your assessment aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Risk assessment analysis",
            query=risk_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = RiskAssessmentAnalyzer()
    return analyzer(user_proj, previous_analyses)
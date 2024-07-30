# File: data_analysis_app/agents/legal_compliance_agent.py
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput
from utils.web_search import web_search

class LegalComplianceAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.legal_prompt = BasicPrompt()
        self.structure_output = dspy.ChainOfThought(StructuredOutput)

    def forward(self, user_proj, previous_analyses):
        business_idea = previous_analyses.get('business_idea', {})
        market_research = previous_analyses.get('market_research', {})
        revenue_model = previous_analyses.get('revenue_model', {})
        risk_assessment = previous_analyses.get('risk_assessment', {})

        search_query = f"legal compliance regulations {user_proj}"
        search_results = web_search(search_query)

        legal_analysis = self.legal_prompt(
            input_description="A business idea for legal and compliance analysis",
            output_description="Legal and compliance considerations",
            context=f"""
            Previous business idea analysis: {business_idea}
            Previous market research: {market_research}
            Previous revenue model analysis: {revenue_model}
            Previous risk assessment: {risk_assessment}
            Provide insights on industry-specific regulations, licensing requirements, and potential legal risks.
            Use the web search results to identify recent regulatory changes or legal issues in the industry.
            Ensure your analysis aligns with and builds upon the previous analyses.
            """,
            query=user_proj,
            search_results=search_results
        )
        
        structured_output = self.structure_output(
            input_description="Legal and compliance analysis",
            query=legal_analysis.response,
            search_results=search_results
        )
        
        return structured_output.response

def analyze(user_proj, previous_analyses):
    analyzer = LegalComplianceAnalyzer()
    return analyzer(user_proj, previous_analyses)

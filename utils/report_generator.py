# great-ideas/utils/report_generator.py
from agents import (
    business_idea_analyze, market_research_analyze, revenue_model_analyze,
    mvp_features_analyze, investment_strategy_analyze, go_to_market_analyze,
    scale_advisor_analyze, competitor_analysis_analyze, pivot_idea_analyze,
    target_audience_analyze, risk_assessment_analyze, legal_compliance_analyze,
    create_canvas
)
import dspy
from models.dspy_config import BasicPrompt, StructuredOutput, BasicChainOfThought

class ReportSynthesizer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.synthesize_prompt = BasicChainOfThought(BasicPrompt)
        self.structure_output = BasicChainOfThought(StructuredOutput)

    def forward(self, report_sections):
        synthesis = self.synthesize_prompt(
            input_description="Complete business report sections",
            output_description="Synthesized executive summary",
            context="Provide a brief overview, key findings, overall assessment, top recommendations, and conclusion",
            query=str(report_sections),
            search_results=[]  # No search results needed for synthesis
        )
        
        structured_output = self.structure_output(
            input_description="Executive summary",
            query=synthesis.response,
            search_results=[]
        )
        
        return structured_output.response

def generate_report(user_proj):
    report = {}
    
    # Sequence of agent calls
    agent_sequence = [
        ("business_idea", business_idea_analyze),
        ("market_research", market_research_analyze),
        ("target_audience", target_audience_analyze),
        ("competitor_analysis", competitor_analysis_analyze),
        ("revenue_model", revenue_model_analyze),
        ("mvp_features", mvp_features_analyze),
        ("go_to_market", go_to_market_analyze),
        ("investment_strategy", investment_strategy_analyze),
        ("scale_advisor", scale_advisor_analyze),
        ("pivot_idea", pivot_idea_analyze),
        ("risk_assessment", risk_assessment_analyze),
        ("legal_compliance", legal_compliance_analyze)
    ]
    
    for key, agent_func in agent_sequence:
        report[key] = agent_func(user_proj, report)
    
    # Business Model Canvas is created last, using all accumulated data
    report["business_model_canvas"] = create_canvas(user_proj, report)

    # Synthesize the report
    synthesizer = ReportSynthesizer()
    summary = synthesizer(report)

    # Add summary to the report
    report["summary"] = summary

    return report

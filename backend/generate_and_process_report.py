import asyncio
import sys
import os
import json
import pandas as pd
from lionagi.core.message import System, Instruction
from lionagi.core.executor.graph_executor import GraphExecutor
from lionagi.core.engine.instruction_map_engine import InstructionMapEngine
from lionagi.core.agent.base_agent import BaseAgent

def custom_json_serializer(obj):
    if isinstance(obj, str):
        return obj.replace('\\', '\\\\').replace('\n', '\\n')
    return obj

async def main():
    print("Starting generate_and_process_report.py", file=sys.stderr)

    user_proj = sys.argv[1]
    model = sys.argv[2]
    api_key = sys.argv[3]

    print(f"Received project: {user_proj}", file=sys.stderr)
    print(f"Using model: {model}", file=sys.stderr)

    os.environ["OPENAI_API_KEY"] = api_key

        # Agent Output Parsers
    def master_parser(agent):
        output = []
        for branch in agent.executable.branches.values():
            output.append(branch.to_df())
        return output

    def assistant_parser(agent):
        output = []
        for branch in agent.executable.branches.values():
            for msg in branch.to_chat_messages():
                if msg["role"] == "assistant":
                    output.append(msg["content"])
        return output
    
    # Define Business Idea Agent
    business_idea = System(system="An experienced business analyst with a keen eye for market opportunities and potential pitfalls")
    business_idea_inst = Instruction(
        f"""As an expert business analyst, evaluate the given business idea: {user_proj}.
        Assess its viability, potential, and uniqueness in the market. Identify key strengths, weaknesses, opportunities, and threats.
        Provide an objective analysis of the idea, potential for success and any areas that need improvement."""
    )
    graph_business_idea = GraphExecutor()
    graph_business_idea.add_node(business_idea)
    graph_business_idea.add_node(business_idea_inst)
    graph_business_idea.add_edge(business_idea, business_idea_inst)

    business_idea_exe = InstructionMapEngine()

    BusinessIdea = BaseAgent(
        structure=graph_business_idea,
        executable=business_idea_exe,
        output_parser=master_parser
    )
    # Define Market Research Agent
    market_research = System(system="A data-driven market research specialist with extensive knowledge of various industries and market trends.")
    market_research_inst = Instruction(
        """As a seasoned market research specialist, conduct a comprehensive market analysis for the given business idea.
        Determine the Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM).
        Identify key market trends, growth potential, and competitive landscape. Provide data-backed insights to support your analysis."""
        )

    graph_market_research = GraphExecutor()
    graph_market_research.add_node(market_research)
    graph_market_research.add_node(market_research_inst)
    graph_market_research.add_edge(market_research, market_research_inst)

    market_research_exe = InstructionMapEngine()

    MarketResearch = BaseAgent(
        structure=graph_market_research,
        executable=market_research_exe,
        output_parser=assistant_parser,
    )

    graph_business_idea.add_node(MarketResearch)
    graph_business_idea.add_edge(business_idea_inst, MarketResearch)

    # # Define Revenue Model Agent
    # revenue_model = System(system="A creative financial strategist with expertise in various business models and revenue streams.")
    # revenue_model_inst = Instruction(
    #     """As an innovative financial strategist, suggest suitable revenue models for the given business idea.
    #     Consider the target market, industry dynamics, and potential scalability.
    #     Recommend the most appropriate model(s), providing pros and cons for each.
    #     Estimate potential revenue streams and explain how they align with the business goals."""
    #     )

    # graph_revenue_model = GraphExecutor()
    # graph_revenue_model.add_node(revenue_model)
    # graph_revenue_model.add_node(revenue_model_inst)
    # graph_revenue_model.add_edge(revenue_model, revenue_model_inst)

    # revenue_model_exe = InstructionMapEngine()

    # RevenueModel = BaseAgent(
    #     structure=graph_revenue_model,
    #     executable=revenue_model_exe,
    #     output_parser=assistant_parser
    # )

    # graph_business_idea.add_node(RevenueModel)
    # graph_business_idea.add_edge(MarketResearch, RevenueModel)
    # # Define MVP Feature Agent
    # mvp_features = System(system="A product development expert with a focus on lean startup methodologies and user-centric design.")
    # mvp_features_inst = Instruction(
    #     """As a product development expert, propose suitable Minimum Viable Product (MVP) features for the given business idea.
    #     Focus on core functionalities that demonstrate value and address the main problem.
    #     Prioritize features based on development time and impact.
    #     Suggest a timeline for MVP development and recommend metrics to measure its success."""
    #     )

    # graph_mvp_features = GraphExecutor()
    # graph_mvp_features.add_node(mvp_features)
    # graph_mvp_features.add_node(mvp_features_inst)
    # graph_mvp_features.add_edge(mvp_features, mvp_features_inst)

    # mvp_features_exe = InstructionMapEngine()

    # MVPFeatures = BaseAgent(
    #     structure=graph_mvp_features,
    #     executable=mvp_features_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(MVPFeatures)
    # graph_business_idea.add_edge(RevenueModel, MVPFeatures)
    # # Define Investor Pitch Agent
    # investor_pitch = System(system="A seasoned startup pitch coach with a track record of helping entrepreneurs secure funding.")
    # investor_pitch_inst = Instruction(
    #     """As an experienced pitch coach, create a compelling investor pitch template for the given business idea.
    #     Develop a clear and concise value proposition. Outline the problem, solution, and market opportunity.
    #     Highlight the team's expertise and competitive advantage. Include key financial projections and funding requirements.
    #     Ensure the pitch is tailored to attract potential investors."""
    #     )

    # graph_investor_pitch = GraphExecutor()
    # graph_investor_pitch.add_node(investor_pitch)
    # graph_investor_pitch.add_node(investor_pitch_inst)
    # graph_investor_pitch.add_edge(investor_pitch, investor_pitch_inst)

    # investor_pitch_exe = InstructionMapEngine()

    # InvestorPitch = BaseAgent(
    #     structure=graph_investor_pitch,
    #     executable=investor_pitch_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(InvestorPitch)
    # graph_business_idea.add_edge(MVPFeatures, InvestorPitch)
    # # Define Go-to-Market Agent
    # gt_market = System(system="A marketing expert specializing in launch strategies and customer acquisition for startups.")
    # gt_market_inst = Instruction(
    #     """As a go-to-market strategist, devise effective strategies for the given business idea.
    #     Identify target customer segments and recommend appropriate marketing channels.
    #     Suggest pricing strategies and develop a comprehensive customer acquisition plan.
    #     Consider the target audience, market conditions, and available resources to create a tailored approach."""
    #     )

    # graph_gt_market = GraphExecutor()
    # graph_gt_market.add_node(gt_market)
    # graph_gt_market.add_node(gt_market_inst)
    # graph_gt_market.add_edge(gt_market, gt_market_inst)

    # gt_market_exe = InstructionMapEngine()

    # GTMarket = BaseAgent(
    #     structure=graph_gt_market,
    #     executable=gt_market_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(GTMarket)
    # graph_business_idea.add_edge(InvestorPitch, GTMarket)
    # # Define Scale Advisor Agent
    # scale_advisor = System(system="A seasoned startup pitch coach with a track record of helping entrepreneurs secure funding")
    # scale_advisor_inst = Instruction(
    #     """As an experienced pitch coach, create a compelling investor pitch template for the given business idea.
    #     Develop a clear and concise value proposition. Outline the problem, solution, and market opportunity.
    #     Highlight the team's expertise and competitive advantage. Include key financial projections and funding requirements.
    #     Ensure the pitch is tailored to attract potential investors."""
    #     )

    # graph_scale_advisor = GraphExecutor()
    # graph_scale_advisor.add_node(scale_advisor)
    # graph_scale_advisor.add_node(scale_advisor_inst)
    # graph_scale_advisor.add_edge(scale_advisor, scale_advisor_inst)

    # scale_advisor_exe = InstructionMapEngine()

    # ScaleAdvisor = BaseAgent(
    #     structure=graph_scale_advisor,
    #     executable=scale_advisor_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(ScaleAdvisor)
    # graph_business_idea.add_edge(GTMarket, ScaleAdvisor)
    # # Define Funding Consultant Agent
    # fund_consultant = System(system="A fundraising expert with deep knowledge of various funding options and investor networks.")
    # fund_consultant_inst = Instruction(
    #     """As a capital raising consultant, offer guidance on raising funds for the startup.
    #     Explain different funding sources (e.g., VC, angel investors, crowdfunding) and recommend the most suitable options for the current business stage.
    #     Provide tips for successful fundraising pitches and advise on equity dilution and valuation considerations."""
    #     )

    # graph_fund_consultant = GraphExecutor()
    # graph_fund_consultant.add_node(fund_consultant)
    # graph_fund_consultant.add_node(fund_consultant_inst)
    # graph_fund_consultant.add_edge(fund_consultant, fund_consultant_inst)

    # fund_consultant_exe = InstructionMapEngine()

    # FundConsultant = BaseAgent(
    #     structure=graph_fund_consultant,
    #     executable=fund_consultant_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(FundConsultant)
    # graph_business_idea.add_edge(ScaleAdvisor, FundConsultant)
    # # Define Competitor Analysis Agent
    # comp_analysis = System(system="A strategic intelligence analyst specializing in competitive landscape assessment.")
    # comp_analysis_inst = Instruction(
    #     """As a competitive intelligence analyst, conduct a thorough analysis of direct and indirect competitors for the given business idea.
    #     Identify key players, analyze their strengths and weaknesses, and compare features, pricing, and market positioning.
    #     Highlight competitive advantages and disadvantages, and suggest strategies to differentiate from competitors."""
    #     )

    # graph_comp_analysis = GraphExecutor()
    # graph_comp_analysis.add_node(comp_analysis)
    # graph_comp_analysis.add_node(comp_analysis_inst)
    # graph_comp_analysis.add_edge(comp_analysis, comp_analysis_inst)

    # comp_analysis_exe = InstructionMapEngine()

    # CompAnalysis = BaseAgent(
    #     structure=graph_comp_analysis,
    #     executable=comp_analysis_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(CompAnalysis)
    # graph_business_idea.add_edge(FundConsultant, CompAnalysis)
    # # Define Pivot Ideation Agent
    # pivot_idea = System(system="An innovation consultant with expertise in business model transformation and market adaptation.")
    # pivot_idea_inst = Instruction(
    #     """As an innovation consultant, generate alternative ideas and pivot options related to the original business concept.
    #     Suggest related business ideas in the same industry and propose pivot options that leverage existing resources.
    #     Identify potential new markets or customer segments and evaluate the feasibility of each pivot option."""
    #     )

    # graph_pivot_idea = GraphExecutor()
    # graph_pivot_idea.add_node(pivot_idea)
    # graph_pivot_idea.add_node(pivot_idea_inst)
    # graph_pivot_idea.add_edge(pivot_idea, pivot_idea_inst)

    # pivot_idea_exe = InstructionMapEngine()

    # PivotIdea = BaseAgent(
    #     structure=graph_pivot_idea,
    #     executable=pivot_idea_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(PivotIdea)
    # graph_business_idea.add_edge(CompAnalysis, PivotIdea)
    # # Define Market Explorer Agent
    # market_explorer = System(system="A business development strategist with a knack for identifying synergies and expansion opportunities.")
    # market_explorer_inst = Instruction(
    #     """As a business development strategist, identify and analyze adjacent markets that the business could potentially enter after scaling.
    #     Explore related industries or market segments and assess the potential for expansion.
    #     Evaluate required resources and capabilities for market entry and suggest strategies for successful market expansion."""
    #     )

    # graph_market_explorer = GraphExecutor()
    # graph_market_explorer.add_node(market_explorer)
    # graph_market_explorer.add_node(market_explorer_inst)
    # graph_market_explorer.add_edge(market_explorer, market_explorer_inst)

    # market_explorer_exe = InstructionMapEngine()

    # MarketExplorer = BaseAgent(
    #     structure=graph_market_explorer,
    #     executable=market_explorer_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(MarketExplorer)
    # graph_business_idea.add_edge(PivotIdea, MarketExplorer)
    # # Define Target Audience Agent
    # target_audience = System(system="A customer segmentation expert with a deep understanding of demographic and psychographic profiling.")
    # target_audience_inst = Instruction(
    #     """As a customer segmentation expert, identify and profile the initial target audience for the given business idea.
    #     Conduct primary and secondary research to identify target demographics, create detailed customer personas, analyze customer needs, preferences, and behaviors.
    #     Recommend strategies to reach and engage the target audience effectively."""
    #     )

    # graph_target_audience = GraphExecutor()
    # graph_target_audience.add_node(target_audience)
    # graph_target_audience.add_node(target_audience_inst)
    # graph_target_audience.add_edge(target_audience, target_audience_inst)

    # target_audience_exe = InstructionMapEngine()

    # TargetAudience = BaseAgent(
    #     structure=graph_target_audience,
    #     executable=target_audience_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(TargetAudience)
    # graph_business_idea.add_edge(MarketExplorer, TargetAudience)
    # # Define Early Adopter Agent
    # early_adopter = System(system="A community-building specialist with experience in cultivating early adopter communities for startups.")
    # early_adopter_inst = Instruction(
    #     """As a community-building specialist, develop techniques and strategies to entice early adopters for the given business idea.
    #     Identify characteristics of potential early adopters, suggest incentives and promotions to attract them.
    #     Develop a communication plan to engage early adopters, and recommend feedback mechanisms to gather insights from this crucial group."""
    #     )

    # graph_early_adopter = GraphExecutor()
    # graph_early_adopter.add_node(early_adopter)
    # graph_early_adopter.add_node(early_adopter_inst)
    # graph_early_adopter.add_edge(early_adopter, early_adopter_inst)

    # early_adopter_exe = InstructionMapEngine()

    # EarlyAdopter = BaseAgent(
    #     structure=graph_early_adopter,
    #     executable=early_adopter_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(EarlyAdopter)
    # graph_business_idea.add_edge(TargetAudience, EarlyAdopter)
    # business_report = System(system="""A skilled business analyst and writer, you generate business reports with a detail overview of the business model.""")
    # business_report_inst = Instruction(
    #     """As a skilled business analyst and writer, generate a comprehensive startup report.
    #     Compile data and insights from all other agents, structure the report with clear sections and apprpriate headings,
    #     introduction, body and actionable conclusion. Ensure the report is clear, concise, and professional."""
    #     )

    # graph_business_report = GraphExecutor()
    # graph_business_report.add_node(business_report)
    # graph_business_report.add_node(business_report_inst)
    # graph_early_adopter.add_edge(business_report, business_report_inst)

    # business_report_exe = InstructionMapEngine()

    # BusinessReport = BaseAgent(
    #     structure=graph_business_report,
    #     executable=business_report_exe,
    #     output_parser=assistant_parser,
    # )

    # graph_business_idea.add_node(BusinessReport)
    # graph_business_idea.add_edge(EarlyAdopter, BusinessReport)
    
    result = await BusinessIdea.execute()
    ex = BusinessIdea.executable
    messages = pd.DataFrame(ex.branches.values())
    output = list(pd.DataFrame(messages[5].to_list())[1])

    df = pd.DataFrame(output).T
    
    # Convert DataFrame to JSON
    json_data = json.dumps(df.to_dict(orient='records'), default=custom_json_serializer)
    print(json_data, flush=True)  # This will be captured as stdout
    print("Finished generate_and_process_report.py", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import sys
import os
import json
import pandas as pd
from lionagi.core.message import System, Instruction
from lionagi.core.executor.graph_executor import GraphExecutor
from lionagi.core.engine.instruction_map_engine import InstructionMapEngine
from lionagi.core.agent.base_agent import BaseAgent

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
    
    result = await BusinessIdea.execute()
    ex = BusinessIdea.executable
    messages = pd.DataFrame(ex.branches.values())
    output = list(pd.DataFrame(messages[5].to_list())[1])

    df = pd.DataFrame(output).T
    
    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records')
    
    print(json_data, flush=True)  # This will be captured as stdout

    print("Finished generate_and_process_report.py", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())
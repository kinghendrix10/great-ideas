# great-ideas/pages/analysis.py
import streamlit as st
import json
from PIL import Image
import io

def show(report_data):
    st.markdown("<h1 style='text-align: center; color: white;'>Business Analysis Report</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs([
        "Overall Summary", "Business Idea", "Market Research", "Target Audience",
        "Competitor Analysis", "Revenue Model", "MVP Features", "Go-to-Market",
        "Investment Strategy", "Scale Advisor", "Pivot Ideas", "Risk Assessment",
        "Legal & Compliance", "Business Model Canvas"
    ])

    with tabs[0]:
        show_overall_summary(report_data["summary"])
    with tabs[1]:
        show_business_idea(report_data["business_idea"])
    with tabs[2]:
        show_market_research(report_data["market_research"])
    with tabs[3]:
        show_target_audience(report_data["target_audience"])
    with tabs[4]:
        show_competitor_analysis(report_data["competitor_analysis"])
    with tabs[5]:
        show_revenue_model(report_data["revenue_model"])
    with tabs[6]:
        show_mvp_features(report_data["mvp_features"])
    with tabs[7]:
        show_go_to_market(report_data["go_to_market"])
    with tabs[8]:
        show_investment_strategy(report_data["investment_strategy"])
    with tabs[9]:
        show_scale_advisor(report_data["scale_advisor"])
    with tabs[10]:
        show_pivot_ideas(report_data["pivot_idea"])
    with tabs[11]:
        show_risk_assessment(report_data["risk_assessment"])
    with tabs[12]:
        show_legal_compliance(report_data["legal_compliance"])
    with tabs[13]:
        show_business_model_canvas(report_data["business_model_canvas"])

def show_overall_summary(summary):
    summary_data = json.loads(summary)
    st.subheader("Business Overview")
    st.write(summary_data["business_overview"])
    
    st.subheader("Key Findings")
    for finding in summary_data["key_findings"]:
        st.write(f"- {finding}")
    
    st.subheader("Overall Assessment")
    st.write(f"Viability Score: {summary_data['viability_score']}/10")
    st.write(summary_data["assessment_justification"])
    
    st.subheader("Top Recommendations")
    for recommendation in summary_data["top_recommendations"]:
        st.write(f"- {recommendation}")
    
    st.subheader("Conclusion")
    st.write(summary_data["conclusion"])

def show_business_idea(business_idea):
    idea_data = json.loads(business_idea)
    st.subheader("SWOT Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Strengths")
        for strength in idea_data["swot"]["strengths"]:
            st.write(f"- {strength}")
        st.write("Opportunities")
        for opportunity in idea_data["swot"]["opportunities"]:
            st.write(f"- {opportunity}")
    with col2:
        st.write("Weaknesses")
        for weakness in idea_data["swot"]["weaknesses"]:
            st.write(f"- {weakness}")
        st.write("Threats")
        for threat in idea_data["swot"]["threats"]:
            st.write(f"- {threat}")
    
    st.subheader("Viability Score")
    st.write(f"{idea_data['viability_score']}/10")
    st.write(idea_data["viability_justification"])
    
    st.subheader("Recommendations")
    for recommendation in idea_data["recommendations"]:
        st.write(f"- {recommendation}")

def show_market_research(market_research):
    research_data = json.loads(market_research)
    st.subheader("Market Size")
    col1, col2, col3 = st.columns(3)
    col1.metric("TAM", research_data["market_size"]["tam"])
    col2.metric("SAM", research_data["market_size"]["sam"])
    col3.metric("SOM", research_data["market_size"]["som"])
    
    st.subheader("Market Trends")
    for trend in research_data["market_trends"]:
        st.write(f"- {trend}")
    
    st.subheader("Growth Forecast")
    st.write(research_data["growth_forecast"])
    
    st.subheader("Competitive Landscape")
    for competitor in research_data["competitors"]:
        st.write(f"- {competitor['name']}: {competitor['description']}")

def show_target_audience(target_audience):
    audience_data = json.loads(target_audience)
    st.subheader("Customer Personas")
    for persona in audience_data["personas"]:
        st.write(f"**{persona['name']}**")
        st.write(f"Demographics: {persona['demographics']}")
        st.write(f"Psychographics: {persona['psychographics']}")
        st.write("Needs:")
        for need in persona["needs"]:
            st.write(f"- {need}")
        st.write("---")
    
    st.subheader("Engagement Strategies")
    for strategy in audience_data["engagement_strategies"]:
        st.write(f"- {strategy}")

def show_competitor_analysis(competitor_analysis):
    analysis_data = json.loads(competitor_analysis)
    st.subheader("Key Competitors")
    for competitor in analysis_data["competitors"]:
        st.write(f"**{competitor['name']}**")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Strengths")
            for strength in competitor["strengths"]:
                st.write(f"- {strength}")
        with col2:
            st.write("Weaknesses")
            for weakness in competitor["weaknesses"]:
                st.write(f"- {weakness}")
        st.write("---")
    
    st.subheader("Differentiation Strategies")
    for strategy in analysis_data["differentiation_strategies"]:
        st.write(f"- {strategy}")

def show_revenue_model(revenue_model):
    model_data = json.loads(revenue_model)
    for model in model_data["revenue_models"]:
        st.subheader(model["name"])
        st.write(model["description"])
        col1, col2 = st.columns(2)
        with col1:
            st.write("Pros")
            for pro in model["pros"]:
                st.write(f"- {pro}")
        with col2:
            st.write("Cons")
            for con in model["cons"]:
                st.write(f"- {con}")
        st.write("Estimated Revenue:")
        st.write(model["estimated_revenue"])
        st.write("---")

def show_mvp_features(mvp_features):
    features_data = json.loads(mvp_features)
    st.subheader("Core MVP Features")
    for feature in features_data["features"]:
        st.write(f"**{feature['name']}**")
        st.write(f"Priority: {feature['priority']}")
        st.write(f"Description: {feature['description']}")
        st.write(f"Development Time: {feature['development_time']}")
        st.write(f"Impact: {feature['impact']}")
        st.write("---")
    
    st.subheader("Success Metrics")
    for metric in features_data["success_metrics"]:
        st.write(f"- {metric}")

def show_go_to_market(go_to_market):
    gtm_data = json.loads(go_to_market)
    st.subheader("Target Customer Segments")
    for segment in gtm_data["target_segments"]:
        st.write(f"- {segment}")
    
    st.subheader("Marketing Channels")
    for channel in gtm_data["marketing_channels"]:
        st.write(f"- {channel}")
    
    st.subheader("Pricing Strategy")
    st.write(gtm_data["pricing_strategy"])
    
    st.subheader("Customer Acquisition Plan")
    st.write(gtm_data["customer_acquisition_plan"])

def show_investment_strategy(investment_strategy):
    strategy_data = json.loads(investment_strategy)
    st.subheader("Value Proposition")
    st.write(strategy_data["value_proposition"])
    
    st.subheader("Financial Projections")
    st.write(strategy_data["financial_projections"])
    
    st.subheader("Funding Requirements")
    st.write(strategy_data["funding_requirements"])
    
    st.subheader("Exit Strategy Options")
    for option in strategy_data["exit_strategy_options"]:
        st.write(f"- {option}")

def show_scale_advisor(scale_advisor):
    advice_data = json.loads(scale_advisor)
    st.subheader("Key Milestones")
    for milestone in advice_data["key_milestones"]:
        st.write(f"- {milestone}")
    
    st.subheader("Potential Challenges")
    for challenge in advice_data["potential_challenges"]:
        st.write(f"- {challenge['challenge']}: {challenge['mitigation']}")
    
    st.subheader("Resource Requirements")
    st.write(advice_data["resource_requirements"])
    
    st.subheader("Quality Maintenance Strategies")
    for strategy in advice_data["quality_maintenance_strategies"]:
        st.write(f"- {strategy}")

def show_pivot_ideas(pivot_ideas):
    ideas_data = json.loads(pivot_ideas)
    st.subheader("Related Business Ideas")
    for idea in ideas_data["related_ideas"]:
        st.write(f"- {idea}")
    
    st.subheader("Pivot Options")
    for option in ideas_data["pivot_options"]:
        st.write(f"**{option['name']}**")
        st.write(f"Description: {option['description']}")
        st.write(f"Feasibility: {option['feasibility']}/10")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Pros")
            for pro in option["pros"]:
                st.write(f"- {pro}")
        with col2:
            st.write("Cons")
            for con in option["cons"]:
                st.write(f"- {con}")
        st.write("---")

def show_risk_assessment(risk_assessment):
    risk_data = json.loads(risk_assessment)
    for risk in risk_data["risks"]:
        st.subheader(risk["name"])
        st.write(f"Probability: {risk['probability']}/10")
        st.write(f"Impact: {risk['impact']}/10")
        st.write(f"Mitigation Strategy: {risk['mitigation_strategy']}")
        st.write("---")

def show_legal_compliance(legal_compliance):
    compliance_data = json.loads(legal_compliance)
    st.subheader("Relevant Regulations")
    for regulation in compliance_data["relevant_regulations"]:
        st.write(f"- {regulation}")
    
    st.subheader("Licensing Requirements")
    for requirement in compliance_data["licensing_requirements"]:
        st.write(f"- {requirement}")
    
    st.subheader("IP Protection Strategies")
    for strategy in compliance_data["ip_protection_strategies"]:
        st.write(f"- {strategy}")
    
    st.subheader("Data Privacy Considerations")
    for consideration in compliance_data["data_privacy_considerations"]:
        st.write(f"- {consideration}")

def show_business_model_canvas(business_model_canvas):
    canvas_data = business_model_canvas
    
    # Display the Business Model Canvas content
    st.subheader("Business Model Canvas")
    canvas_content = json.loads(canvas_data["description"])
    for section, content in canvas_content.items():
        st.write(f"**{section.replace('_', ' ').title()}**")
        st.write(content)
        st.write("---")

    # Display the Business Model Canvas image
    st.subheader("Business Model Canvas Visualization")
    canvas_image = Image.open(io.BytesIO(canvas_data["image"]))
    st.image(canvas_image, caption="Business Model Canvas", use_column_width=True)
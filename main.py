from textwrap import dedent
import streamlit as st
from crewai import Agent, Crew
from agents import MarketingAnalysisAgents
from tasks import MarketingAnalysisTasks

def main():
    st.title("Instagram Post Crew")
    st.markdown("---")

    tasks = MarketingAnalysisTasks()
    agents = MarketingAnalysisAgents()

    product_website = st.text_input(
        "What is the product website you want a marketing strategy for?"
    )
    product_details = st.text_area(
        "Any extra details about the product and/or the Instagram post you want?"
    )

    if st.button("Generate Marketing Strategy"):
        status_placeholder = st.empty()
        
        status_placeholder.info("Starting the marketing strategy generation process...")

        # Create Agents
        status_placeholder.info("Creating agents...")
        product_competitor_agent = agents.product_competitor_agent()
        strategy_planner_agent = agents.strategy_planner_agent()
        creative_agent = agents.creative_content_creator_agent()

        # Create Tasks
        status_placeholder.info("Setting up tasks for copy generation...")
        website_analysis = tasks.product_analysis(
            product_competitor_agent, product_website, product_details
        )
        market_analysis = tasks.competitor_analysis(
            product_competitor_agent, product_website, product_details
        )
        campaign_development = tasks.campaign_development(
            strategy_planner_agent, product_website, product_details
        )
        write_copy = tasks.instagram_ad_copy(creative_agent)

        # Create Crew responsible for Copy
        status_placeholder.info("Assembling copy crew and generating ad copy...")
        copy_crew = Crew(
            agents=[
                product_competitor_agent,
                strategy_planner_agent,
                creative_agent,
            ],
            tasks=[
                website_analysis,
                market_analysis,
                campaign_development,
                write_copy,
            ],
            verbose=True,
        )
        ad_copy = copy_crew.kickoff()

        # Create Crew responsible for Image
        status_placeholder.info("Setting up image generation crew...")
        senior_photographer = agents.senior_photographer_agent()
        chief_creative_director = agents.chief_creative_diretor_agent()

        # Create Tasks for Image
        status_placeholder.info("Preparing image generation tasks...")
        take_photo = tasks.take_photograph_task(
            senior_photographer, ad_copy, product_website, product_details
        )
        approve_photo = tasks.review_photo(
            chief_creative_director, product_website, product_details
        )

        status_placeholder.info("Generating and reviewing image...")
        image_crew = Crew(
            agents=[senior_photographer, chief_creative_director],
            tasks=[take_photo, approve_photo],
            verbose=True,
        )
        image = image_crew.kickoff()

        # Display results
        status_placeholder.success("Marketing strategy generated successfully!")
        st.subheader("Instagram Post Copy")
        st.write(ad_copy)
        st.subheader("Midjourney Description")
        st.write(image)

if __name__ == "__main__":
    main()
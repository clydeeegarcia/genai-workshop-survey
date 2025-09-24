import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="GenAI Workshop Review",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #2E86AB 0%, #A23B72 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .section-header {
        background-color: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #2E86AB;
        margin: 1.5rem 0 1rem 0;
        border-radius: 5px;
    }
    .success-story {
        background: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #28a745;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'survey_data' not in st.session_state:
    if os.path.exists('genai_survey_responses.json'):
        try:
            with open('genai_survey_responses.json', 'r') as f:
                st.session_state.survey_data = json.load(f)
        except:
            st.session_state.survey_data = []
    else:
        st.session_state.survey_data = []

def save_response(responses):
    """Save survey response"""
    response_data = {
        'timestamp': datetime.now().isoformat(),
        'responses': responses
    }
    st.session_state.survey_data.append(response_data)
    
    with open('genai_survey_responses.json', 'w') as f:
        json.dump(st.session_state.survey_data, f, indent=2)

def calculate_nps(scores):
    """Calculate Net Promoter Score"""
    if not scores:
        return 0
    promoters = sum(1 for score in scores if score >= 9)
    detractors = sum(1 for score in scores if score <= 6)
    return ((promoters - detractors) / len(scores)) * 100

# Main App
st.markdown("""
<div class="main-header">
    <h1>🤖 GenAI Workshop Review</h1>
    <p>Help us understand outcomes and improve future workshops</p>
</div>
""", unsafe_allow_html=True)

# Navigation
tab1, tab2 = st.tabs(["📝 Survey", "📊 Dashboard"])

with tab1:
    with st.form("genai_feedback_form"):
        
        # Contact Info
        work_email = st.text_input("Your work email")
        
        # Core Outcome Questions
        st.markdown("### 🎯 Workshop Outcomes")
        
        key_takeaway = st.text_area(
            "What's one helpful thing you took away from these workshops?",
            height=100
        )
        
        missing_coverage = st.text_area(
            "What's one thing these workshops didn't cover that you'd like to explore?",
            height=100
        )
        
        expectations = st.radio(
            "Overall, how did these workshops compare to your expectations?",
            ["I got WAY more than I was expecting from these workshops",
             "I got more than I expected",
             "I got what I was hoping for",
             "I was hoping for something more or different",
             "These workshops fell short of my expectations",
             "Not sure"]
        )
        
        # Success Stories & Application
        st.markdown("### 🚀 Practical Application")
        
        built_something = st.multiselect(
            "Did you build something with LLM Suite during or after these workshops? (Check all that apply)",
            ["I made a complex prompt",
             "I set up a custom tile in LLM Suite",
             "I wrote some custom code",
             "Something else",
             "Not yet but I plan to soon",
             "I'm not sure?"]
        )
        
        if "Something else" in built_something:
            something_else = st.text_input("Please specify what else you built:")
        
        what_created = st.text_area(
            "If yes, describe what you created.",
            height=100
        )
        
        # Workshop Rankings
        st.markdown("### 📊 Workshop Effectiveness")
        
        workshop_options = [
            "Prompting: Improving prompts with the PICO framework",
            "Prompting: Craft and iterate on complex prompts",
            "Collaborating with GenAI: Make better decisions with GenAI",
            "Collaborating with GenAI: Practice and improve performance with GenAI",
            "Coding with GenAI: Write and run code with LLM Suite",
            "Coding with GenAI: Organize and share coding projects",
            "Crafting Utilities: Prototype and test GenAI Utilities",
            "Crafting Utilities: Collaborate on a Utility that makes an impact"
        ]
        
        most_helpful = st.multiselect(
            "Which workshops were the most helpful? (Select up to 3)",
            workshop_options,
            max_selections=3
        )
        
        least_helpful = st.multiselect(
            "Which workshops were the least helpful? (Select up to 3)",
            workshop_options,
            max_selections=3
        )
        
        # Recommendations & Future Engagement
        st.markdown("### 🤝 Recommendations & Future")
        
        recommend_colleagues = st.text_area(
            "Who are two colleagues you'd recommend these workshops to? Why those colleagues, specifically?",
            height=100,
            help="If you wouldn't recommend these workshops to colleagues, leave this blank."
        )
        
        future_interest = st.multiselect(
            "(optional) Would you like to contribute to any of these workshop working groups?",
            ["GenAI for rising leaders",
             "GenAI for learning and development",
             "GenAI for sales professionals",
             "GenAI for tech / data",
             "GenAI for design / product",
             "GenAI for your sub-LOB (e.g. originations, servicing, correspondent, ...)",
             "I'm not sure. I'd like more info."],
            help="These groups will meet to craft GenAI workshops and resources for specific groups within Chase."
        )
        
        if "GenAI for your sub-LOB (e.g. originations, servicing, correspondent, ...)" in future_interest:
            sub_lob = st.text_input("GenAI for _____ (you fill in the blank):")
        
        train_trainer = st.radio(
            "(optional) Would you like to participate in a 'train-the-trainer' program to learn how to lead workshops?",
            ["Yes!", "I think so?", "No thanks", "Not sure"]
        )
        
        # Improvement Suggestions
        st.markdown("### 💡 Improvements")
        
        improvements = st.text_area(
            "What's one thing you would suggest we improve on or add to these workshops?",
            height=100
        )
        
        # Open Feedback Field (Michael's suggestion)
        additional_thoughts = st.text_area(
            "Any additional thoughts about the workshops? (e.g., if sessions felt too long/short, needed more/less guidance, etc.)",
            height=100,
            help="Share any preferences or thoughts about workshop format, pacing, or delivery"
        )
        
        # Final Open Field
        anything_else = st.text_area(
            "(optional) Anything else you'd like to share?",
            height=100
        )
        
        # Submit
        submitted = st.form_submit_button("Submit", use_container_width=True)
        
        if submitted:
            if not work_email or '@' not in work_email:
                st.error("Please provide a valid work email address")
            else:
                response_data = {
                    'work_email': work_email,
                    'key_takeaway': key_takeaway,
                    'missing_coverage': missing_coverage,
                    'expectations': expectations,
                    'built_something': built_something,
                    'something_else': something_else if "Something else" in built_something else "",
                    'what_created': what_created,
                    'most_helpful': most_helpful,
                    'least_helpful': least_helpful,
                    'recommend_colleagues': recommend_colleagues,
                    'future_interest': future_interest,
                    'sub_lob': sub_lob if "GenAI for your sub-LOB" in future_interest else "",
                    'train_trainer': train_trainer,
                    'improvements': improvements,
                    'additional_thoughts': additional_thoughts,
                    'anything_else': anything_else
                }
                
                save_response(response_data)
                st.success("✅ Thank you! Your feedback has been submitted.")
                st.balloons()

with tab2:
    st.markdown("### 📊 Survey Analytics Dashboard")
    
    # Admin password
    password = st.text_input("Enter admin password:", type="password")
    
    if password == "genai2024":
        if st.session_state.survey_data:
            df = pd.DataFrame([response['responses'] for response in st.session_state.survey_data])
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Responses", len(df))
            
            with col2:
                if 'expectations' in df.columns:
                    exceeded = df['expectations'].str.contains('WAY more|more than I expected', na=False).sum()
                    exceeded_pct = (exceeded / len(df)) * 100
                    st.metric("Exceeded Expectations", f"{exceeded_pct:.0f}%")
            
            with col3:
                if 'recommend_colleagues' in df.columns:
                    would_recommend = df['recommend_colleagues'].str.len() > 10
                    recommend_pct = (would_recommend.sum() / len(df)) * 100
                    st.metric("Would Recommend", f"{recommend_pct:.0f}%")
            
            with col4:
                if 'built_something' in df.columns:
                    built_something = df['built_something'].apply(lambda x: len(x) > 0 if isinstance(x, list) else False)
                    built_pct = (built_something.sum() / len(df)) * 100
                    st.metric("Built Something", f"{built_pct:.0f}%")
            
            # Expectations Analysis
            if 'expectations' in df.columns:
                st.subheader("Workshop Expectations")
                expectations_counts = df['expectations'].value_counts()
                fig = px.bar(x=expectations_counts.values, y=expectations_counts.index, 
                           orientation='h', title="How workshops compared to expectations")
                st.plotly_chart(fig, use_container_width=True)
            
            # Most/Least Helpful Workshops
            if 'most_helpful' in df.columns:
                st.subheader("Most Helpful Workshops")
                most_helpful_flat = []
                for workshops in df['most_helpful'].dropna():
                    if isinstance(workshops, list):
                        most_helpful_flat.extend(workshops)
                
                if most_helpful_flat:
                    helpful_counts = pd.Series(most_helpful_flat).value_counts()
                    fig = px.bar(x=helpful_counts.values, y=helpful_counts.index,
                               orientation='h', title="Most Helpful Workshops")
                    st.plotly_chart(fig, use_container_width=True)
            
            # Success Stories
            st.subheader("🌟 Success Stories")
            success_stories = df[df['what_created'].str.len() > 20]['what_created'].dropna()
            
            for i, story in enumerate(success_stories.head(5)):
                st.markdown(f"""
                <div class="success-story">
                    <strong>Success Story #{i+1}:</strong><br>
                    {story}
                </div>
                """, unsafe_allow_html=True)
            
            # Champions for Marketing
            st.subheader("🎯 Potential Success Story Champions")
            champions = df[
                (df['recommend_colleagues'].str.len() > 20) & 
                (df['what_created'].str.len() > 20)
            ][['work_email', 'what_created', 'recommend_colleagues']]
            
            if not champions.empty:
                st.write("Participants with strong success stories AND willing to recommend:")
                for _, champion in champions.iterrows():
                    st.write(f"**{champion['work_email']}**")
                    st.write(f"Built: {champion['what_created'][:100]}...")
                    st.write(f"Would recommend to: {champion['recommend_colleagues'][:100]}...")
                    st.write("---")
            
            # Raw Data Export
            st.subheader("Raw Data")
            st.dataframe(df)
            
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                f"genai_workshop_responses_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
            
        else:
            st.info("No responses yet.")
    
    elif password:
        st.error("Incorrect password")

# Footer
st.markdown("---")
st.markdown("*Your feedback helps us improve GenAI workshops and build compelling success stories for program expansion.*")
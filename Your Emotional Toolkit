import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Your Emotional Toolkit",
    page_icon="💝",
    layout="wide"
)

# Initialize session state
if 'evidence_df' not in st.session_state:
    st.session_state.evidence_df = pd.DataFrame(columns=["Date", "Category", "Evidence", "Impact"])

if 'reframing_history' not in st.session_state:
    st.session_state.reframing_history = []

# Custom CSS for cuteness
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #ff6b6b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cute-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin: 1rem 0;
    }
    .category-pill {
        background-color: #ffd93d;
        color: #6b4f4f;
        padding: 0.3rem 1rem;
        border-radius: 15px;
        font-weight: bold;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Improved categories
CATEGORIES = {
    "Growth & Maturity": "🌟",
    "Considerate Moment": "💭", 
    "Loving Action": "💖",
    "Smart Insight": "🧠",
    "Emotional Strength": "🛡️",
    "Made Me Laugh": "😂",
    "Teamwork Win": "🤝",
    "Personal Breakthrough": "🚀",
    "Sweet Gesture": "🍬",
    "Problem-Solving": "🔧",
    "Patience & Understanding": "⏳"
}

def save_data():
    """Save data to browser local storage"""
    evidence_json = st.session_state.evidence_df.to_json()
    st.experimental_set_query_params(
        evidence_data=evidence_json,
        reframing_data=json.dumps(st.session_state.reframing_history)
    )

def load_data():
    """Load data from URL parameters"""
    params = st.experimental_get_query_params()
    if 'evidence_data' in params:
        evidence_json = params['evidence_data'][0]
        st.session_state.evidence_df = pd.read_json(evidence_json)
    if 'reframing_data' in params:
        st.session_state.reframing_history = json.loads(params['reframing_data'][0])

# Load existing data
load_data()

# Main app
st.markdown('<h1 class="main-header">💝 Your Emotional Toolkit</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📂 Evidence Locker", "🔍 Reframing Engine", "📊 Growth Dashboard"])

with tab1:
    st.header("📂 Build Your Case for Awesome")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.form("evidence_form"):
            date = st.date_input("📅 Date", datetime.now())
            category = st.selectbox("🏷️ Category", options=list(CATEGORIES.keys()), 
                                  format_func=lambda x: f"{CATEGORIES[x]} {x}")
            evidence = st.text_area("📝 The Evidence", 
                                  placeholder="e.g., 'When I was stressed about work, you listened patiently and helped me break it down into manageable steps...'",
                                  height=100)
            impact = st.slider("💫 Impact Level", 1, 5, 3, 
                             help="How much did this moment matter?")
            
            submitted = st.form_submit_button("🔒 Lock It In!")
            
            if submitted and evidence:
                new_entry = {
                    "Date": date.strftime("%Y-%m-%d"),
                    "Category": category,
                    "Evidence": evidence,
                    "Impact": impact
                }
                st.session_state.evidence_df = pd.concat([
                    st.session_state.evidence_df, 
                    pd.DataFrame([new_entry])
                ], ignore_index=True)
                save_data()
                st.success("🎉 Evidence stored in your permanent record!")
                st.balloons()

    with col2:
        if not st.session_state.evidence_df.empty:
            st.subheader("Your Evidence Collection")
            
            # Filter options
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                selected_categories = st.multiselect("Filter categories:", 
                                                   options=list(CATEGORIES.keys()),
                                                   default=list(CATEGORIES.keys()))
            with col_f2:
                min_impact = st.slider("Minimum impact:", 1, 5, 1)
            
            filtered_df = st.session_state.evidence_df[
                (st.session_state.evidence_df['Category'].isin(selected_categories)) &
                (st.session_state.evidence_df['Impact'] >= min_impact)
            ]
            
            # Display entries with delete buttons
            for idx, row in filtered_df.sort_values('Date', ascending=False).iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                border-radius: 15px; padding: 1.5rem; margin: 1rem 0; color: white;'>
                        <div style='display: flex; justify-content: space-between; align-items: start;'>
                            <h4 style='margin: 0;'>{CATEGORIES[row['Category']]} {row['Category']}</h4>
                            <div style='display: flex; gap: 10px; align-items: center;'>
                                <small>Impact: {'⭐' * row['Impact']}</small>
                                <button onclick='document.getElementById("delete-{idx}").click()' 
                                        style='background: #ff6b6b; border: none; border-radius: 50%; 
                                               width: 25px; height: 25px; color: white; cursor: pointer;'>×</button>
                            </div>
                        </div>
                        <p style='margin: 0.5rem 0;'>{row['Evidence']}</p>
                        <small>📅 {row['Date']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("×", key=f"delete-{idx}"):
                        st.session_state.evidence_df = st.session_state.evidence_df.drop(idx).reset_index(drop=True)
                        save_data()
                        st.rerun()
        else:
            st.info("✨ Your evidence locker is waiting for its first entry...")

with tab2:
    st.header("🔍 Cognitive Reframing Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        negative_thought = st.text_area("What's the thought you'd like to reframe?",
                                      placeholder="e.g., 'I messed up that conversation and now she thinks I'm inconsiderate...'")
        
        if st.button("🧠 Analyze Thought"):
            if negative_thought:
                st.session_state.current_thought = negative_thought
                st.rerun()

    with col2:
        if 'current_thought' in st.session_state:
            st.subheader("Let's break this down:")
            
            st.write("**1. Identify the core belief:**")
            st.info("Underneath this thought, what's the story you're telling yourself?")
            
            st.write("**2. Look for evidence:**")
            st.success("Check your Evidence Locker tab - what does your actual track record show?")
            
            st.write("**3. Consider alternative perspectives:**")
            st.warning("How would someone who loves you see this situation?")
            
            st.write("**4. Construct a balanced view:**")
            reframed = st.text_area("Write your new, balanced perspective:",
                                  key="reframed_perspective")
            
            if st.button("💾 Save This Reframing"):
                if reframed:
                    reframing_entry = {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "original": st.session_state.current_thought,
                        "reframed": reframed
                    }
                    st.session_state.reframing_history.append(reframing_entry)
                    save_data()
                    st.success("Reframing saved to your growth history!")
                    del st.session_state.current_thought
                    st.rerun()

with tab3:
    st.header("📊 Your Growth Dashboard")
    
    if not st.session_state.evidence_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Category distribution
            category_counts = st.session_state.evidence_df['Category'].value_counts()
            fig1 = px.pie(values=category_counts.values, names=category_counts.index,
                         title="📈 Your Superpowers Distribution")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Impact over time
            st.session_state.evidence_df['Date'] = pd.to_datetime(st.session_state.evidence_df['Date'])
            monthly_impact = st.session_state.evidence_df.groupby(
                st.session_state.evidence_df['Date'].dt.to_period('M')
            )['Impact'].mean().reset_index()
            monthly_impact['Date'] = monthly_impact['Date'].dt.to_timestamp()
            
            fig2 = px.line(monthly_impact, x='Date', y='Impact',
                          title="🚀 Your Growth Journey",
                          markers=True)
            st.plotly_chart(fig2, use_container_width=True)
        
        # Recent milestones
        st.subheader("🎯 Recent Growth Milestones")
        recent_high_impact = st.session_state.evidence_df.nlargest(3, 'Impact')
        for _, milestone in recent_high_impact.iterrows():
            st.markdown(f"**{milestone['Category']}** (Impact: {'⭐' * milestone['Impact']})")
            st.caption(f"📅 {milestone['Date'].strftime('%Y-%m-%d')}: {milestone['Evidence']}")
            st.write("---")
    
    else:
        st.info("Start building your evidence collection to see your growth dashboard!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #ff6b6b;'>"
    "Built with 💖 for someone who's growing more wonderful every day"
    "</div>",
    unsafe_allow_html=True
)

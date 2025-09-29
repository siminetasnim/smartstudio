import streamlit as st
import pandas as pd
import json
from datetime import datetime
import altair as alt

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
    .evidence-entry {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        border-left: 5px solid #ffd93d;
    }
    .reframing-entry {
        background: linear-gradient(135deg, #6aeb9e 0%, #45b47c 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        border-left: 5px solid #ffd93d;
    }
    .relevant-evidence {
        background: linear-gradient(135deg, #ffb347 0%, #ffcc33 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #333;
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
    """Save data to URL parameters with proper date handling"""
    # Convert dates to strings for JSON serialization
    df_to_save = st.session_state.evidence_df.copy()
    df_to_save['Date'] = df_to_save['Date'].astype(str)
    
    evidence_json = df_to_save.to_json(orient='records')
    reframing_json = json.dumps(st.session_state.reframing_history)
    
    # Update query parameters
    st.query_params.evidence_data = evidence_json
    st.query_params.reframing_data = reframing_json

def load_data():
    """Load data from URL parameters with proper date handling"""
    params = dict(st.query_params)
    
    if 'evidence_data' in params:
        try:
            evidence_json = params['evidence_data']
            if isinstance(evidence_json, list):
                evidence_json = evidence_json[0]
            
            # Load the data and convert dates properly
            loaded_df = pd.read_json(evidence_json, orient='records')
            if not loaded_df.empty:
                loaded_df['Date'] = pd.to_datetime(loaded_df['Date']).dt.date
                st.session_state.evidence_df = loaded_df
        except Exception as e:
            st.session_state.evidence_df = pd.DataFrame(columns=["Date", "Category", "Evidence", "Impact"])
    
    if 'reframing_data' in params:
        try:
            reframing_json = params['reframing_data']
            if isinstance(reframing_json, list):
                reframing_json = reframing_json[0]
            st.session_state.reframing_history = json.loads(reframing_json)
        except:
            st.session_state.reframing_history = []

def get_relevant_evidence(negative_thought):
    """Find evidence from the locker that's relevant to the current negative thought"""
    if st.session_state.evidence_df.empty:
        return []
    
    # Simple keyword matching for relevance
    negative_lower = negative_thought.lower()
    relevant_categories = []
    
    # Map negative thought patterns to relevant categories
    if any(word in negative_lower for word in ['stupid', 'dumb', 'not smart', 'ignorant']):
        relevant_categories.extend(['Smart Insight', 'Problem-Solving'])
    if any(word in negative_lower for word in ['inconsiderate', 'selfish', 'thoughtless']):
        relevant_categories.extend(['Considerate Moment', 'Loving Action', 'Sweet Gesture'])
    if any(word in negative_lower for word in ['weak', 'can\'t handle', 'overwhelmed']):
        relevant_categories.extend(['Emotional Strength', 'Growth & Maturity'])
    if any(word in negative_lower for word in ['failure', 'mess up', 'mistake']):
        relevant_categories.extend(['Growth & Maturity', 'Personal Breakthrough', 'Problem-Solving'])
    if any(word in negative_lower for word in ['alone', 'misunderstood', 'nobody cares']):
        relevant_categories.extend(['Loving Action', 'Teamwork Win', 'Considerate Moment'])
    
    # Get unique categories and return relevant evidence
    relevant_categories = list(set(relevant_categories))
    if relevant_categories:
        relevant_evidence = st.session_state.evidence_df[
            st.session_state.evidence_df['Category'].isin(relevant_categories)
        ].nlargest(3, 'Impact')
        return relevant_evidence.to_dict('records')
    
    # If no specific matches, return highest impact evidence
    return st.session_state.evidence_df.nlargest(2, 'Impact').to_dict('records')

# Load existing data
load_data()

# Main app
st.markdown('<h1 class="main-header">💝 Your Emotional Toolkit</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📂 Evidence Locker", "🔍 Reframing Engine", "📊 Growth Dashboard"])

with tab1:
    st.header("📂 Build Your Case for Awesome")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.form("evidence_form", clear_on_submit=True):
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
                    "Date": date,
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
            st.subheader(f"Your Evidence Collection ({len(st.session_state.evidence_df)} entries)")
            
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
                    col_d1, col_d2 = st.columns([4, 1])
                    with col_d1:
                        st.markdown(f"""
                        <div class="evidence-entry">
                            <div style='display: flex; justify-content: space-between; align-items: start;'>
                                <h4 style='margin: 0;'>{CATEGORIES[row['Category']]} {row['Category']}</h4>
                                <small>Impact: {'⭐' * row['Impact']}</small>
                            </div>
                            <p style='margin: 0.5rem 0; font-size: 14px;'>{row['Evidence']}</p>
                            <small>📅 {row['Date'].strftime('%Y-%m-%d')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_d2:
                        if st.button("🗑️", key=f"delete-{idx}"):
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
                                      placeholder="e.g., 'I messed up that conversation and now she thinks I'm inconsiderate...'",
                                      height=150,
                                      key="negative_thought_input")
        
        if st.button("🧠 Analyze Thought"):
            if negative_thought:
                st.session_state.current_thought = negative_thought
                st.rerun()

    with col2:
        if 'current_thought' in st.session_state:
            st.subheader("Let's break this down together:")
            
            st.write("**1. 🎯 Identify the core belief:**")
            st.info("What's the underlying story you're telling yourself about this situation?")
            
            st.write("**2. 📊 Relevant Evidence from Your Locker:**")
            relevant_evidence = get_relevant_evidence(st.session_state.current_thought)
            
            if relevant_evidence:
                st.success("Here's evidence that contradicts that negative story:")
                for evidence in relevant_evidence:
                    st.markdown(f"""
                    <div class="relevant-evidence">
                        <strong>{CATEGORIES[evidence['Category']]} {evidence['Category']}</strong>
                        <p style='margin: 0.3rem 0; font-size: 14px;'>{evidence['Evidence']}</p>
                        <small>Impact: {'⭐' * evidence['Impact']} • Date: {evidence['Date'].strftime('%Y-%m-%d')}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No relevant evidence yet. Start building your evidence locker to see your amazing qualities!")
            
            st.write("**3. 🔄 Consider alternative perspectives:**")
            st.warning("How would someone who loves you unconditionally see this situation?")
            
            st.write("**4. 💡 Construct a balanced view:**")
            reframed = st.text_area("Write your new, more balanced perspective:",
                                  placeholder="e.g., 'I'm learning and growing. One conversation doesn't define my entire character...'",
                                  height=100,
                                  key="reframed_perspective")
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("💾 Save This Reframing"):
                    if reframed:
                        reframing_entry = {
                            "date": datetime.now().strftime('%Y-%m-%d %H:%M'),
                            "original": st.session_state.current_thought,
                            "reframed": reframed
                        }
                        st.session_state.reframing_history.append(reframing_entry)
                        save_data()
                        st.success("Reframing saved to your growth history!")
                        del st.session_state.current_thought
                        st.rerun()
            with col_b2:
                if st.button("🔄 Start Over"):
                    if 'current_thought' in st.session_state:
                        del st.session_state.current_thought
                    st.rerun()
        
        # Show reframing history
        if st.session_state.reframing_history:
            st.subheader("📖 Your Reframing History")
            for i, entry in enumerate(reversed(st.session_state.reframing_history[-5:])):  # Show last 5
                with st.expander(f"Reframing from {entry['date']}"):
                    st.write("**Original thought:**")
                    st.info(entry['original'])
                    st.write("**Balanced perspective:**")
                    st.success(entry['reframed'])

with tab3:
    st.header("📊 Your Growth Dashboard")
    
    if not st.session_state.evidence_df.empty:
        # Convert Date to datetime for proper sorting
        st.session_state.evidence_df['Date'] = pd.to_datetime(st.session_state.evidence_df['Date'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Your Superpowers Distribution")
            
            # Simple bar chart with Altair
            category_counts = st.session_state.evidence_df['Category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            
            chart = alt.Chart(category_counts).mark_bar().encode(
                x='Count:Q',
                y=alt.Y('Category:N', sort='-x'),
                color=alt.value('#ff6b6b')
            ).properties(height=300)
            
            st.altair_chart(chart, use_container_width=True)
        
        with col2:
            st.subheader("🚀 Impact Over Time")
            
            # Monthly impact average
            monthly_data = st.session_state.evidence_df.copy()
            monthly_data['Month'] = monthly_data['Date'].dt.to_period('M').astype(str)
            monthly_avg = monthly_data.groupby('Month')['Impact'].mean().reset_index()
            
            if len(monthly_avg) > 1:
                line_chart = alt.Chart(monthly_avg).mark_line(point=True).encode(
                    x='Month:N',
                    y='Impact:Q',
                    color=alt.value('#667eea')
                ).properties(height=300)
                st.altair_chart(line_chart, use_container_width=True)
            else:
                st.info("Add more entries to see your growth trend!")
        
        # Statistics
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.metric("Total Entries", len(st.session_state.evidence_df))
        with col_s2:
            avg_impact = st.session_state.evidence_df['Impact'].mean()
            st.metric("Average Impact", f"{avg_impact:.1f} ⭐")
        with col_s3:
            top_category = st.session_state.evidence_df['Category'].mode()[0] if not st.session_state.evidence_df.empty else "N/A"
            st.metric("Top Strength", top_category)
        with col_s4:
            days_span = (st.session_state.evidence_df['Date'].max() - st.session_state.evidence_df['Date'].min()).days if len(st.session_state.evidence_df) > 1 else 0
            st.metric("Journey Length", f"{days_span} days")
        
        # Recent milestones
        st.subheader("🎯 Recent Growth Milestones")
        recent_high_impact = st.session_state.evidence_df.nlargest(3, 'Impact')
        for _, milestone in recent_high_impact.iterrows():
            with st.expander(f"{milestone['Category']} (Impact: {'⭐' * milestone['Impact']}) - {milestone['Date'].strftime('%Y-%m-%d')}"):
                st.write(milestone['Evidence'])
    
    else:
        st.info("Start building your evidence collection to see your amazing growth dashboard!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #ff6b6b; font-style: italic;'>"
    "Built with 💖 for someone who's growing more wonderful every day · "
    "Your data is saved in this URL - bookmark it to keep your progress!"
    "</div>",
    unsafe_allow_html=True
)

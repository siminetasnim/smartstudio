import streamlit as st
import pandas as pd
import json
from datetime import datetime
import altair as alt
import urllib.parse
import sqlite3
import os
from contextlib import contextmanager

# Page config
st.set_page_config(
    page_title="Your Emotional Toolkit",
    page_icon="💝",
    layout="wide"
)

# Database setup
DB_PATH = "emotional_toolkit.db"

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Initialize the database tables"""
    with get_db_connection() as conn:
        # Evidence table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_slug TEXT NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                evidence TEXT NOT NULL,
                impact INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Reframing history table
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reframing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_slug TEXT NOT NULL,
                original_thought TEXT NOT NULL,
                reframed_thought TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        conn.execute('CREATE INDEX IF NOT EXISTS idx_evidence_user ON evidence(user_slug)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_reframing_user ON reframing_history(user_slug)')
        conn.commit()

# Initialize database on app start
init_database()

# Initialize session state
if 'evidence_df' not in st.session_state:
    st.session_state.evidence_df = pd.DataFrame(columns=["Date", "Category", "Evidence", "Impact"])

if 'reframing_history' not in st.session_state:
    st.session_state.reframing_history = []

if 'editing_reframing' not in st.session_state:
    st.session_state.editing_reframing = None

if 'editing_evidence' not in st.session_state:
    st.session_state.editing_evidence = None

if 'user_slug' not in st.session_state:
    st.session_state.user_slug = 'default'

if 'data_initialized' not in st.session_state:
    st.session_state.data_initialized = False

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

# Better keyword mapping for relevant evidence
CATEGORY_KEYWORDS = {
    "Loving Action": ['love', 'loving', 'affection', 'care', 'caring', 'romantic', 'sweet', 'kind', 'kindness'],
    "Considerate Moment": ['considerate', 'thoughtful', 'thinking of you', 'noticed', 'remembered', 'attention'],
    "Growth & Maturity": ['grow', 'growth', 'mature', 'maturity', 'learn', 'learning', 'improve', 'better', 'progress'],
    "Smart Insight": ['smart', 'intelligent', 'clever', 'insight', 'wisdom', 'knowledge', 'brilliant'],
    "Emotional Strength": ['strong', 'strength', 'resilient', 'brave', 'courage', 'emotional', 'support'],
    "Problem-Solving": ['solve', 'solution', 'fix', 'resolve', 'problem', 'issue', 'challenge'],
    "Patience & Understanding": ['patient', 'patience', 'understand', 'understanding', 'listen', 'calm']
}

# Database functions
def save_evidence(user_slug, date, category, evidence, impact):
    """Save evidence to database"""
    with get_db_connection() as conn:
        conn.execute(
            'INSERT INTO evidence (user_slug, date, category, evidence, impact) VALUES (?, ?, ?, ?, ?)',
            (user_slug, date.isoformat(), category, evidence, impact)
        )
        conn.commit()

def get_user_evidence(user_slug):
    """Get all evidence for a user"""
    with get_db_connection() as conn:
        cursor = conn.execute(
            'SELECT date, category, evidence, impact FROM evidence WHERE user_slug = ? ORDER BY date DESC',
            (user_slug,)
        )
        rows = cursor.fetchall()
        
        if not rows:
            return pd.DataFrame(columns=["Date", "Category", "Evidence", "Impact"])
        
        data = []
        for row in rows:
            data.append({
                "Date": datetime.fromisoformat(row['date']).date(),
                "Category": row['category'],
                "Evidence": row['evidence'],
                "Impact": row['impact']
            })
        
        return pd.DataFrame(data)

def delete_evidence(user_slug, index):
    """Delete evidence entry by index"""
    with get_db_connection() as conn:
        # Get all evidence for user ordered by date to find the correct ID
        cursor = conn.execute(
            'SELECT id FROM evidence WHERE user_slug = ? ORDER BY date DESC',
            (user_slug,)
        )
        rows = cursor.fetchall()
        
        if 0 <= index < len(rows):
            evidence_id = rows[index]['id']
            conn.execute('DELETE FROM evidence WHERE id = ?', (evidence_id,))
            conn.commit()
            return True
        return False

def update_evidence(user_slug, index, date, category, evidence, impact):
    """Update evidence entry"""
    with get_db_connection() as conn:
        # Get all evidence for user ordered by date to find the correct ID
        cursor = conn.execute(
            'SELECT id FROM evidence WHERE user_slug = ? ORDER BY date DESC',
            (user_slug,)
        )
        rows = cursor.fetchall()
        
        if 0 <= index < len(rows):
            evidence_id = rows[index]['id']
            conn.execute(
                'UPDATE evidence SET date = ?, category = ?, evidence = ?, impact = ? WHERE id = ?',
                (date.isoformat(), category, evidence, impact, evidence_id)
            )
            conn.commit()
            return True
        return False

def save_reframing(user_slug, original_thought, reframed_thought):
    """Save reframing to database"""
    with get_db_connection() as conn:
        conn.execute(
            'INSERT INTO reframing_history (user_slug, original_thought, reframed_thought) VALUES (?, ?, ?)',
            (user_slug, original_thought, reframed_thought)
        )
        conn.commit()

def get_user_reframing_history(user_slug):
    """Get all reframing history for a user"""
    with get_db_connection() as conn:
        cursor = conn.execute(
            'SELECT original_thought, reframed_thought, created_at FROM reframing_history WHERE user_slug = ? ORDER BY created_at DESC',
            (user_slug,)
        )
        rows = cursor.fetchall()
        
        history = []
        for row in rows:
            history.append({
                "original": row['original_thought'],
                "reframed": row['reframed_thought'],
                "date": row['created_at']
            })
        
        return history

def delete_reframing(user_slug, index):
    """Delete reframing entry by index"""
    with get_db_connection() as conn:
        # Get all reframing for user ordered by date to find the correct ID
        cursor = conn.execute(
            'SELECT id FROM reframing_history WHERE user_slug = ? ORDER BY created_at DESC',
            (user_slug,)
        )
        rows = cursor.fetchall()
        
        if 0 <= index < len(rows):
            reframing_id = rows[index]['id']
            conn.execute('DELETE FROM reframing_history WHERE id = ?', (reframing_id,))
            conn.commit()
            return True
        return False

def update_reframing(user_slug, index, original_thought, reframed_thought):
    """Update reframing entry"""
    with get_db_connection() as conn:
        # Get all reframing for user ordered by date to find the correct ID
        cursor = conn.execute(
            'SELECT id FROM reframing_history WHERE user_slug = ? ORDER BY created_at DESC',
            (user_slug,)
        )
        rows = cursor.fetchall()
        
        if 0 <= index < len(rows):
            reframing_id = rows[index]['id']
            conn.execute(
                'UPDATE reframing_history SET original_thought = ?, reframed_thought = ? WHERE id = ?',
                (original_thought, reframed_thought, reframing_id)
            )
            conn.commit()
            return True
        return False

def load_user_data(user_slug):
    """Load all data for a user from database"""
    st.session_state.evidence_df = get_user_evidence(user_slug)
    st.session_state.reframing_history = get_user_reframing_history(user_slug)

def get_relevant_evidence(negative_thought):
    """Find evidence from the locker that's relevant to the current negative thought"""
    if st.session_state.evidence_df.empty:
        return []
    
    negative_lower = negative_thought.lower()
    relevant_categories = set()
    
    # Check each category's keywords against the negative thought
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in negative_lower:
                relevant_categories.add(category)
                break
    
    # If we found relevant categories, get evidence from those categories
    if relevant_categories:
        relevant_evidence = st.session_state.evidence_df[
            st.session_state.evidence_df['Category'].isin(relevant_categories)
        ].nlargest(3, 'Impact')
        return relevant_evidence.to_dict('records')
    
    # If no specific matches, return highest impact evidence
    return st.session_state.evidence_df.nlargest(2, 'Impact').to_dict('records')

def edit_reframing_form(index):
    """Form to edit a reframing entry"""
    entry = st.session_state.reframing_history[index]
    
    with st.form(f"edit_reframing_{index}"):
        st.write("**Edit your reframing:**")
        edited_original = st.text_area("Original thought:", value=entry['original'], key=f"edit_orig_{index}")
        edited_reframed = st.text_area("Balanced perspective:", value=entry['reframed'], key=f"edit_ref_{index}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Save Changes"):
                if update_reframing(st.session_state.user_slug, index, edited_original, edited_reframed):
                    load_user_data(st.session_state.user_slug)  # Reload data
                    st.session_state.editing_reframing = None
                    st.rerun()
        with col2:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.editing_reframing = None
                st.rerun()

def edit_evidence_form(index):
    """Form to edit an evidence entry"""
    row = st.session_state.evidence_df.iloc[index]
    
    with st.form(f"edit_evidence_{index}"):
        st.write("**Edit your evidence:**")
        edited_date = st.date_input("Date", value=datetime.strptime(str(row['Date']), '%Y-%m-%d'), key=f"edit_date_{index}")
        edited_category = st.selectbox("Category", options=list(CATEGORIES.keys()), 
                                     index=list(CATEGORIES.keys()).index(row['Category']), 
                                     key=f"edit_cat_{index}")
        edited_evidence = st.text_area("Evidence", value=row['Evidence'], key=f"edit_ev_{index}")
        edited_impact = st.slider("Impact", 1, 5, row['Impact'], key=f"edit_imp_{index}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("💾 Save Changes"):
                if update_evidence(st.session_state.user_slug, index, edited_date, edited_category, edited_evidence, edited_impact):
                    load_user_data(st.session_state.user_slug)  # Reload data
                    st.session_state.editing_evidence = None
                    st.rerun()
        with col2:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.editing_evidence = None
                st.rerun()

def user_setup():
    """Let users set their custom URL slug"""
    params = dict(st.query_params)
    
    if 'user' not in params:
        st.markdown('<h1 class="main-header">💝 Your Emotional Toolkit</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("https://cdn.pixabay.com/photo/2017/09/23/16/33/pixel-heart-2779422_1280.png", width=150)
        
        with col2:
            st.subheader("🎯 Create Your Personal Space")
            st.write("Welcome! Create your own permanent URL to save all your progress.")
            
            user_slug = st.text_input("Choose your personal URL name:", 
                                    placeholder="",
                                    help="This will create your permanent URL like: yourapp.streamlit.app/?user=yourname")
            
            if st.button("🚀 Create My Space", type="primary"):
                if user_slug and user_slug.strip():
                    # Use the exact input without modification
                    user_slug_clean = user_slug.strip()
                    st.session_state.user_slug = user_slug_clean
                    # URL encode the user slug for the URL
                    st.query_params.user = urllib.parse.quote(user_slug_clean)
                    st.rerun()
                else:
                    st.error("Please enter a name for your personal URL")
        
        st.markdown("---")
        st.info("💡 **Tip:** Choose a name you'll remember! This will be your permanent space.")
        return False
    return True

# Main app flow
if user_setup():
    # Get the current user slug from URL to ensure it's always correct
    params = dict(st.query_params)
    if 'user' in params:
        current_user_slug = params['user']
        if isinstance(current_user_slug, list):
            current_user_slug = current_user_slug[0]
        # URL decode to get the original text
        current_user_slug = urllib.parse.unquote(current_user_slug)
    else:
        current_user_slug = 'default'
    
    # Update session state with the correct user slug
    st.session_state.user_slug = current_user_slug

    # Load data for this user from database
    if not st.session_state.data_initialized:
        load_user_data(st.session_state.user_slug)
        st.session_state.data_initialized = True

    # Show user info in sidebar
    with st.sidebar:
        st.success(f"✨ Welcome, {st.session_state.user_slug}!")
        st.info(f"**Your permanent URL:**")
        # Show the actual URL-encoded version for the link
        encoded_slug = urllib.parse.quote(st.session_state.user_slug)
        st.code(f"?user={encoded_slug}")
        
        # Show data statistics
        if not st.session_state.evidence_df.empty:
            st.metric("Evidence Entries", len(st.session_state.evidence_df))
        if st.session_state.reframing_history:
            st.metric("Reframing Exercises", len(st.session_state.reframing_history))
        
        if st.button("🔄 Switch User"):
            # Clear current user data from URL
            del st.query_params.user
            st.session_state.data_initialized = False
            # Clear the user slug from session state
            if 'user_slug' in st.session_state:
                del st.session_state.user_slug
            st.rerun()
        
        st.markdown("---")
        st.caption("💝 Your data is safely stored in a secure database!")

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
                    save_evidence(st.session_state.user_slug, date, category, evidence, impact)
                    load_user_data(st.session_state.user_slug)  # Reload updated data
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
                
                # Display entries with edit/delete buttons
                for idx, row in filtered_df.sort_values('Date', ascending=False).iterrows():
                    with st.container():
                        if st.session_state.editing_evidence == idx:
                            edit_evidence_form(idx)
                        else:
                            col_d1, col_d2, col_d3 = st.columns([4, 1, 1])
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
                                if st.button("✏️", key=f"edit_{idx}"):
                                    st.session_state.editing_evidence = idx
                                    st.rerun()
                            with col_d3:
                                if st.button("🗑️", key=f"delete_{idx}"):
                                    if delete_evidence(st.session_state.user_slug, idx):
                                        load_user_data(st.session_state.user_slug)  # Reload data
                                        st.rerun()
            else:
                st.info("✨ Your evidence locker is waiting for its first entry...")

    with tab2:
        st.header("🔍 Cognitive Reframing Engine")
        
        col1, col2 = st.columns(2)
        
        with col1:
            negative_thought = st.text_area("What's the thought you'd like to reframe?",
                                          placeholder="e.g., 'I feel like I'm not loving enough in our relationship...'",
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
                            save_reframing(st.session_state.user_slug, st.session_state.current_thought, reframed)
                            load_user_data(st.session_state.user_slug)  # Reload updated data
                            st.success("Reframing saved to your growth history!")
                            del st.session_state.current_thought
                            st.rerun()
                with col_b2:
                    if st.button("🔄 Start Over"):
                        if 'current_thought' in st.session_state:
                            del st.session_state.current_thought
                        st.rerun()
            
            # Show reframing history with edit/delete
            if st.session_state.reframing_history:
                st.subheader("📖 Your Reframing History")
                for i, entry in enumerate(reversed(st.session_state.reframing_history)):
                    idx = len(st.session_state.reframing_history) - 1 - i  # Get original index
                    
                    if st.session_state.editing_reframing == idx:
                        edit_reframing_form(idx)
                    else:
                        with st.expander(f"Reframing from {entry['date']}", expanded=i < 3):  # First 3 expanded
                            st.write("**Original thought:**")
                            st.info(entry['original'])
                            st.write("**Balanced perspective:**")
                            st.success(entry['reframed'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("✏️ Edit", key=f"edit_ref_{idx}"):
                                    st.session_state.editing_reframing = idx
                                    st.rerun()
                            with col2:
                                if st.button("🗑️ Delete", key=f"del_ref_{idx}"):
                                    if delete_reframing(st.session_state.user_slug, idx):
                                        load_user_data(st.session_state.user_slug)  # Reload data
                                        st.rerun()

    with tab3:
        st.header("📊 Your Growth Dashboard")
        
        if not st.session_state.evidence_df.empty:
            # Ensure Date is datetime for proper processing
            evidence_df_copy = st.session_state.evidence_df.copy()
            evidence_df_copy['Date'] = pd.to_datetime(evidence_df_copy['Date'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Your Superpowers Distribution")
                
                # Simple bar chart with Altair
                category_counts = evidence_df_copy['Category'].value_counts().reset_index()
                category_counts.columns = ['Category', 'Count']
                
                chart = alt.Chart(category_counts).mark_bar().encode(
                    x='Count:Q',
                    y=alt.Y('Category:N', sort='-x'),
                    color=alt.value('#ff6b6b')
                ).properties(height=300)
                
                st.altair_chart(chart, use_container_width=True)
            
            with col2:
                st.subheader("🚀 Impact Over Time")
                
                # FIXED: Proper monthly grouping and impact calculation
                monthly_data = evidence_df_copy.copy()
                
                # Create month-year column for grouping
                monthly_data['Month_Year'] = monthly_data['Date'].dt.to_period('M').astype(str)
                
                # Calculate monthly statistics
                monthly_stats = monthly_data.groupby('Month_Year').agg({
                    'Impact': 'mean',
                    'Date': 'count'
                }).reset_index()
                monthly_stats.columns = ['Month', 'Average_Impact', 'Entry_Count']
                
                # Only show chart if we have data across multiple time periods
                if len(monthly_stats) > 1:
                    # Create the line chart
                    line_chart = alt.Chart(monthly_stats).mark_line(point=True).encode(
                        x=alt.X('Month:N', title='Month', axis=alt.Axis(labelAngle=-45)),
                        y=alt.Y('Average_Impact:Q', title='Average Impact', scale=alt.Scale(domain=[1, 5])),
                        tooltip=['Month', 'Average_Impact', 'Entry_Count']
                    ).properties(
                        height=300,
                        title='Your Emotional Growth Journey'
                    )
                    
                    # Add points to the line
                    points = alt.Chart(monthly_stats).mark_circle(
                        size=100,
                        opacity=0.7
                    ).encode(
                        x='Month:N',
                        y='Average_Impact:Q',
                        size=alt.Size('Entry_Count:Q', legend=None, scale=alt.Scale(range=[50, 300])),
                        color=alt.value('#667eea'),
                        tooltip=['Month', 'Average_Impact', 'Entry_Count']
                    )
                    
                    combined_chart = line_chart + points
                    st.altair_chart(combined_chart, use_container_width=True)
                    
                    # Show monthly breakdown
                    with st.expander("📅 Monthly Breakdown"):
                        for _, month_data in monthly_stats.iterrows():
                            st.write(f"**{month_data['Month']}:** Average Impact {month_data['Average_Impact']:.1f} ⭐ ({month_data['Entry_Count']} entries)")
                else:
                    st.info("📈 Add entries from different months to see your growth trend over time!")
                    # Show current month's average
                    current_avg = monthly_stats.iloc[0]['Average_Impact']
                    st.metric("Current Month Average", f"{current_avg:.1f} ⭐")
            
            # Statistics
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                st.metric("Total Entries", len(evidence_df_copy))
            with col_s2:
                avg_impact = evidence_df_copy['Impact'].mean()
                st.metric("Average Impact", f"{avg_impact:.1f} ⭐")
            with col_s3:
                top_category = evidence_df_copy['Category'].mode()[0] if not evidence_df_copy.empty else "N/A"
                st.metric("Top Strength", top_category)
            with col_s4:
                days_span = (evidence_df_copy['Date'].max() - evidence_df_copy['Date'].min()).days + 1 if len(evidence_df_copy) > 1 else 1
                st.metric("Journey Length", f"{days_span} days")
            
            # Recent milestones
            st.subheader("🎯 Recent Growth Milestones")
            recent_high_impact = evidence_df_copy.nlargest(3, 'Impact')
            for _, milestone in recent_high_impact.iterrows():
                with st.expander(f"{milestone['Category']} (Impact: {'⭐' * milestone['Impact']}) - {milestone['Date'].strftime('%Y-%m-%d')}"):
                    st.write(milestone['Evidence'])
        
        else:
            st.info("Start building your evidence collection to see your amazing growth dashboard!")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #ff6b6b; font-style: italic;'>"
        f"Built with 💖 for {st.session_state.user_slug}'s growth journey · "
        "Your data is safely stored in a secure database!"
        "</div>",
        unsafe_allow_html=True
    )

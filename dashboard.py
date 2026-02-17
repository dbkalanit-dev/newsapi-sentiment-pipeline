import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NLP Auditor Dashboard", layout="wide")

# --- 1. DATA & STATE MANAGEMENT ---
if 'audit_data' not in st.session_state:
    try:
        # Load data with safety for messy lines
        df = pd.read_csv("news_sentiment_report.csv", on_bad_lines='skip') 

        # De-duplicate: Keep only the LATEST version of an article by title
        df = df.sort_values('date_added', ascending=False).drop_duplicates('title')
        
        if 'status' not in df.columns:
            df['status'] = "🤖 Auto"
            
        st.session_state.audit_data = df
    except FileNotFoundError:
        st.error("Please run live_ingest.py first!")
        st.stop()

# --- 2. DEFINE FILTERED DATA FIRST (Fixes NameError) ---
# We define this BEFORE the sidebar logic so the Auditor Toolbox can see it
st.sidebar.header("🎯 Global Filters")
sentiment_options = st.session_state.audit_data['sentiment'].unique().tolist()
selected_sentiments = st.sidebar.multiselect("View Sentiments:", sentiment_options, default=sentiment_options)

# This variable is now globally defined for the rest of the script
filtered_display = st.session_state.audit_data[st.session_state.audit_data['sentiment'].isin(selected_sentiments)]

# --- 3. THE "CHALLENGE" LOGIC (SIDEBAR EDITOR) ---
st.sidebar.markdown("---")
st.sidebar.header("🛠️ Auditor Toolbox")

# Access selection from the dataframe defined later in step 5
selected_rows = st.session_state.get("table_selection", {"selection": {"rows": []}})
row_indices = selected_rows["selection"]["rows"]

if row_indices:
    # Now filtered_display is guaranteed to exist here
    selected_article = filtered_display.iloc[row_indices[0]]
    st.sidebar.info(f"**Reviewing:**\n{selected_article['title']}")
    
    new_score = st.sidebar.slider(
        "Adjust Sentiment Score:",
        -1.0, 1.0, float(selected_article['score']), 0.01,
        help="Legend: 1.0 (Positive), 0.0 (Neutral), -1.0 (Negative)"
    )
    
    if st.sidebar.button("Confirm Override"):
        new_label = "Neutral"
        if new_score >= 0.05: new_label = "Positive"
        elif new_score <= -0.05: new_label = "Negative"
        
        # Update session state using the unique index
        original_idx = selected_article.name 
        st.session_state.audit_data.at[original_idx, 'score'] = new_score
        st.session_state.audit_data.at[original_idx, 'sentiment'] = new_label
        st.session_state.audit_data.at[original_idx, 'status'] = "👤 Manual"
        st.rerun() 
else:
    st.sidebar.write("💡 *Click a row in the table below to challenge its sentiment.*")

if st.sidebar.button("💾 Permanent Save to CSV"):
    st.session_state.audit_data.to_csv("news_sentiment_report.csv", index=False)
    st.sidebar.success("CSV Saved!")

# --- 4. VISUALS ---
st.title("📊 News Sentiment Auditor")
color_map = {'Positive': '#2ecc71', 'Neutral': '#95a5a6', 'Negative': '#e74c3c'}
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(px.bar(filtered_display['sentiment'].value_counts().reset_index(), 
                           x='sentiment', y='count', color='sentiment', 
                           color_discrete_map=color_map, title="Filtered Volume"), use_container_width=True)
with col2:
    st.plotly_chart(px.pie(filtered_display, names='sentiment', hole=0.4, 
                           color='sentiment', color_discrete_map=color_map, 
                           title="Filtered Share of Voice"), use_container_width=True)

# --- 5. THE AUDIT TABLE ---
st.subheader("Article Audit Log")

display_columns = ["status", "sentiment", "score", "title", "description", "link"]

st.dataframe(
    filtered_display[display_columns],
    column_config={
        "status": st.column_config.TextColumn("Source", width=50),
        "sentiment": st.column_config.TextColumn("Label", width=75),
        "score": st.column_config.NumberColumn("Score", format="%.2f", width=50),
        "title": st.column_config.TextColumn("Headline", width="large"),
        "description": st.column_config.TextColumn("Context", width="large"),
        "link": st.column_config.LinkColumn("Link", width=60),
    },
    hide_index=True,
    width="stretch",
    height=500,
    on_select="rerun",
    selection_mode="single-row",
    key="table_selection"
)
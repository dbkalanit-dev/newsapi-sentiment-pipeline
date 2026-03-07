import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NLP Auditor Dashboard", layout="wide")

# --- 1. DATA & STATE MANAGEMENT ---
if 'audit_data' not in st.session_state:
    try:
        # Load data with safety for messy lines
        df = pd.read_csv("news_sentiment_report.csv", on_bad_lines='skip') 

        # Convert strings to datetime objects for accurate plotting
        df['date_added'] = pd.to_datetime(df['date_added'])
        df['date_published'] = pd.to_datetime(df['date_published'])

        # De-duplicate: Keep only the LATEST version of an article by title
        df = df.sort_values('date_added', ascending=False).drop_duplicates('title')
        
        if 'status' not in df.columns:
            df['status'] = "🤖 Auto"
            
        st.session_state.audit_data = df
    except FileNotFoundError:
        st.error("Please run live_ingest.py first!")
        st.stop()

# --- 2. DEFINE FILTERED DATA FIRST ---
st.sidebar.header("🎯 Global Filters")
sentiment_options = st.session_state.audit_data['sentiment'].unique().tolist()
selected_sentiments = st.sidebar.multiselect("View Sentiments:", sentiment_options, default=sentiment_options)

# Global filtered variable for the rest of the script
filtered_display = st.session_state.audit_data[st.session_state.audit_data['sentiment'].isin(selected_sentiments)]

# --- 3. THE "CHALLENGE" LOGIC (SIDEBAR EDITOR) ---
st.sidebar.markdown("---")
st.sidebar.header("🛠️ Auditor Toolbox")

selected_rows = st.session_state.get("table_selection", {"selection": {"rows": []}})
row_indices = selected_rows["selection"]["rows"]

if row_indices:
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

# --- 5. PUBLISHER ANALYSIS ---
st.subheader("📰 Publisher Sentiment Breakdown")
pub_df = filtered_display.groupby('publisher')['score'].mean().sort_values().reset_index()

fig_pub = px.bar(
    pub_df, x='score', y='publisher', orientation='h',
    title="Average Sentiment Score by Source",
    color='score', color_continuous_scale='RdYlGn', range_color=[-1, 1]
)
st.plotly_chart(fig_pub, use_container_width=True)

# --- 6. SENTIMENT DRIFT (WITH EMPTY STATE UX) ---
st.subheader("📈 Sentiment Drift Over Time")

# Group by day and calculate the mean score
trend_df = filtered_display.resample('D', on='date_added')['score'].mean().reset_index()

# Empty State Logic: Provides context if the user has only run the ingest once
if len(trend_df) < 2:
    st.info("💡 **PM Note:** Trend analysis requires multiple days of data. Run 'live_ingest.py' daily to see sentiment drift.")

fig_trend = px.line(
    trend_df, x='date_added', y='score',
    title="Mean Sentiment Score (Daily Ingestion)",
    labels={'score': 'Avg Sentiment', 'date_added': 'Date'},
    markers=True
)
fig_trend.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral Threshold")
st.plotly_chart(fig_trend, use_container_width=True)

# --- 7. THE AUDIT TABLE ---
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
    hide_index=True, width="stretch", height=500,
    on_select="rerun", selection_mode="single-row", key="table_selection"
)
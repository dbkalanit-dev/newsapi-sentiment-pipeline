import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NLP Auditor Dashboard", layout="wide")

# --- 1. DATA & STATE MANAGEMENT ---
def load_data(file_path):
    df = pd.read_csv(file_path, on_bad_lines='skip') 
    df['date_added'] = pd.to_datetime(df['date_added'])
    df['date_published'] = pd.to_datetime(df['date_published'], format='ISO8601', errors='coerce')
    
    # Fill missing dates to prevent filter crashes
    df['date_published'] = df['date_published'].fillna(df['date_added']) 
    
    # Sort and Deduplicate
    df = df.sort_values(by='date_published', ascending=True)
    df = df.drop_duplicates('title')
    
    # Reset Index for clean 1-based "Item Numbers"
    df = df.reset_index(drop=True)
    df.index = df.index + 1  

    if 'status' not in df.columns:
        df['status'] = "🤖 Auto"
    
    return df

# Main logic to actually call the function
if 'audit_data' not in st.session_state:
    try:
        st.session_state.audit_data = load_data("news_sentiment_report.csv")
    except FileNotFoundError:
        try:
            st.session_state.audit_data = load_data("sample_data.csv")
            st.warning("⚠️ Using **Sample Data**. Run 'live_ingest.py' to collect your own live news.")
        except FileNotFoundError:
            st.error("No data found. Please ensure 'sample_data.csv' exists or run 'live_ingest.py'!")
            st.stop()

# --- 2. GLOBAL FILTERS ---
st.sidebar.header("🎯 Global Filters")

# 1. Sentiment Filter
sentiment_options = st.session_state.audit_data['sentiment'].unique().tolist()
selected_sentiments = st.sidebar.multiselect("View Sentiments:", sentiment_options, default=sentiment_options)

# 2. Search Filter
search_term = st.sidebar.text_input("🔍 Search Dashboard:", "")

# 3. Date Range Filter
# We default to showing everything (using min/max of the data) or None to force selection
min_date = st.session_state.audit_data['date_published'].min().date()
max_date = st.session_state.audit_data['date_published'].max().date()

date_range = st.sidebar.date_input(
    "📅 Date Published:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# --- APPLY FILTERS ---
# Create a fresh copy
filtered_display = st.session_state.audit_data.copy()

# Filter by Sentiment
filtered_display = filtered_display[filtered_display['sentiment'].isin(selected_sentiments)]

# Filter by Search
if search_term:
    search_mask = (
        filtered_display['title'].astype(str).str.contains(search_term, case=False, na='') |
        filtered_display['description'].astype(str).str.contains(search_term, case=False, na='') |
        filtered_display['publisher'].astype(str).str.contains(search_term, case=False, na='')
    )
    filtered_display = filtered_display[search_mask]

# Filter by Date
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    # Ensure we are comparing dates correctly
    mask_date = (filtered_display['date_published'].dt.date >= start_date) & \
                (filtered_display['date_published'].dt.date <= end_date)
    filtered_display = filtered_display[mask_date]

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

# --- 5.5 GOVERNANCE METRICS: AI ACCURACY ---
st.subheader("⚖️ Governance: AI Accuracy & Verification")

# Calculate the split between Auto and Manual
# We use the 'status' column we initialized in Section 1
gov_counts = filtered_display['status'].value_counts().reset_index()
gov_counts.columns = ['Source', 'Count']

# Create a donut chart to visualize the "Audit Rate"
fig_gov = px.pie(
    gov_counts, 
    values='Count', 
    names='Source', 
    hole=0.5,
    title="Human-in-the-Loop Verification Rate",
    color='Source',
    # Consistent visual encoding: Blue for AI, Orange/Red for Human
    color_discrete_map={'🤖 Auto': '#3498db', '👤 Manual': '#e67e22'}
)

# Professional styling to match the rest of the dash
fig_gov.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_gov, use_container_width=True)

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
display_columns = ["status", "sentiment", "score",'date_published', "title", "description", "publisher", "link"]
df_display = filtered_display[display_columns].copy()
df_display['date_published'] = df_display['date_published'].dt.strftime('%Y-%m-%d %H:%M')

st.dataframe(
    df_display, 
    use_container_width=True,
    on_select="rerun", 
    selection_mode="single-row",
    column_config={
        "link": st.column_config.LinkColumn("Link", display_text="Open Article"),
        "score": st.column_config.NumberColumn("Score", format="%.3f"),
        "status": st.column_config.TextColumn("Status", help="🤖 = Auto, 👤 = Manual Override")
    },
    key="table_selection"

)

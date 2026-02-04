import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")

st.title("📊 News Sentiment Analysis Dashboard")
st.markdown("This dashboard analyzes live news headlines using **VADER NLP**.")

# 2. Load the Data
try:
    df = pd.read_csv("news_sentiment_report.csv")
    
    # 3. Sidebar Metrics
    st.sidebar.header("Data Summary")
    st.sidebar.metric("Total Articles", len(df))
    st.sidebar.write("Project: AI Sentiment Sandbox")

    # 4. Visualization: Sentiment Distribution
    st.subheader("Sentiment Breakdown")
    sentiment_counts = df['sentiment'].value_counts()
    
    # Create a simple bar chart for quick executive summary
    st.bar_chart(sentiment_counts)

    # 5. Searchable Data Table with Clickable Links
    st.subheader("Latest Headlines & Context")
    
    st.dataframe(
        df,
        column_config={
            "link": st.column_config.LinkColumn(
                "Source Link",     # Label for the user
                help="Click to read the full article",
                validate="^https://",
            ),
            "score": st.column_config.NumberColumn(
                "Sentiment Score",
                format="%.2f",     # Rounds to 2 decimal places in the UI
            )
        },
        hide_index=True,
        use_container_width=True # Makes the table fill the screen nicely
    )

except FileNotFoundError:
    st.error("CSV file not found. Please run 'python3 live_ingest.py' first!")
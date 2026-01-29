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
    total_articles = len(df)
    st.sidebar.metric("Total Articles", total_articles)

    # 4. Visualization: Sentiment Distribution
    st.subheader("Sentiment Breakdown")
    sentiment_counts = df['sentiment'].value_counts()
    
    # Create a columns layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("Raw Counts:")
        st.dataframe(sentiment_counts)
        
    with col2:
        st.bar_chart(sentiment_counts)

    # 5. Searchable Data Table
    st.subheader("Latest Headlines")
    st.dataframe(df[['title', 'publisher', 'sentiment', 'score', 'link']])

except FileNotFoundError:
    st.error("CSV file not found. Please run 'python3 live_ingest.py' first!")
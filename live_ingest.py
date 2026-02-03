"""
PROJECT: Real-Time News Sentiment Pipeline
AUTHOR: Deborah Kalanit
VERSION: 2.0 (VADER NLP + Excel-Optimized Export)
DESCRIPTION: 
    Ingests live headlines via NewsAPI, performs contextual 
    sentiment analysis using VADER, and exports an enriched 
    CSV report with metadata for stakeholders.
"""
import os
import requests
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# --- CONFIGURATION SETTINGS ---
LIMIT = 100  # Change this one number to scale your whole project!
TOPIC = "Artificial Intelligence"

analyzer = SentimentIntensityAnalyzer()

new_words = {
    'deal': 0.5,   # We want 'deal' to be slightly positive in our context
    'oled': 0.8,      # Tech wins!
    'easier': 1.0,    # Efficiency wins!
    'deepfakes': -2.0 # Still very bad
}
analyzer.lexicon.update(new_words)

# Load security layer
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def analyze_news_to_csv(query="Technology"):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize=100&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        processed_data = [] 
        
        print(f"Analyzing {len(articles[:LIMIT])} headlines...")

        for art in articles[:LIMIT]:
            title = art['title']
            publisher = art['source']['name'] # Accessing the nested 'source' name
            link = art['url'] # The direct URL
            
            # --- NLP ANALYSIS (VADER STYLE) ---
            # VADER gives us a 'dictionary' of scores (pos, neg, neu, and compound)
            vs = analyzer.polarity_scores(title)
            score = vs['compound'] # Compound is the overall "summary" score
            
            # Classification logic (VADER is more precise, so we keep the same logic)
            if score >= 0.05:
                label = "Positive"
            elif score <= -0.05:
                label = "Negative"
            else:
                label = "Neutral"
            
            processed_data.append({
                "title": title,
                "publisher": publisher,
                "link": link,
                "sentiment": label,
                "score": round(score, 2)
            })

        filename = "news_sentiment_report.csv"
        keys = ["title", "publisher", "sentiment", "score", "link"] 
        
        with open(filename, "w", newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(processed_data)
            
        print(f"Done! Report saved as {filename}")
    else:
        print(f"Error: {response.status_code}")

# Run the full pipeline
analyze_news_to_csv(TOPIC)
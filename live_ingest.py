import os
import requests
import pandas as pd
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# --- CONFIGURATION SETTINGS ---
LIMIT = 100 
TOPIC = "Artificial Intelligence"
FILENAME = "news_sentiment_report.csv"

analyzer = SentimentIntensityAnalyzer()
# Custom lexicon tuning remains the same
new_words = {'deal': 0.5, 'oled': 0.8, 'easier': 1.0, 'deepfakes': -2.0}
analyzer.lexicon.update(new_words)

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def analyze_news_to_csv(query="Technology"):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize=100&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        processed_data = [] 
        
        # New: Capture the ingestion timestamp
        ingest_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"Analyzing {len(articles[:LIMIT])} headlines...")

        for art in articles[:LIMIT]:
            title = art['title']
            description = art.get('description', "")
            full_text = f"{title} {description}"
            
            vs = analyzer.polarity_scores(full_text)
            score = vs['compound']
            
            if score >= 0.05:
                label = "Positive"
            elif score <= -0.05:
                label = "Negative"
            else:
                label = "Neutral"
            
            # Updated Data Dictionary with Date Stamps and Status
            processed_data.append({
                "status": "🤖 Auto",
                "date_published": art['publishedAt'], # Timestamp from NewsAPI
                "date_added": ingest_time,             # Internal ingestion time
                "title": title,
                "description": description,
                "publisher": art['source']['name'],
                "link": art['url'],
                "sentiment": label,
                "score": round(score, 2)
            })

        new_df = pd.DataFrame(processed_data)
        
        # New: Append logic to prevent overwriting historical data
        if not os.path.isfile(FILENAME):
            new_df.to_csv(FILENAME, index=False, encoding='utf-8-sig')
            print(f"Created new historical record: {FILENAME}")
        else:
            new_df.to_csv(FILENAME, mode='a', index=False, header=False, encoding='utf-8-sig')
            print(f"Appended {len(new_df)} records to {FILENAME}")
            
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    analyze_news_to_csv(TOPIC)
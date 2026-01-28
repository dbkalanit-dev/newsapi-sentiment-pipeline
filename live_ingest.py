import os
import requests
import csv
from textblob import TextBlob
from dotenv import load_dotenv

# Load security layer
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def analyze_news_to_csv(query="Artificial Intelligence"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        processed_data = [] # Our collection bucket
        
        print(f"Analyzing {len(articles[:10])} headlines...")

        for art in articles[:10]:
            title = art['title']
            analysis = TextBlob(title)
            score = analysis.sentiment.polarity
            
            # Classification logic
            if score > 0:
                label = "Positive"
            elif score < 0:
                label = "Negative"
            else:
                label = "Neutral"
            
            # Store the data in a "Row" format
            processed_data.append({
                "title": title,
                "sentiment": label,
                "score": round(score, 2)
            })

        # --- EXPORT STEP ---
        filename = "news_sentiment_report.csv"
        keys = ["title", "sentiment", "score"]
        
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(processed_data)
            
        print(f"Done! Report saved as {filename}")
    else:
        print(f"Error: {response.status_code}")

# Run the full pipeline
analyze_news_to_csv("Technology")
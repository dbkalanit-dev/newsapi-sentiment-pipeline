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
            publisher = art['source']['name'] # Accessing the nested 'source' name
            link = art['url'] # The direct URL
            
            analysis = TextBlob(title)
            score = analysis.sentiment.polarity
            
            # Classification
            label = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
            
            # Now we add the new fields to our dictionary
            processed_data.append({
                "title": title,
                "publisher": publisher,
                "link": link,
                "sentiment": label,
                "score": round(score, 2)
            })

        # Update the CSV keys to include the new columns
        filename = "news_sentiment_report.csv"
        keys = ["title", "publisher", "sentiment", "score", "link"] # Added new keys
        
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(processed_data)
            
        print(f"Done! Report saved as {filename}")
    else:
        print(f"Error: {response.status_code}")

# Run the full pipeline
analyze_news_to_csv("Technology")
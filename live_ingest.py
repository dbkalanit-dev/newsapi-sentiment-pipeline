import os
import requests
from textblob import TextBlob
from dotenv import load_dotenv # Import the environment loader

# This finds the .env file and loads the variables
load_dotenv()

# Instead of the plain text key, we pull from the environment
API_KEY = os.getenv("NEWS_API_KEY") 


def analyze_news(query="technology"):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        
        print(f"--- Sentiment Analysis for '{query}' ---")
        
        for art in articles[:5]:  # Let's look at the first 5
            title = art['title']
            
            # This is the ML part!
            analysis = TextBlob(title)
            score = analysis.sentiment.polarity # Returns a number between -1 and 1
            
            # Categorize the score
            if score > 0:
                sentiment = "POSITIVE"
            elif score < 0:
                sentiment = "NEGATIVE"
            else:
                sentiment = "NEUTRAL"
            
            print(f"[{sentiment}] Score: {score:.2f} | {title}")
    else:
        print("Error fetching data.")

analyze_news("Apple")
# News Sentiment Analysis Pipeline

## Project Overview
A real-time data pipeline designed to ingest unstructured news data via REST API and perform NLP-based sentiment analysis. This project demonstrates a production-ready approach to handling live data streams and automated insights generation.

## The Tech Stack
* **Language:** Python 3.9+
* **Ingestion:** NewsAPI (RESTful API)
* **NLP Engine:** TextBlob (Natural Language Processing)
* **Environment Management:** Python-Dotenv (Security/Secrets Management)

## System Architecture
1. **Ingestion Layer:** Connects to NewsAPI to fetch headlines based on specific keyword queries.
2. **Preprocessing:** Cleans strings and prepares text for inference.
3. **Inference Layer:** Utilizes a pre-trained Lexicon-based model to assign sentiment polarity scores (-1.0 to +1.0).
4. **Classification:** Maps polarity scores to categorical labels (Positive, Negative, Neutral) for business reporting.

## Key Technical Challenges Overcome
* **API Authentication:** Implemented secure credential management using `.env` files to prevent exposure of sensitive keys in version control.
* **Resilience:** Built-in error handling for API status codes (e.g., 401 Unauthorized, 429 Rate Limiting).
* **Environment Configuration:** Managed POSIX file paths and hidden system files in a macOS ZSH environment.

## How to Run
1. Clone the repo.
2. Create a `.env` file with your `NEWS_API_KEY`.
3. Run `pip install -r requirements.txt`.
4. Execute `python3 live_ingest.py`.
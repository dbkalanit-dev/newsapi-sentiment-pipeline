# News Sentiment Analysis Pipeline

## Project Overview
A real-time data pipeline designed to ingest unstructured news data via REST API and perform NLP-based sentiment analysis. This project demonstrates a production-ready approach to handling live data streams and automated insights generation.

## Technical Stack Update (v2.0)
- **Sentiment Engine:** Switched from `TextBlob` to `VADER` (Valence Aware Dictionary and sEntiment Reasoner) to better handle contextual negations and technical jargon.
- **Encoding:** Implemented `utf-8-sig` export to ensure cross-platform compatibility with Microsoft Excel's character rendering.
- **Data Enrichment:** Added Publisher names and Source URLs for full data traceability.

## Model Tuning
To improve accuracy for technical news, the VADER lexicon was custom-tuned:
- **Positive Weights:** "OLED", "HDR", "Efficiency", "Illegal" (when referring to harmful content).
- **Negative Weights:** "Deepfakes", "Vulnerability".

## System Architecture
1. **Ingestion Layer:** Connects to NewsAPI to fetch headlines based on specific keyword queries.
2. **Preprocessing:** Cleans strings and prepares text for inference.
3. **Inference Layer:** Utilizes a pre-trained Lexicon-based model to assign sentiment polarity scores (-1.0 to +1.0).
4. **Classification:** Maps polarity scores to categorical labels (Positive, Negative, Neutral) for business reporting.

## Data Dictionary (Output Schema)
The final `news_sentiment_report.csv` contains the following fields:

| Column | Description | Data Type |
| :--- | :--- | :--- |
| **Title** | The headline of the news article. | String |
| **Publisher** | The news outlet that published the story (e.g., BBC, CNBC). | String |
| **Sentiment** | Categorical label based on polarity score (Positive/Negative/Neutral). | String |
| **Score** | Numerical polarity value ranging from -1.0 to 1.0. | Float |
| **Link** | Direct URL to the original article source. | URL |

## Key Technical Challenges Overcome
* **API Authentication:** Implemented secure credential management using `.env` files to prevent exposure of sensitive keys in version control.
* **Resilience:** Built-in error handling for API status codes (e.g., 401 Unauthorized, 429 Rate Limiting).
* **Environment Configuration:** Managed POSIX file paths and hidden system files in a macOS ZSH environment.

## How to Run
1. Clone the repo.
2. Create a `.env` file with your `NEWS_API_KEY`.
3. Run `pip install -r requirements.txt`.
4. Execute `python3 live_ingest.py`.
# WhatsApp Chat Analyzer

A Streamlit-based web app to analyze WhatsApp chat exports.

It extracts meaningful insights such as message density, user activity cycles, sentiment trends, and word clouds, making it useful for personal reflection, group analysis, or community engagement strategies.

## Features

- Upload & Parse WhatsApp chats (supports both individual and group chats).
- Regex-based preprocessing to extract timestamps, users, and messages from .txt chat exports.
- Interactive Visualizations:
  - Daily / monthly message trends
  - Most active users and contribution breakdown
  - Hourly activity cycles
- Word Clouds: highlights most frequent words, with sentiment-aware coloring.
- Sentiment Analysis: Positive vs Negative vs Neutral distribution of messages.
- Web-based (Streamlit) — no setup needed beyond Python + libraries.

## Tech Stack
- Python 3.x
- Streamlit – web UI framework
- Regex – chat parsing
- pandas – data wrangling
- matplotlib / seaborn – visualizations
- wordcloud – text cloud generation
- nltk / textblob / vaderSentiment – sentiment analysis

## Project Structure
```
WhatsApp-Chat-Analyzer/
│── app.py                # Main Streamlit app
│── preprocessing.py      # Regex parsing & data cleaning
│── analysis.py           # Functions for insights/visuals
│── requirements.txt      # Dependencies
│── sample_chat.txt       # Example WhatsApp export file
│── README.md             # Documentation
```

## Installation & Usage
1. Clone the repository
   ```
   git clone https://github.com/ruchikapatro24/WhatsApp-Chat-Analyzer.git
   cd WhatsApp-Chat-Analyzer
   ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app
   ```
   streamlit run app.py
   ```
4. Upload a WhatsApp chat file
- Export from WhatsApp:
  ```
  ⋮ > More > Export Chat > Without Media
  ```
- Upload the .txt file in the app.
- Explore interactive analytics

## License
This project is licensed under the MIT License.

---

✨ Built by [Ruchika Patro](https://github.com/ruchikapatro24)

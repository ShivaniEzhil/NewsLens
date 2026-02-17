# NewsLens - AI-Powered News Summarizer

NewsLens is a web application that automatically generates concise summaries from news articles using state-of-the-art AI.

## Features
- **URL Extraction:** Extracts text from any news article URL.
- **AI Summarization:** Uses the `facebook/bart-large-cnn` model via Hugging Face Transformers.
- **Clean UI:** A modern, responsive interface built with Flask and CSS.

## Setup

1.  **Clone the repository** (if applicable).
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run NLTK setup:**
    ```bash
    python setup_nltk.py
    ```

## Usage

1.  **Start the app:**
    ```bash
    python app.py
    ```
2.  **Open in browser:**
    Navigate to `http://127.0.0.1:5000`

## Technologies
- Python
- Flask
- Hugging Face Transformers
- Newspaper3k

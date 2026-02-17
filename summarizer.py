from newspaper import Article
from transformers import pipeline

# Initialize the summarization pipeline
# Using facebook/bart-large-cnn model which is excellent for news summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_article(url):
    """
    Extracts the title and text from a given URL using newspaper3k.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "error": None
        }
    except Exception as e:
        return {
            "title": None,
            "text": None,
            "error": str(e)
        }

def generate_summary(text, max_length=150, min_length=50):
    """
    Generates a summary of the provided text using the BART model.
    Handles long text by chunking if necessary, but for simplicity, we'll
    truncate to the model's limit (1024 tokens) which pipeline handles automatically usually,
    but it's good practice to be aware of limits.
    """
    try:
        # The pipeline handles tokenization and truncation automatically
        # but for very long texts, we might want to truncate manually to be safe.
        # BART's max position embedding is 1024.
        
        # Simple truncation to ~3000 chars to avoid model errors on extremely long inputs
        # Real-world apps might need smarter chunking.
        truncated_text = text[:3000] 
        
        summary = summarizer(truncated_text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error generating summary: {str(e)}"

if __name__ == "__main__":
    # Test quickly
    test_url = "https://www.bbc.com/news/world-us-canada-68385074" # Example URL
    # Note: Replace with a valid URL for testing
    print("Summarizer module loaded.")

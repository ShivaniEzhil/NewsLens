from newspaper import Article
from transformers import pipeline
import pdfplumber
import pytesseract
from PIL import Image
import io

# Note: Model is now loaded in app.py via st.cache_resource for better thread safety on macOS.


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

def extract_from_pdf(file_stream):
    """
    Extracts text from a PDF file stream using pdfplumber.
    """
    try:
        text = ""
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_from_image(file_stream):
    """
    Extracts text from an image file stream using Tesseract OCR.
    """
    try:
        image = Image.open(file_stream)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error extraction Image OCR: {str(e)}"

def generate_summary(text, summarizer_model, max_length=150, min_length=50):

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
        
        # The pipeline is now passed as an argument or loaded via cache
        summary = summarizer_model(truncated_text, max_length=max_length, min_length=min_length, do_sample=False)

        return summary[0]['summary_text']
    except Exception as e:
        return f"Error generating summary: {str(e)}"

if __name__ == "__main__":
    # Note: Testing now requires a model instance.
    print("Summarizer module loaded. Use app.py to run with caching.")


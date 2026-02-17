from flask import Flask, render_template, request
from summarizer import extract_article, generate_summary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        summary = ""
        original_text = ""
        original_title = "Uploaded Content"
        url = None
        error = None

        if 'url' in request.form and request.form['url']:
            url = request.form['url']
            article_data = extract_article(url)
            if article_data['error']:
                return render_template('index.html', error=article_data['error'])
            original_text = article_data['text']
            original_title = article_data['title']

        elif 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return render_template('index.html', error="No file selected")
            
            if file.filename.lower().endswith('.pdf'):
                original_text = extract_from_pdf(file)
            elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                original_text = extract_from_image(file)
            else:
                return render_template('index.html', error="Unsupported file type")
            
            if original_text.startswith("Error"):
                 return render_template('index.html', error=original_text)

        if not original_text:
             return render_template('index.html', error="Could not extract text from input")

        summary = generate_summary(original_text)
        
        return render_template('result.html', 
                               summary=summary, 
                               original_title=original_title,
                               original_text=original_text,
                               url=url)

if __name__ == '__main__':
    app.run(debug=True)

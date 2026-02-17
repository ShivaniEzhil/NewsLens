from flask import Flask, render_template, request
from summarizer import extract_article, generate_summary

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if request.method == 'POST':
        url = request.form['url']
        article_data = extract_article(url)

        if article_data['error']:
            return render_template('index.html', error=article_data['error'])

        summary = generate_summary(article_data['text'])
        
        return render_template('result.html', 
                               summary=summary, 
                               original_title=article_data['title'],
                               original_text=article_data['text'],
                               url=url)

if __name__ == '__main__':
    app.run(debug=True)

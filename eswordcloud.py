import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the dataset
data = pd.read_csv(r"E:\BRUH!!!\Projects\Project 1 (SntAnl)\Web App\flipkart_updated.csv")

# Function to extract keywords from reviews
def extract_keywords(reviews):
    # Initialize TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    # Fit the vectorizer on the reviews
    tfidf_matrix = tfidf_vectorizer.fit_transform(reviews)
    # Get feature names (words)
    feature_names = tfidf_vectorizer.get_feature_names_out()
    # Get TF-IDF scores for each feature in each review
    tfidf_scores = tfidf_matrix.sum(axis=0)
    # Sort the features by their TF-IDF scores
    sorted_indices = tfidf_scores.argsort()[0, ::-1]
    # Get the top keywords
    top_keywords = [feature_names[i] for i in sorted_indices[:]]  # Get all keywords
    return [str(keyword) for keyword in top_keywords]  # Convert keywords to strings

# Function to generate Word Cloud and save as image
def generate_wordcloud(reviews):
    keywords = extract_keywords(reviews)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(keywords))
    # Save Word Cloud as an image
    wordcloud.to_file('static/wordcloud.png')

# Route for the home page
@app.route('/')
def index():
    return render_template('search.html')

# Route for handling search and displaying result
@app.route('/search', methods=['POST'])
def search_reviews():
    search_query = request.form['search_query'].strip().lower()

    if search_query == "":
        return "Please enter a search query."

    filtered_data = data[data['company_name'].str.contains(search_query, case=False)]

    if len(filtered_data) > 0:
        reviews = filtered_data['Review'].tolist()
        generate_wordcloud(reviews)
        return render_template('result.html')
    else:
        return "No reviews found for the given search criteria."

if __name__ == '__main__':
    app.run(debug=True, port=5001)
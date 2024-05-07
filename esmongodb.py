#Website to Print All Company Rankings

from flask import Flask, render_template
import pandas as pd
from pymongo import MongoClient
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
import nltk
import collections
from tqdm import tqdm

app = Flask(__name__)

# MongoDB connection details
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'emosense'
MONGO_COLLECTION = 'flipkart dataset'

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

@app.route('/')
def index():
    # Perform sentiment analysis
    companies, scores = perform_sentiment_analysis()
    
    # Render HTML template with sentiment analysis results
    return render_template('index.html', companies=companies, scores=scores)

def perform_sentiment_analysis():
    # Ensure NLTK resources are downloaded
    nltk.download('punkt')
    nltk.download('vader_lexicon')

    # Query data from MongoDB
    cursor = collection.find().limit(2305)  # Limit to the first specified number of reviews

    # Initialize the NLTK sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    # Create a defaultdict to store reviews for each company
    company_reviews = collections.defaultdict(list)

    # Populate the company_reviews dictionary
    for doc in tqdm(cursor, desc="Processing Reviews"):
        company = doc['Company']
        review = doc['Review']
        company_reviews[company].append(review)

    # Calculate the sentiment scores for each company
    company_scores = {}
    for company, reviews in company_reviews.items():
        total_score = 0
        for review in reviews:
            # Tokenize the review into words
            words = word_tokenize(review)
            # Compute the sentiment score for each word and aggregate
            for word in words:
                scores = sid.polarity_scores(word)
                total_score += scores['compound']

        # Calculate the average score for the company
        company_scores[company] = total_score / len(reviews)

    # Convert company scores dictionary to lists for plotting
    companies = list(company_scores.keys())
    scores = list(company_scores.values())

    return companies, scores

if __name__ == '__main__':
    app.run(debug=True)
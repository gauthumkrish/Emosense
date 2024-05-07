from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['emosense']
collection = db['flipkart dataset']

@app.route('/')
def index():
    # Fetch data from MongoDB
    results = collection.find()

    # Count occurrences of company names
    company_count = {}
    for result in results:
        company_name = result['Company']
        company_count[company_name] = company_count.get(company_name, 0) + 1

    # Sort company names and sales counts based on sales counts
    sorted_data = sorted(company_count.items(), key=lambda x: x[1], reverse=True)
    company_names = [item[0] for item in sorted_data]
    sales_counts = [item[1] for item in sorted_data]

    return render_template('admin_index_sales.html', company_names=company_names, sales_counts=sales_counts)

@app.route('/update', methods=['POST'])
def update_data():
    company_name = request.form['company']
    new_sales_count = int(request.form['sales'])

    # Update the MongoDB collection with the new sales count
    collection.update_one({'Company': company_name}, {'$set': {'Sales': new_sales_count}})

    # Redirect back to the index page or return a success message
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True , port=5005)

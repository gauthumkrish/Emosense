from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['emosense']  # Change this to your database name
collection = db['create_account']  # Change this to your collection name

@app.route('/')
def index():
    return render_template('create_account.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phonenumber']
        password = request.form['password']
        user_type = request.form['type']  # Get the fixed user type value
        # Check if username already exists
        if collection.find_one({'username': username}):
            return "Username already exists!"
        else:
            collection.insert_one({'username': username, 'email': email, 'phone_number': phone_number, 'password': password, 'type': user_type})  # Include the user type
            return redirect('/')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5003)

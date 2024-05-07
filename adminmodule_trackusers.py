from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['emosense']
collection = db['create_account']

@app.route('/')
def index():
    # Fetch user data from MongoDB
    users = list(collection.find())
    # Convert ObjectId to string for serialization
    for user in users:
        user['_id'] = str(user['_id'])
    return render_template('admin_index_users.html', users=users)

@app.route('/update/<string:user_id>', methods=['POST'])
def update_user(user_id):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        user_type = request.form['type']

        # Update user data in MongoDB
        collection.update_one({'_id': ObjectId(user_id)}, {'$set': {
            'username': username,
            'email': email,
            'phone_number': phone_number,
            'password': password,
            'type': user_type
        }})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True , port=5006)

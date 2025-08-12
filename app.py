from flask import Flask, request, jsonify
from flask_login import LoginManager

from database import db
from models.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
# Initialize the database
db.init_app(app)
login_manager.init_app(app)
#  set login view

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return jsonify({'message': 'User logged in successfully'})

    return jsonify({'message': 'Invalid credentials'}), 400
    

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)

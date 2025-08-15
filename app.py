from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

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
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({'message': 'User logged in successfully'})

    return jsonify({'message': 'Invalid credentials'}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():

    logout_user()
    return jsonify({'message': 'User logged out successfully'})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 200

    return jsonify({'message': 'Invalid data'}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username
        }), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    data = request.json
    password = data.get('password')

    if user and password:
        user.password = password

        db.session.commit()
        return jsonify({'message': f'User {user_id} updated successfully'}), 200

    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

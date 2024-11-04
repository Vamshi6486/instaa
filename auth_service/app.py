from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SECRET_KEY = "your_secret_key"  # Replace with a secure key for JWT signing

class User(db.Model):
    user_id = db.Column(db.String(80), primary_key=True)  # Set user_id as the primary key
    password = db.Column(db.String(120), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            return jsonify({"message": "user_id and password are required!"}), 400

        # Check if the user_id already exists
        existing_user = User.query.get(user_id)
        if existing_user:
            return jsonify({"message": "user_id already exists!"}), 409  # 409 Conflict status code

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(user_id=user_id, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        
        if not user_id or not password:
            return jsonify({"message": "user_id and password are required!"}), 400

        # Retrieve user from the database using user_id as the primary key
        user = User.query.get(user_id)
        
        # Validate credentials
        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Invalid user_id or password!"}), 401

        # Generate JWT token upon successful login
        token = jwt.encode({
            "user_id": user.user_id,  # Store user_id in the token
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        
        # Redirect to feed in post_service with token in URL
        return redirect(f"http://localhost:5000/feed?token={token}")
    
    # Render the login form
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

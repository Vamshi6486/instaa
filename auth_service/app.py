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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({"message": "Username and password are required!"}), 400

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Access form data directly from request.form
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return jsonify({"message": "Username and password are required!"}), 400

        # Retrieve user from the database
        user = User.query.filter_by(username=username).first()
        
        # Validate credentials
        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Invalid username or password!"}), 401

        # Generate JWT token upon successful login
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        
        # Redirect to feed in post_service with token in URL
        return redirect(f"http://localhost:5000/feed?token={token}")
    
    # Render the login form
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

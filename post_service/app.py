from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import jwt
import os
from werkzeug.utils import secure_filename
from functools import wraps

# Set up the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Secret key for JWT
SECRET_KEY = "your_secret_key"

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=True)

@app.before_first_request
def create_tables():
    db.create_all()

def token_required(f):
    """Decorator to check for valid JWT token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 403
        return f(current_user_id, *args, **kwargs)
    return decorated_function

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/feed', methods=['GET'])
@token_required
def feed(current_user_id):
    posts = Post.query.all()
    all_posts = [{"id": post.id, "user_id": post.user_id, "image_path": post.image_path, "caption": post.caption} for post in posts[::-1]]
    return render_template('feed.html', posts=all_posts, user_id=current_user_id)

@app.route('/posts', methods=['POST'])
@token_required
def create_post(current_user_id):
    data = request.form
    caption = data.get('caption')
    image = request.files.get('image')

    if not image:
        return jsonify({"message": "Image is required!"}), 400

    # Create a secure filename to prevent directory traversal attacks
    image_filename = secure_filename(image.filename)
    save_path = os.path.join(UPLOAD_FOLDER, image_filename)

    try:
        image.save(save_path)  # Save the image to the uploads directory
    except Exception as e:
        return jsonify({"message": f"Error saving image: {str(e)}"}), 500

    new_post = Post(user_id=current_user_id, image_path=image_filename, caption=caption)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Post created successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

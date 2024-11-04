from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)  # Reference to the post being commented on
    user_id = db.Column(db.Integer, nullable=False)  # Reference to the user making the comment
    content = db.Column(db.String, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()  # Create tables before the first request

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    post_id = data.get('post_id')
    user_id = data.get('user_id')  # Get user_id from request
    comment = data.get('comment')
    
    if not post_id or not user_id or not comment:
        return jsonify({"message": "Post ID, User ID, and content are required!"}), 400

    new_comment = Comment(post_id=post_id, user_id=user_id, content=comment)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully!"}), 201

@app.route('/comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()  # Retrieve comments for a specific post
    all_comments = [{"id": comment.id, "post_id": comment.post_id, "user_id": comment.user_id, "content": comment.content} for comment in comments[::-1]]
    return jsonify(all_comments), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)  # Change the port if necessary

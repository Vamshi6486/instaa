from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'  # SQLite database for comments
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)  # Reference to the post being commented on
    content = db.Column(db.String, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all()  # Create tables before the first request

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    post_id = data.get('post_id')
    comment = data.get('comment')
    
    if not post_id or not comment:
        return jsonify({"message": "Post ID and content are required!"}), 400

    new_comment = Comment(post_id=post_id, content=comment)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully!"}), 201

@app.route('/comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()  # Retrieve comments for a specific post
    all_comments = [{"id": comment.id, "post_id": comment.post_id, "content": comment.content} for comment in comments]
    return jsonify(all_comments), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)  # Change the port if necessary

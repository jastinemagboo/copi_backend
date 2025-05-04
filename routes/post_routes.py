from flask import Blueprint, request, jsonify
from models.post_model import Post
from extensions import db  # ✅ not from app
from datetime import datetime

post_bp = Blueprint('post_bp', __name__)

# This route creates a new post entry in the database using the HTTP POST method.
@post_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400

    new_post = Post(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        'message': 'Created successfully!',
        'post': {
            'id': new_post.id,
            'title': new_post.title,
            'content': new_post.content,
            'created_at': new_post.created_at
        }
    }), 201

# This route retrieves post data from the server using the HTTP GET method.
@post_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.filter(Post.deleted_at.is_(None)).order_by(Post.created_at.desc()).all()
    posts_data = []

    # Loop through each post and add it to the posts_data list
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'created_at': post.created_at,
            'updated_at': post.updated_at
        })

    return jsonify(posts_data), 200

# This route updates the title and/or content of a specific post using the HTTP PATCH method.
@post_bp.route('/posts/<uuid:id>', methods=['PATCH'])
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.get_json()

    title = data.get('title')
    content = data.get('content')

    if title is None and content is None:
        return jsonify({'error': 'No data provided to update'}), 400

    if title is not None:
        post.title = title
    if content is not None:
        post.content = content

    post.updated_at = datetime.now()
    db.session.commit()

    return jsonify({
        'message': 'Post updated successfully',
        'post': {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'updated_at': post.updated_at
        }
    }), 200

# This route performs a soft delete on a specific post using the HTTP DELETE method.
@post_bp.route('/posts/<uuid:id>', methods=['DELETE'])
def delete_post(id):
    post = Post.query.get(id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    post.deleted_at = datetime.now()
    db.session.commit()
    return jsonify({'message': 'Successfully deleted'}), 200


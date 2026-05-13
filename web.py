from flask import Flask, render_template, jsonify, request
from db import Database
from config import FLASK_SECRET_KEY

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
db = Database()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users from the database."""
    users = db.get_all_users()
    return jsonify(users)

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID."""
    user = db.get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics."""
    stats = {
        'total_users': db.get_total_users(),
        'active_users': db.get_active_users()
    }
    return jsonify(stats)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



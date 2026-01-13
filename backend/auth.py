from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import re

auth_bp = Blueprint('auth', __name__)

def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'status': 'error', 
                'message': 'Username and password are required',
                'data': {}
            }), 400
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return jsonify({
                'status': 'success', 
                'message': 'Login successful',
                'data': {
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'role': user['role']
                    }
                }
            })
        
        return jsonify({
            'status': 'error', 
            'message': 'Invalid credentials',
            'data': {}
        }), 401
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'user')  # default to user role
        
        if not username or not password or not email:
            return jsonify({
                'status': 'error', 
                'message': 'Username, password, and email are required',
                'data': {}
            }), 400
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({
                'status': 'error', 
                'message': 'Invalid email format',
                'data': {}
            }), 400
        
        # Validate password strength
        if len(password) < 6:
            return jsonify({
                'status': 'error', 
                'message': 'Password must be at least 6 characters long',
                'data': {}
            }), 400
        
        conn = get_db_connection()
        
        # Check if username already exists
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'Username already exists',
                'data': {}
            }), 409
        
        # Hash password and create user
        password_hash = generate_password_hash(password)
        
        conn.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                     (username, password_hash, role, email))
        conn.commit()
        user_id = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
        conn.close()
        
        return jsonify({
            'status': 'success', 
            'message': 'Registration successful',
            'data': {'user_id': user_id}
        })
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({
            'status': 'success', 
            'message': 'Logged out successfully',
            'data': {}
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@auth_bp.route('/profile', methods=['GET'])
def profile():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        conn = get_db_connection()
        user = conn.execute('SELECT id, username, role, email, created_at FROM users WHERE id = ?', 
                           (session['user_id'],)).fetchone()
        conn.close()
        
        if user:
            return jsonify({
                'status': 'success',
                'message': 'Profile retrieved successfully',
                'data': dict(user)
            })
        else:
            return jsonify({
                'status': 'error', 
                'message': 'User not found',
                'data': {}
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500
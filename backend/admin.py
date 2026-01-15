from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
import sqlite3

admin_bp = Blueprint('admin', __name__)

def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        conn = get_db_connection()
        # Get system stats
        user_count = conn.execute('SELECT COUNT(*) FROM users WHERE role = "user"').fetchone()[0]
        doctor_count = conn.execute('SELECT COUNT(*) FROM users WHERE role = "doctor"').fetchone()[0]
        prediction_count = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
        chat_count = conn.execute('SELECT COUNT(*) FROM chats').fetchone()[0]
        
        # Get recent activity
        recent_users = conn.execute('''
            SELECT id, username, role, created_at
            FROM users
            ORDER BY created_at DESC
            LIMIT 10
        ''').fetchall()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Dashboard data retrieved successfully',
            'data': {
                'stats': {
                    'users': user_count,
                    'doctors': doctor_count,
                    'predictions': prediction_count,
                    'chats': chat_count
                },
                'recent_activity': [dict(user) for user in recent_users]
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        conn = get_db_connection()
        users = conn.execute('SELECT id, username, role, email, created_at FROM users ORDER BY created_at DESC').fetchall()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Users retrieved successfully',
            'data': [dict(user) for user in users]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@admin_bp.route('/doctors', methods=['GET'])
def get_all_doctors():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        conn = get_db_connection()
        doctors = conn.execute('''
            SELECT u.id, u.username, u.email, d.specialization, d.license_number, u.created_at
            FROM users u
            LEFT JOIN doctors d ON u.id = d.user_id
            WHERE u.role = 'doctor'
            ORDER BY u.created_at DESC
        ''').fetchall()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Doctors retrieved successfully',
            'data': [dict(doctor) for doctor in doctors]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@admin_bp.route('/users', methods=['POST'])
def create_user():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'user')
        
        if not username or not password or not email:
            return jsonify({
                'status': 'error', 
                'message': 'Username, password, and email are required',
                'data': {}
            }), 400
        
        if role not in ['user', 'doctor']:
            return jsonify({
                'status': 'error', 
                'message': 'Invalid role. Use "user" or "doctor"',
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
        
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                     (username, password_hash, role, email))
        user_id = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
        
        if role == 'doctor':
            conn.execute('INSERT INTO doctors (user_id, specialization) VALUES (?, ?)',
                         (user_id, data.get('specialization', 'General')))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'User created successfully',
            'data': {
                'user_id': user_id
            }
        })
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        data = request.get_json()
        conn = get_db_connection()
        
        # Update user info
        update_fields = []
        params = []
        
        if 'username' in data:
            update_fields.append('username = ?')
            params.append(data['username'])
        if 'email' in data:
            update_fields.append('email = ?')
            params.append(data['email'])
        if 'role' in data:
            update_fields.append('role = ?')
            params.append(data['role'])
        
        if update_fields:
            sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
            params.append(user_id)
            conn.execute(sql, params)
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'User updated successfully',
            'data': {}
        })
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        # Don't allow deleting admin users
        conn = get_db_connection()
        user = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        
        if not user:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'User not found',
                'data': {}
            }), 404
        
        if user['role'] == 'admin':
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'Cannot delete admin users',
                'data': {}
            }), 403
        
        # Remove assignments and related data
        conn.execute('DELETE FROM assignments WHERE user_id = ? OR doctor_id = ?', (user_id, user_id))
        conn.execute('DELETE FROM predictions WHERE user_id = ?', (user_id,))
        conn.execute('DELETE FROM chats WHERE sender_id = ? OR receiver_id = ?', (user_id, user_id))
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'User deleted successfully',
            'data': {}
        })
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@admin_bp.route('/assignments', methods=['GET'])
def get_assignments():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        conn = get_db_connection()
        assignments = conn.execute('''
            SELECT a.id, u.username as user_name, d.username as doctor_name, a.assigned_at as assigned_date
            FROM assignments a
            JOIN users u ON a.user_id = u.id
            JOIN users d ON a.doctor_id = d.id
            ORDER BY a.assigned_at DESC
        ''').fetchall()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Assignments retrieved successfully',
            'data': [dict(assignment) for assignment in assignments]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500


@admin_bp.route('/assignments/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        conn = get_db_connection()
        
        # Check if assignment exists
        assignment = conn.execute('SELECT * FROM assignments WHERE id = ?', (assignment_id,)).fetchone()
        if not assignment:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'Assignment not found',
                'data': {}
            }), 404
        
        # Remove the assignment
        conn.execute('DELETE FROM assignments WHERE id = ?', (assignment_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Assignment removed successfully',
            'data': {}
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500


@admin_bp.route('/assignments', methods=['POST'])
def assign_user_to_doctor():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        data = request.get_json()
        user_id = data.get('user_id')
        doctor_id = data.get('doctor_id')
        
        if not user_id or not doctor_id:
            return jsonify({
                'status': 'error', 
                'message': 'User ID and Doctor ID are required',
                'data': {}
            }), 400
        
        conn = get_db_connection()
        
        # Verify that both user and doctor exist
        user_exists = conn.execute('SELECT * FROM users WHERE id = ? AND role = "user"', (user_id,)).fetchone()
        doctor_exists = conn.execute('SELECT * FROM users WHERE id = ? AND role = "doctor"', (doctor_id,)).fetchone()
        
        if not user_exists:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'User not found or invalid role',
                'data': {}
            }), 404
        
        if not doctor_exists:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'Doctor not found or invalid role',
                'data': {}
            }), 404
        
        # Remove any existing assignment
        conn.execute('DELETE FROM assignments WHERE user_id = ?', (user_id,))
        # Create new assignment
        conn.execute('INSERT INTO assignments (user_id, doctor_id) VALUES (?, ?)', (user_id, doctor_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Assignment created successfully',
            'data': {}
        })
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@admin_bp.route('/logs', methods=['GET'])
def get_system_logs():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        # This would typically connect to a logging system
        # For now, we'll return a sample response
        return jsonify({
            'status': 'success',
            'message': 'System logs retrieved successfully',
            'data': {
                'logs': [
                    {'timestamp': '2024-01-13 22:30:00', 'level': 'INFO', 'message': 'System started'},
                    {'timestamp': '2024-01-13 22:31:00', 'level': 'INFO', 'message': 'Database initialized'},
                    {'timestamp': '2024-01-13 22:32:00', 'level': 'INFO', 'message': 'Admin logged in'},
                    {'timestamp': '2024-01-13 22:33:00', 'level': 'INFO', 'message': 'New user created: user1'},
                ]
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500
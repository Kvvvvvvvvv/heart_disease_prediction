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
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Not authorized'}), 401
    
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
        'stats': {
            'users': user_count,
            'doctors': doctor_count,
            'predictions': prediction_count,
            'chats': chat_count
        },
        'recent_activity': [dict(user) for user in recent_users]
    })

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Not authorized'}), 401
    
    conn = get_db_connection()
    users = conn.execute('SELECT id, username, role, email, created_at FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

@admin_bp.route('/doctors', methods=['GET'])
def get_all_doctors():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Not authorized'}), 401
    
    conn = get_db_connection()
    doctors = conn.execute('''
        SELECT u.id, u.username, u.email, d.specialization, d.license_number, u.created_at
        FROM users u
        LEFT JOIN doctors d ON u.id = d.user_id
        WHERE u.role = 'doctor'
        ORDER BY u.created_at DESC
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(doctor) for doctor in doctors])

@admin_bp.route('/users', methods=['POST'])
def create_user():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Not authorized'}), 401
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'user')
    
    if not username or not password or not email:
        return jsonify({'error': 'Username, password, and email are required'}), 400
    
    if role not in ['user', 'doctor']:
        return jsonify({'error': 'Invalid role. Use "user" or "doctor"'}), 400
    
    conn = get_db_connection()
    # Check if username already exists
    existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if existing_user:
        conn.close()
        return jsonify({'error': 'Username already exists'}), 409
    
    try:
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
            'success': True,
            'message': 'User created successfully',
            'user_id': user_id
        })
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Not authorized'}), 401
    
    data = request.get_json()
    conn = get_db_connection()
    
    try:
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
        
        return jsonify({'success': True, 'message': 'User updated successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Not authorized'}), 401
    
    # Don't allow deleting admin users
    conn = get_db_connection()
    user = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    
    if user['role'] == 'admin':
        conn.close()
        return jsonify({'error': 'Cannot delete admin users'}), 403
    
    try:
        # Remove assignments and related data
        conn.execute('DELETE FROM assignments WHERE user_id = ? OR doctor_id = ?', (user_id, user_id))
        conn.execute('DELETE FROM predictions WHERE user_id = ?', (user_id,))
        conn.execute('DELETE FROM chats WHERE sender_id = ? OR receiver_id = ?', (user_id, user_id))
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/assignments', methods=['POST'])
def assign_user_to_doctor():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Not authorized'}), 401
    
    data = request.get_json()
    user_id = data.get('user_id')
    doctor_id = data.get('doctor_id')
    
    if not user_id or not doctor_id:
        return jsonify({'error': 'User ID and Doctor ID are required'}), 400
    
    conn = get_db_connection()
    
    # Verify that both user and doctor exist
    user_exists = conn.execute('SELECT * FROM users WHERE id = ? AND role = "user"', (user_id,)).fetchone()
    doctor_exists = conn.execute('SELECT * FROM users WHERE id = ? AND role = "doctor"', (doctor_id,)).fetchone()
    
    if not user_exists:
        conn.close()
        return jsonify({'error': 'User not found or invalid role'}), 404
    
    if not doctor_exists:
        conn.close()
        return jsonify({'error': 'Doctor not found or invalid role'}), 404
    
    try:
        # Remove any existing assignment
        conn.execute('DELETE FROM assignments WHERE user_id = ?', (user_id,))
        # Create new assignment
        conn.execute('INSERT INTO assignments (user_id, doctor_id) VALUES (?, ?)', (user_id, doctor_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Assignment created successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/logs', methods=['GET'])
def get_system_logs():
    if 'user_id' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Not authorized'}), 401
    
    # This would typically connect to a logging system
    # For now, we'll return a sample response
    return jsonify({
        'logs': [
            {'timestamp': '2024-01-13 22:30:00', 'level': 'INFO', 'message': 'System started'},
            {'timestamp': '2024-01-13 22:31:00', 'level': 'INFO', 'message': 'Database initialized'},
            {'timestamp': '2024-01-13 22:32:00', 'level': 'INFO', 'message': 'Admin logged in'},
            {'timestamp': '2024-01-13 22:33:00', 'level': 'INFO', 'message': 'New user created: user1'},
        ]
    })
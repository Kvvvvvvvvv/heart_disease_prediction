from flask import Blueprint, request, jsonify, session
import sqlite3
from datetime import datetime

chat_bp = Blueprint('chat', __name__)

def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

@chat_bp.route('/send', methods=['POST'])
def send_message():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        data = request.get_json()
        sender_id = session['user_id']
        receiver_id = data.get('receiver_id')
        message = data.get('message')
        
        if not receiver_id or not message:
            return jsonify({
                'status': 'error', 
                'message': 'Receiver ID and message are required',
                'data': {}
            }), 400
        
        # Check if sender and receiver exist and are valid for chatting
        conn = get_db_connection()
        sender = conn.execute('SELECT id, role FROM users WHERE id = ?', (sender_id,)).fetchone()
        receiver = conn.execute('SELECT id, role FROM users WHERE id = ?', (receiver_id,)).fetchone()
        
        if not sender or not receiver:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'Sender or receiver not found',
                'data': {}
            }), 404
        
        # Verify that the chat is allowed between these users
        # For simplicity, we allow chat between users and their assigned doctor
        # Or between any users with appropriate roles
        is_valid_chat = False
        
        # Check if it's a user talking to their assigned doctor
        if sender['role'] == 'user' and receiver['role'] == 'doctor':
            assignment = conn.execute('SELECT * FROM assignments WHERE user_id = ? AND doctor_id = ?', 
                                      (sender_id, receiver_id)).fetchone()
            if assignment:
                is_valid_chat = True
        
        # Check if it's a doctor talking to one of their assigned users
        elif sender['role'] == 'doctor' and receiver['role'] == 'user':
            assignment = conn.execute('SELECT * FROM assignments WHERE user_id = ? AND doctor_id = ?', 
                                      (receiver_id, sender_id)).fetchone()
            if assignment:
                is_valid_chat = True
        
        # Admins can talk to anyone
        elif sender['role'] == 'admin':
            is_valid_chat = True
        
        if not is_valid_chat:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'Invalid chat relationship',
                'data': {}
            }), 403
        
        # Insert the message
        conn.execute('INSERT INTO chats (sender_id, receiver_id, message) VALUES (?, ?, ?)',
                     (sender_id, receiver_id, message))
        conn.commit()
        
        # Get the inserted message for response
        new_message = conn.execute('''
            SELECT c.*, u.username as sender_name
            FROM chats c
            JOIN users u ON c.sender_id = u.id
            WHERE c.sender_id = ? AND c.receiver_id = ? AND c.message = ?
            ORDER BY c.timestamp DESC
            LIMIT 1
        ''', (sender_id, receiver_id, message)).fetchone()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Message sent successfully',
            'data': {
                'message': dict(new_message)
            }
        })
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@chat_bp.route('/messages/<int:receiver_id>', methods=['GET'])
def get_messages(receiver_id):
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        user_id = session['user_id']
        
        # Verify that the chat is allowed between these users
        conn = get_db_connection()
        sender_role = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
        receiver_role = conn.execute('SELECT role FROM users WHERE id = ?', (receiver_id,)).fetchone()
        
        if not sender_role or not receiver_role:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'Invalid users',
                'data': {}
            }), 404
        
        is_valid_chat = False
        
        # Check if it's a user talking to their assigned doctor
        if sender_role['role'] == 'user' and receiver_role['role'] == 'doctor':
            assignment = conn.execute('SELECT * FROM assignments WHERE user_id = ? AND doctor_id = ?', 
                                      (user_id, receiver_id)).fetchone()
            if assignment:
                is_valid_chat = True
        
        # Check if it's a doctor talking to one of their assigned users
        elif sender_role['role'] == 'doctor' and receiver_role['role'] == 'user':
            assignment = conn.execute('SELECT * FROM assignments WHERE user_id = ? AND doctor_id = ?', 
                                      (receiver_id, user_id)).fetchone()
            if assignment:
                is_valid_chat = True
        
        # Admins can talk to anyone
        elif sender_role['role'] == 'admin':
            is_valid_chat = True
        
        if not is_valid_chat:
            conn.close()
            return jsonify({
                'status': 'error', 
                'message': 'Invalid chat relationship',
                'data': {}
            }), 403
        
        # Get messages between these users
        messages = conn.execute('''
            SELECT c.*, u.username as sender_name
            FROM chats c
            JOIN users u ON c.sender_id = u.id
            WHERE (c.sender_id = ? AND c.receiver_id = ?) OR (c.sender_id = ? AND c.receiver_id = ?)
            ORDER BY c.timestamp ASC
        ''', (user_id, receiver_id, receiver_id, user_id)).fetchall()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Messages retrieved successfully',
            'data': [dict(msg) for msg in messages]
        })
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@chat_bp.route('/conversations', methods=['GET'])
def get_conversations():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        user_id = session['user_id']
        
        conn = get_db_connection()
        # Get all conversations this user is part of
        conversations = conn.execute('''
            SELECT DISTINCT 
                CASE 
                    WHEN c.sender_id = ? THEN c.receiver_id 
                    ELSE c.sender_id 
                END as other_user_id,
                u.username as other_username,
                u.role as other_role,
                MAX(c.timestamp) as last_message_time,
                c.message as last_message
            FROM chats c
            JOIN users u ON 
                CASE 
                    WHEN c.sender_id = ? THEN u.id = c.receiver_id 
                    ELSE u.id = c.sender_id 
                END
            WHERE c.sender_id = ? OR c.receiver_id = ?
            GROUP BY other_user_id
            ORDER BY last_message_time DESC
        ''', (user_id, user_id, user_id, user_id)).fetchall()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Conversations retrieved successfully',
            'data': [dict(conv) for conv in conversations]
        })
    except Exception as e:
        conn.close()
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@chat_bp.route('/typing', methods=['POST'])
def typing_indicator():
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        data = request.get_json()
        receiver_id = data.get('receiver_id')
        is_typing = data.get('is_typing', False)
        
        if not receiver_id:
            return jsonify({
                'status': 'error', 
                'message': 'Receiver ID is required',
                'data': {}
            }), 400
        
        # In a real implementation, this would broadcast the typing status to the receiver
        # For now, we'll just return success
        return jsonify({
            'status': 'success',
            'message': f'Typing status updated for receiver {receiver_id}',
            'data': {}
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@chat_bp.route('/mark_delivered/<int:message_id>', methods=['POST'])
def mark_message_delivered(message_id):
    try:
        if 'user_id' not in session:
            return jsonify({
                'status': 'error', 
                'message': 'Not authenticated',
                'data': {}
            }), 401
        
        # In a real implementation, this would update the message status in the database
        # For now, we'll just return success
        return jsonify({
            'status': 'success',
            'message': 'Message delivery status updated',
            'data': {
                'message_id': message_id,
                'status': 'delivered'
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500

@chat_bp.route('/admin/logs', methods=['GET'])
def get_chat_logs():
    try:
        if 'user_id' not in session or session.get('role') != 'admin':
            return jsonify({
                'status': 'error', 
                'message': 'Not authorized',
                'data': {}
            }), 401
        
        # Admin endpoint to view all chat logs (read-only)
        conn = get_db_connection()
        chat_logs = conn.execute('''
            SELECT c.*, s.username as sender_name, r.username as receiver_name
            FROM chats c
            JOIN users s ON c.sender_id = s.id
            JOIN users r ON c.receiver_id = r.id
            ORDER BY c.timestamp DESC
            LIMIT 100
        ''').fetchall()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Chat logs retrieved successfully',
            'data': [dict(log) for log in chat_logs]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'data': {}
        }), 500
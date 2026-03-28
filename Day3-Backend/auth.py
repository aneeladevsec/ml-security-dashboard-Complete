from functools import wraps
from flask import request, jsonify
import jwt
import datetime
from database import db

SECRET_KEY = 'your-secret-key-change-in-production'

def generate_token(user_id, username):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    """Decorator for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Add user info to request
        request.user_id = payload['user_id']
        request.username = payload['username']
        
        return f(*args, **kwargs)
    
    return decorated_function

def register_user(username, email, password):
    """Register new user"""
    # Simple validation
    if len(password) < 6:
        return {'success': False, 'error': 'Password must be at least 6 characters'}
    
    result = db.add_user(username, email, password)
    return result

def login_user(username, password):
    """Login user"""
    user = db.get_user(username)
    
    if not user:
        return {'success': False, 'error': 'User not found'}
    
    # In production, use bcrypt to check hashed password
    if user['password'] != password:
        return {'success': False, 'error': 'Invalid password'}
    
    token = generate_token(user['id'], user['username'])
    
    return {
        'success': True,
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }
    }

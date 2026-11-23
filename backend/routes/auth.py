"""
SpeechBloom AI - Authentication Routes
"""
from flask import Blueprint, request, jsonify, session
from backend.models.user import User
from database import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    role = data.get('role', 'parent').strip().lower()

    if not email or not password or not name:
        return jsonify({'success': False, 'message': 'Name, email, and password are required.'}), 400

    if role not in ['parent', 'therapist']:
        role = 'parent'

    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'An account with this email already exists.'}), 409

    user = User(email=email, name=name, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    return jsonify({
        'success': True,
        'message': 'Account registered successfully!',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required.'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Invalid email or password.'}), 401

    session['user_id'] = user.id
    return jsonify({
        'success': True,
        'message': 'Logged in successfully!',
        'user': user.to_dict()
    })


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'success': True, 'message': 'Logged out successfully.'})

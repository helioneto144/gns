"""
Simple authentication system for gnS (Genius) Admin Panel
"""

from functools import wraps
from flask import session, request, redirect, url_for, flash
from config import Config
import hashlib
import logging

logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hash"""
    return hash_password(password) == hashed

def login_required(f):
    """Decorator to require login for admin functions"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Acesso negado. Faça login como administrador.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def is_logged_in():
    """Check if user is logged in as admin"""
    return session.get('admin_logged_in', False)

def authenticate_admin(username, password):
    """Authenticate admin credentials"""
    if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        session['admin_username'] = username
        logger.info(f"Admin login successful: {username}")
        return True
    else:
        logger.warning(f"Failed admin login attempt: {username}")
        return False

def logout_admin():
    """Logout admin user"""
    username = session.get('admin_username', 'unknown')
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    logger.info(f"Admin logout: {username}")

def get_admin_info():
    """Get current admin information"""
    if is_logged_in():
        return {
            'username': session.get('admin_username'),
            'logged_in': True
        }
    return {'logged_in': False}

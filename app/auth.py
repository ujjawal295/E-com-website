from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.get_user_by_email(email)
        
        if not user or not user.check_password(password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('home'))
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))
        
        user = User.get_user_by_email(email)
        if user:
            flash('Email address already exists.', 'error')
            return redirect(url_for('auth.register'))
        
        user = User.create_user(email=email, password=password, name=name)
        if user:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.get_user_by_email(email)
        
        if user:
            # In a real application, send password reset email
            flash('If an account exists with this email, you will receive password reset instructions.', 'info')
        else:
            # Don't reveal that the user doesn't exist
            flash('If an account exists with this email, you will receive password reset instructions.', 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html') 
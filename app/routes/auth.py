from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import db, User, Tutor
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('auth.login'))
        
        # Try to find user in both User and Tutor tables
        user = User.query.filter_by(email=email).first()
        tutor = Tutor.query.filter_by(email=email).first()
        
        if tutor:
            if tutor.check_password(password):
                if not tutor.is_verified:
                    flash('Your account is pending verification. Please wait for admin approval.', 'error')
                    return redirect(url_for('auth.login'))
                login_user(tutor)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index'))
        elif user:
            if user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index'))
            
        flash('Invalid email or password.', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        
        if not all([email, name, password, confirm_password]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('auth.register'))
            
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first() or Tutor.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))
            
        user = User(
            email=email,
            name=name,
            phone=phone
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/register/tutor', methods=['GET', 'POST'])
def register_tutor():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone')
        qualification = request.form.get('qualification')
        experience = request.form.get('experience')
        bio = request.form.get('bio')
        
        if not all([email, name, password, confirm_password, qualification, experience]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('auth.register_tutor'))
            
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('auth.register_tutor'))
            
        if User.query.filter_by(email=email).first() or Tutor.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register_tutor'))
            
        tutor = Tutor(
            email=email,
            name=name,
            phone=phone,
            qualification=qualification,
            experience=experience,
            bio=bio,
            is_verified=False  # Tutors need to be verified by admin
        )
        tutor.set_password(password)
        
        db.session.add(tutor)
        db.session.commit()
        
        flash('Registration successful! Please wait for admin verification before logging in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register_tutor.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
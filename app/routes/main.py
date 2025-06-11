from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.models import db, Tutor, Testimonial
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get featured testimonials
    testimonials = Testimonial.query.join(Testimonial.tutor).filter(Tutor.is_verified == True).order_by(Testimonial.created_at.desc()).limit(3).all()
    return render_template('main/index.html', testimonials=testimonials)

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if not all([name, email, message]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('main.contact'))
        
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('main.contact'))
        
    return render_template('main/contact.html')

@main_bp.route('/team')
def team():
    # Get all verified tutors
    tutors = Tutor.query.filter_by(is_verified=True).all()
    return render_template('main/team.html', tutors=tutors) 
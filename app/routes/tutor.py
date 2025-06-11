from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.models import db, Tutor, Subject, Booking, Testimonial
from werkzeug.utils import secure_filename
import os

tutor_bp = Blueprint('tutor', __name__)

@tutor_bp.route('/tutor/dashboard')
@login_required
def dashboard():
    if not isinstance(current_user, Tutor):
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
        
    # Get tutor's bookings
    bookings = Booking.query.filter_by(tutor_id=current_user.id)\
        .order_by(Booking.date.desc())\
        .all()
        
    # Get tutor's testimonials
    testimonials = Testimonial.query.filter_by(tutor_id=current_user.id)\
        .order_by(Testimonial.created_at.desc())\
        .all()
        
    return render_template('tutor/dashboard.html',
                         bookings=bookings,
                         testimonials=testimonials)

@tutor_bp.route('/tutor/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if not isinstance(current_user, Tutor):
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.phone = request.form.get('phone')
        current_user.qualification = request.form.get('qualification')
        current_user.experience = request.form.get('experience')
        current_user.bio = request.form.get('bio')
        
        # Handle profile image upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('app/static/uploads', filename))
                current_user.profile_image = filename
        
        # Handle subjects
        selected_subjects = request.form.getlist('subjects')
        current_user.subjects = Subject.query.filter(Subject.id.in_(selected_subjects)).all()
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('tutor.profile'))
    
    subjects = Subject.query.all()
    return render_template('tutor/profile.html',
                         tutor=current_user,
                         subjects=subjects)

@tutor_bp.route('/tutor/bookings')
@login_required
def bookings():
    if not isinstance(current_user, Tutor):
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
        
    bookings = Booking.query.filter_by(tutor_id=current_user.id)\
        .order_by(Booking.date.desc())\
        .all()
        
    return render_template('tutor/bookings.html', bookings=bookings)

@tutor_bp.route('/tutor/booking/<int:booking_id>/status', methods=['POST'])
@login_required
def update_booking_status(booking_id):
    if not isinstance(current_user, Tutor):
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
        
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.tutor_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('tutor.bookings'))
        
    status = request.form.get('status')
    if status in ['confirmed', 'cancelled']:
        booking.status = status
        db.session.commit()
        flash(f'Booking {status} successfully!', 'success')
    
    return redirect(url_for('tutor.bookings'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.models import db, Booking, Tutor, Subject, Testimonial
from datetime import datetime, timedelta

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/book-session', methods=['GET', 'POST'])
@login_required
def book_session():
    if request.method == 'POST':
        tutor_id = request.form.get('tutor_id')
        subject_id = request.form.get('subject_id')
        date_str = request.form.get('date')
        time_slot = request.form.get('time_slot')
        
        if not all([tutor_id, subject_id, date_str, time_slot]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('booking.book_session'))
            
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date < datetime.now().date():
                flash('Please select a future date.', 'error')
                return redirect(url_for('booking.book_session'))
        except ValueError:
            flash('Invalid date format.', 'error')
            return redirect(url_for('booking.book_session'))
            
        # Check if tutor is available
        existing_booking = Booking.query.filter_by(
            tutor_id=tutor_id,
            date=date,
            time_slot=time_slot,
            status='confirmed'
        ).first()
        
        if existing_booking:
            flash('This time slot is already booked.', 'error')
            return redirect(url_for('booking.book_session'))
            
        booking = Booking(
            user_id=current_user.id,
            tutor_id=tutor_id,
            subject_id=subject_id,
            date=date,
            time_slot=time_slot,
            status='pending'
        )
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking request sent successfully!', 'success')
        return redirect(url_for('booking.my_bookings'))
        
    tutors = Tutor.query.filter_by(is_verified=True).all()
    subjects = Subject.query.all()
    time_slots = generate_time_slots()
    
    return render_template('booking/book_session.html',
                         tutors=tutors,
                         subjects=subjects,
                         time_slots=time_slots)

@booking_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id)\
        .order_by(Booking.booking_date.desc())\
        .all()
    return render_template('booking/my_bookings.html', bookings=bookings)

@booking_bp.route('/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('booking.my_bookings'))
        
    if booking.status == 'confirmed' and booking.booking_date <= datetime.now().date():
        flash('Cannot cancel a confirmed booking for today or past dates.', 'error')
        return redirect(url_for('booking.my_bookings'))
        
    booking.status = 'cancelled'
    db.session.commit()
    
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('booking.my_bookings'))

@booking_bp.route('/booking/<int:booking_id>/review', methods=['POST'])
@login_required
def add_review(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('booking.my_bookings'))
        
    if booking.status != 'confirmed' or booking.date > datetime.now().date():
        flash('Can only review completed sessions.', 'error')
        return redirect(url_for('booking.my_bookings'))
        
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if not rating or not comment:
        flash('Please provide both rating and comment.', 'error')
        return redirect(url_for('booking.my_bookings'))
        
    testimonial = Testimonial(
        user_id=current_user.id,
        tutor_id=booking.tutor_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(testimonial)
    db.session.commit()
    
    flash('Review submitted successfully!', 'success')
    return redirect(url_for('booking.my_bookings'))

@booking_bp.route('/get-tutor-subjects/<int:tutor_id>')
def get_tutor_subjects(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    subjects = [{'id': s.id, 'name': s.name} for s in tutor.subjects]
    return jsonify(subjects)

def generate_time_slots():
    """Generate available time slots from 9 AM to 9 PM"""
    slots = []
    start = datetime.strptime('09:00', '%H:%M')
    end = datetime.strptime('21:00', '%H:%M')
    slot_duration = timedelta(hours=1)
    
    current = start
    while current < end:
        slot = current.strftime('%H:%M')
        slots.append(f'{slot}-{(current + slot_duration).strftime("%H:%M")}')
        current += slot_duration
        
    return slots 
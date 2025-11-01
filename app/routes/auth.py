import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db  # Import db from app
from app.models import User, Patient  # Import models from app.models
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle role-based user login"""
    if request.method == 'GET':
        from flask import get_flashed_messages
        get_flashed_messages()  # Clears success messages from previous login
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validation 1: Empty fields
        if not email or not password:
            flash('Email and password are required.', 'error')
            return render_template('auth/login.html')
        
        # Validation 2: Email format
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            flash('Please enter a valid email address.', 'error')
            return render_template('auth/login.html')
        
        # Check if user exists and password matches
        user = User.query.filter_by(email=email).first()
        if not user or user.password_hash != password:
            flash('Invalid password.', 'error')
            return render_template('auth/login.html')
        
        # SUCCESS: Clear ALL flash messages before redirect
        from flask import get_flashed_messages
        get_flashed_messages()  # Clear existing flash messages
        
        # Role-based redirection
        if '@admin.com' in email.lower():
            flash('Welcome Admin!', 'success')
            return redirect(url_for('admin.dashboard'))
        elif '@trinityhealth.com' in email.lower():
            flash('Welcome Doctor!', 'success')
            return redirect(url_for('doctor.dashboard'))
        else:
            flash('Welcome Patient!', 'success')
            return redirect(url_for('patient.dashboard'))
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle general user registration (e.g., for admins or doctors)"""
    print(f"DB instance in register: {db}")
    print(f"Current app in register: {current_app}")
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Hash password in production
        full_name = request.form.get('full_name')
        role = request.form.get('role')  # 'admin', 'doctor', 'patient'
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('auth/register.html')
        new_user = User(username=username, email=email, password_hash=password, full_name=full_name, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/register/patient', methods=['GET', 'POST'])
def register_patient():
    """Handle patient-specific registration"""
    print(f"DB instance in register_patient: {db}")
    print(f"Current app in register_patient: {current_app}")
    if request.method == 'POST':
        # User fields
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')  # Hash password in production
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        # Patient fields
        blood_group = request.form.get('blood_group')
        address = request.form.get('address')
        emergency_contact = request.form.get('emergency_contact')

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('auth/registerPatient.html')

        # Create User
        new_user = User(
            username=username,
            email=email,
            password_hash=password,  # Simplified; use bcrypt
            full_name=full_name,
            phone=phone,
            dob=datetime.strptime(dob, '%Y-%m-%d') if dob else None,
            gender=gender,
            role='patient'
        )
        db.session.add(new_user)
        db.session.commit()

        # Create Patient
        new_patient = Patient(
            user_id=new_user.user_id,
            blood_group=blood_group,
            address=address,
            emergency_contact=emergency_contact
        )
        db.session.add(new_patient)
        db.session.commit()

        flash('Patient registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/registerPatient.html')

@auth.route('/profile')
def profile():
    """Handle user profile view for all roles"""
    print(f"DB instance in profile: {db}")
    print(f"Current app in profile: {current_app}")
    user = User.query.get(1)  # Replace with actual user ID from session
    if user.role == 'patient':
        return render_template('patient/profile.html', user=user)
    elif user.role == 'doctor':
        return render_template('doctor/profile.html', user=user)
    else:
        return render_template('admin/profile.html', user=user)
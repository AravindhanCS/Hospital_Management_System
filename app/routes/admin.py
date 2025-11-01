from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Patient, Doctor, Department, Appointment, PatientHistory, Blacklist
from sqlalchemy import or_, and_
from datetime import datetime

admin = Blueprint('admin', __name__, template_folder='templates/admin')

@admin.route('/admin/dashboard')
@login_required
def dashboard():
    """Admin Dashboard with stats and initial data"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('auth.login'))
    
    # Stats
    stats = {
        'patients': db.session.query(Patient).count(),
        'doctors': db.session.query(Doctor).count(),
        'appointments': db.session.query(Appointment).count(),
        'blacklisted': db.session.query(Blacklist).count()
    }
    
    # Patients (with pagination)
    page = request.args.get('page', 1, type=int)
    patients = db.session.query(User, Patient).join(Patient, User.id == Patient.user_id).filter(
        User.role == 'patient'
    ).paginate(page=page, per_page=10, error_out=False)
    
    departments = Department.query.all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         patients=patients, 
                         departments=departments)

# PATIENTS CRUD
@admin.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = db.session.query(User, Patient).join(Patient).filter(Patient.patient_id == patient_id).first()
    if patient:
        return jsonify({
            'success': True,
            'data': {
                'full_name': patient.User.full_name,
                'email': patient.User.email,
                'phone': patient.User.phone,
                # ... more fields
            }
        })
    return jsonify({'success': False, 'message': 'Patient not found'}), 404

@admin.route('/api/patients', methods=['POST'])
def create_update_patient():
    data = request.json
    patient_id = data.get('patient_id')
    
    try:
        if patient_id:  # Update
            user = User.query.filter_by(id=data['user_id']).first()
            patient = Patient.query.get(patient_id)
            # Update logic...
            db.session.commit()
            return jsonify({'success': True, 'message': 'Patient updated successfully'})
        else:  # Create
            user = User(
                full_name=data['full_name'],
                email=data['email'],
                password_hash='default_hash',  # Use bcrypt in production
                role='patient',
                is_active=True
            )
            db.session.add(user)
            db.session.flush()  # Get user_id
            
            patient = Patient(
                user_id=user.id,
                blood_group=data.get('blood_group'),
                address=data.get('address'),
                emergency_contact=data.get('emergency_contact')
            )
            db.session.add(patient)
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Patient created successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin.route('/api/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Patient deleted'})
    return jsonify({'success': False}), 404

# DOCTORS CRUD (Similar structure)
@admin.route('/api/doctors', methods=['POST'])
def create_update_doctor():
    # Implementation similar to patients
    pass

@admin.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    # Implementation
    pass

# BLACKLIST
@admin.route('/api/blacklist', methods=['POST'])
def blacklist_doctor():
    data = request.json
    doctor_id = data['doctor_id']
    reason = data['reason']
    
    # Deactivate doctor
    doctor_user = db.session.query(User).join(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    if doctor_user:
        doctor_user.is_active = False
        doctor_user.is_blacklisted = True
        
        blacklist_entry = Blacklist(
            user_id=doctor_user.id,
            reason=reason
        )
        db.session.add(blacklist_entry)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Doctor blacklisted successfully'})
    
    return jsonify({'success': False, 'message': 'Doctor not found'}), 404

# APPOINTMENTS CRUD
@admin.route('/api/appointments', methods=['POST'])
def create_update_appointment():
    # Implementation
    pass

# PATIENT HISTORY CRUD
@admin.route('/api/history', methods=['POST'])
def create_update_history():
    # Implementation
    pass
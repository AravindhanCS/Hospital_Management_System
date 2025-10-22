from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from app import db 

# 1. Users
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    dob = db.Column(db.DateTime)
    gender = db.Column(db.Enum("male", "female", "other", name="gender_enum"))
    role = db.Column(db.Enum("admin", "doctor", "patient", name="role_enum"), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)

    doctor = db.relationship("Doctor", back_populates="user", uselist=False)
    patient = db.relationship("Patient", back_populates="user", uselist=False)

# 2. Departments
class Department(db.Model):
    __tablename__ = "departments"

    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    doctors_registered = db.Column(db.Integer, default=0)

    doctors = db.relationship("Doctor", back_populates="department")

# 3. Doctors
class Doctor(db.Model):
    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.department_id"), nullable=False)
    qualification = db.Column(db.String(255))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())

    user = db.relationship("User", back_populates="doctor")
    department = db.relationship("Department", back_populates="doctors")
    availabilities = db.relationship("DoctorAvailability", back_populates="doctor")
    appointments = db.relationship("Appointment", back_populates="doctor")
    treatments = db.relationship("Treatment", back_populates="doctor")

# 4. Patients
class Patient(db.Model):
    __tablename__ = "patients"

    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    blood_group = db.Column(db.String(10))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=func.now())

    user = db.relationship("User", back_populates="patient")
    appointments = db.relationship("Appointment", back_populates="patient")
    treatments = db.relationship("Treatment", back_populates="patient")
    history = db.relationship("PatientHistory", back_populates="patient")

# 5. Doctor Availability
class DoctorAvailability(db.Model):
    __tablename__ = "doctor_availability"

    slot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())

    doctor = db.relationship("Doctor", back_populates="availabilities")

# 6. Appointments
class Appointment(db.Model):
    __tablename__ = "appointments"

    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    appointment_start = db.Column(db.DateTime, nullable=False)
    appointment_end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum("Booked", "Completed", "Cancelled", name="appointment_status_enum"), nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    doctor = db.relationship("Doctor", back_populates="appointments")
    patient = db.relationship("Patient", back_populates="appointments")
    treatment = db.relationship("Treatment", back_populates="appointment", uselist=False)

# 7. Treatments
class Treatment(db.Model):
    __tablename__ = "treatments"

    treatment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.appointment_id"), unique=True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=func.now())

    appointment = db.relationship("Appointment", back_populates="treatment")
    doctor = db.relationship("Doctor", back_populates="treatments")
    patient = db.relationship("Patient", back_populates="treatments")

# 8. Blacklist
class Blacklist(db.Model):
    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    reason = db.Column(db.Text)
    blacklisted_at = db.Column(db.DateTime, default=func.now())

# 9. Patient History
class PatientHistory(db.Model):
    __tablename__ = "patient_history"

    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.patient_id"), nullable=False)
    hospital_name = db.Column(db.String(255), nullable=False)
    doctor_name = db.Column(db.String(255))
    department = db.Column(db.String(255))
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    treatment_date = db.Column(db.DateTime, nullable=False)
    documents_url = db.Column(db.String(500))  # optional
    created_at = db.Column(db.DateTime, default=func.now())

    patient = db.relationship("Patient", back_populates="history")

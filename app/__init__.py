import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, '..', 'data', 'hms.db')
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from app.models import User, Department, Doctor, Patient, DoctorAvailability, Appointment, Treatment, Blacklist, PatientHistory
        db.create_all()

    # from app.routes import auth, admin, doctor, patient, common
    from app.routes import auth, admin
    app.register_blueprint(auth)
    app.register_blueprint(admin)
    # app.register_blueprint(doctor)
    # app.register_blueprint(patient)
    # app.register_blueprint(common)

    return app
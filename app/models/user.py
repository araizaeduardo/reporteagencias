from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin', 'user'
    is_active = db.Column(db.Boolean, default=False)  # Cambiado a False por defecto
    email_confirmed = db.Column(db.Boolean, default=False)  # Nuevo campo para verificación
    email_confirm_date = db.Column(db.DateTime, nullable=True)  # Fecha de verificación
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con la agencia (si el usuario es un agente)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=True)
    agency = db.relationship('Agency', back_populates='agents')
    
    def __init__(self, username, email, password, role='user', agency_id=None, is_active=False, email_confirmed=False):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role
        self.agency_id = agency_id
        self.is_active = is_active
        self.email_confirmed = email_confirmed
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def generate_confirmation_token(self):
        """Genera un token para confirmar el correo electrónico"""
        serializer = Serializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt='email-confirm')
    
    @staticmethod
    def verify_confirmation_token(token, expiration=3600):
        """Verifica el token de confirmación"""
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='email-confirm', max_age=expiration)
            return email
        except:
            return None
    
    def confirm_email(self):
        """Confirma el correo electrónico del usuario"""
        self.email_confirmed = True
        self.is_active = True
        self.email_confirm_date = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

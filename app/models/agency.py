from app import db
from datetime import datetime

class Agency(db.Model):
    __tablename__ = 'agencies'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    agents = db.relationship('User', back_populates='agency')
    sales = db.relationship('Sale', back_populates='agency')
    
    def __init__(self, code, name, address=None, phone=None, email=None):
        self.code = code
        self.name = name
        self.address = address
        self.phone = phone
        self.email = email
    
    def __repr__(self):
        return f'<Agency {self.code}: {self.name}>'

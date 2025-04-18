from app import db
from datetime import datetime

class Airline(db.Model):
    __tablename__ = 'airlines'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    logo_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    contracts = db.relationship('Contract', back_populates='airline', cascade='all, delete-orphan')
    
    def __init__(self, code, name, description=None, logo_path=None):
        self.code = code
        self.name = name
        self.description = description
        self.logo_path = logo_path
    
    def __repr__(self):
        return f'<Airline {self.code}: {self.name}>'

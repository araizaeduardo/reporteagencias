from app import db
from datetime import datetime

class Contract(db.Model):
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    file_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)
    airline = db.relationship('Airline', back_populates='contracts')
    
    # Documentos adjuntos
    documents = db.relationship('ContractDocument', back_populates='contract', cascade='all, delete-orphan')
    
    def __init__(self, title, description, start_date, end_date, airline_id, file_path=None):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.airline_id = airline_id
        self.file_path = file_path
    
    def __repr__(self):
        return f'<Contract {self.title}>'

class ContractDocument(db.Model):
    __tablename__ = 'contract_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con el contrato
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    contract = db.relationship('Contract', back_populates='documents')
    
    def __init__(self, name, file_path, contract_id, description=None):
        self.name = name
        self.file_path = file_path
        self.contract_id = contract_id
        self.description = description
    
    def __repr__(self):
        return f'<ContractDocument {self.name}>'

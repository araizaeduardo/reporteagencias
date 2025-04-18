from app import db
from datetime import datetime

class Sale(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(20), nullable=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    sale_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    commission = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    payment_method = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    agency = db.relationship('Agency', back_populates='sales')
    
    # Usuario que registró la venta (agente)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User')
    
    # Aerolínea relacionada con la venta
    airline_id = db.Column(db.Integer, db.ForeignKey('airlines.id'), nullable=False)
    airline = db.relationship('Airline')
    
    def __init__(self, client_name, client_email, origin, destination, sale_date, amount, 
                 agency_id, user_id, airline_id, commission, status='pending', 
                 payment_method='credit_card', ticket_number=None, notes=None):
        self.client_name = client_name
        self.client_email = client_email
        self.ticket_number = ticket_number
        self.origin = origin
        self.destination = destination
        self.sale_date = sale_date
        self.amount = amount
        self.commission = commission
        self.status = status
        self.payment_method = payment_method
        self.notes = notes
        self.agency_id = agency_id
        self.user_id = user_id
        self.airline_id = airline_id
    
    def __repr__(self):
        return f'<Sale #{self.id}: {self.client_name}>'

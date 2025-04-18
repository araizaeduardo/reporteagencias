from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField, DateField, HiddenField
from wtforms.validators import DataRequired, Email, Optional, NumberRange

class SaleForm(FlaskForm):
    client_name = StringField('Nombre del Cliente', validators=[DataRequired()])
    client_email = StringField('Email del Cliente', validators=[DataRequired(), Email()])
    airline_id = SelectField('Aerolínea', validators=[DataRequired()], coerce=int)
    sale_date = DateField('Fecha de Venta', validators=[DataRequired()])
    ticket_number = StringField('Número de Boleto', validators=[Optional()])
    amount = FloatField('Monto', validators=[DataRequired(), NumberRange(min=0.01)])
    commission = FloatField('Comisión', validators=[DataRequired(), NumberRange(min=0)])
    origin = StringField('Origen', validators=[DataRequired()])
    destination = StringField('Destino', validators=[DataRequired()])
    notes = TextAreaField('Notas', validators=[Optional()])
    status = SelectField('Estado', validators=[DataRequired()], 
                        choices=[
                            ('pending', 'Pendiente'),
                            ('completed', 'Completada'),
                            ('cancelled', 'Cancelada')
                        ])
    payment_method = SelectField('Método de Pago', validators=[DataRequired()],
                                choices=[
                                    ('credit_card', 'Tarjeta de Crédito'),
                                    ('debit_card', 'Tarjeta de Débito'),
                                    ('cash', 'Efectivo'),
                                    ('transfer', 'Transferencia Bancaria')
                                ])

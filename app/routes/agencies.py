from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from app import db
from app.models.agency import Agency
from app.models.airline import Airline
from app.models.contract import Contract
from app.models.sale import Sale
from app.forms.sale import SaleForm
from datetime import datetime

agencies = Blueprint('agencies', __name__, url_prefix='/agencies')

@agencies.route('/')
@login_required
def index():
    """Dashboard para agencias de viajes"""
    # Si el usuario es un agente, mostrar solo su agencia
    if not current_user.is_admin() and current_user.agency_id:
        agency = Agency.query.get_or_404(current_user.agency_id)
        return render_template('agencies/dashboard.html', agency=agency)
    
    # Si es administrador, mostrar todas las agencias
    if current_user.is_admin():
        agencies_list = Agency.query.all()
        return render_template('agencies/index.html', agencies=agencies_list)
    
    # Si es un usuario sin agencia asignada
    flash('No tienes una agencia asignada', 'warning')
    return redirect(url_for('main.dashboard'))

@agencies.route('/<int:id>/view')
@login_required
def view_agency(id):
    """Ver detalles de una agencia"""
    agency = Agency.query.get_or_404(id)
    
    # Verificar permisos: solo administradores o agentes de la misma agencia
    if not current_user.is_admin() and current_user.agency_id != id:
        abort(403)  # Forbidden
    
    return render_template('agencies/view.html', agency=agency)

@agencies.route('/contracts')
@login_required
def contracts():
    """Búsqueda de contratos para agencias"""
    airlines = Airline.query.all()
    
    # Obtener parámetros de búsqueda
    airline_id = request.args.get('airline_id', type=int)
    keyword = request.args.get('keyword', '')
    
    # Construir consulta base
    query = Contract.query
    
    # Aplicar filtros si se proporcionan
    if airline_id:
        query = query.filter_by(airline_id=airline_id)
    
    if keyword:
        query = query.filter(
            (Contract.title.ilike(f'%{keyword}%')) | 
            (Contract.description.ilike(f'%{keyword}%'))
        )
    
    # Obtener resultados
    contracts = query.all()
    
    return render_template(
        'agencies/contracts.html',
        contracts=contracts,
        airlines=airlines,
        selected_airline=airline_id,
        keyword=keyword
    )

@agencies.route('/contracts/<int:id>')
@login_required
def view_contract(id):
    """Ver detalles de un contrato"""
    contract = Contract.query.get_or_404(id)
    return render_template('agencies/contract_details.html', contract=contract)

# Rutas para ventas (para futuras implementaciones)
@agencies.route('/sales')
@login_required
def sales():
    """Lista de ventas de la agencia"""
    # Obtener parámetros de filtro
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    airline_id = request.args.get('airline_id', type=int)
    
    # Construir consulta base
    query = Sale.query
    
    # Si el usuario es un agente, mostrar solo las ventas de su agencia
    if not current_user.is_admin() and current_user.agency_id:
        query = query.filter_by(agency_id=current_user.agency_id)
    # Si no es administrador y no tiene agencia, redirigir
    elif not current_user.is_admin():
        flash('No tienes una agencia asignada', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Aplicar filtros adicionales
    if start_date:
        query = query.filter(Sale.sale_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    
    if end_date:
        query = query.filter(Sale.sale_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    if airline_id:
        query = query.filter_by(airline_id=airline_id)
    
    # Obtener resultados
    sales_list = query.all()
    
    # Calcular totales
    total_sales = sum(sale.amount for sale in sales_list) if sales_list else 0
    total_commissions = sum(sale.commission for sale in sales_list) if sales_list else 0
    
    # Obtener aerolíneas para el filtro
    airlines = Airline.query.all()
    
    return render_template(
        'agencies/sales/index.html', 
        sales=sales_list,
        airlines=airlines,
        total_sales=total_sales,
        total_commissions=total_commissions
    )

@agencies.route('/sales/new', methods=['GET', 'POST'])
@login_required
def new_sale():
    """Registrar nueva venta (para futuras implementaciones con API)"""
    # Verificar que el usuario tenga una agencia asignada
    if not current_user.agency_id:
        flash('No tienes una agencia asignada', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Crear formulario
    form = SaleForm()
    
    # Cargar opciones de aerolíneas
    airlines = Airline.query.all()
    form.airline_id.choices = [(a.id, a.name) for a in airlines]
    
    # Establecer fecha actual por defecto
    if not form.sale_date.data:
        form.sale_date.data = datetime.now().date()
    
    if form.validate_on_submit():
        # Crear nueva venta
        new_sale = Sale(
            client_name=form.client_name.data,
            client_email=form.client_email.data,
            ticket_number=form.ticket_number.data,
            origin=form.origin.data,
            destination=form.destination.data,
            sale_date=form.sale_date.data,
            amount=form.amount.data,
            commission=form.commission.data,
            status=form.status.data,
            payment_method=form.payment_method.data,
            notes=form.notes.data,
            agency_id=current_user.agency_id,
            user_id=current_user.id,
            airline_id=form.airline_id.data
        )
        
        db.session.add(new_sale)
        db.session.commit()
        
        flash('Venta registrada correctamente', 'success')
        return redirect(url_for('agencies.sales'))
    
    return render_template('agencies/sales/new.html', form=form, airlines=airlines)

@agencies.route('/sales/<int:id>')
@login_required
def view_sale(id):
    """Ver detalles de una venta"""
    sale = Sale.query.get_or_404(id)
    
    # Verificar permisos: solo administradores o agentes de la misma agencia
    if not current_user.is_admin() and current_user.agency_id != sale.agency_id:
        abort(403)  # Forbidden
    
    return render_template('agencies/sales/view.html', sale=sale)

@agencies.route('/sales/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_sale(id):
    """Editar una venta existente"""
    sale = Sale.query.get_or_404(id)
    
    # Verificar permisos: solo administradores o agentes de la misma agencia
    if not current_user.is_admin() and current_user.agency_id != sale.agency_id:
        abort(403)  # Forbidden
    
    # Crear formulario y cargar datos actuales
    form = SaleForm(obj=sale)
    
    # Cargar opciones de aerolíneas
    airlines = Airline.query.all()
    form.airline_id.choices = [(a.id, a.name) for a in airlines]
    
    if form.validate_on_submit():
        # Actualizar datos de la venta
        form.populate_obj(sale)
        db.session.commit()
        
        flash('Venta actualizada correctamente', 'success')
        return redirect(url_for('agencies.view_sale', id=sale.id))
    
    return render_template('agencies/sales/edit.html', form=form, sale=sale)

@agencies.route('/sales/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_sale(id):
    """Cancelar una venta"""
    sale = Sale.query.get_or_404(id)
    
    # Verificar permisos: solo administradores o agentes de la misma agencia
    if not current_user.is_admin() and current_user.agency_id != sale.agency_id:
        abort(403)  # Forbidden
    
    # Verificar que la venta no esté ya cancelada
    if sale.status == 'cancelled':
        flash('Esta venta ya ha sido cancelada', 'warning')
    else:
        sale.status = 'cancelled'
        db.session.commit()
        flash('Venta cancelada correctamente', 'success')
    
    return redirect(url_for('agencies.view_sale', id=sale.id))

@agencies.route('/reports')
@login_required
def reports():
    """Reportes de ventas (para futuras implementaciones)"""
    # Verificar permisos
    if not current_user.is_admin() and not current_user.agency_id:
        flash('No tienes una agencia asignada', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Aquí se implementaría la lógica para generar reportes
    
    return render_template('agencies/reports.html')

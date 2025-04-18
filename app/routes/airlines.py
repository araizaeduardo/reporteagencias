from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_required, current_user
from app import db
from app.models.airline import Airline
from app.models.contract import Contract, ContractDocument
from werkzeug.utils import secure_filename
import os
from datetime import datetime

airlines = Blueprint('airlines', __name__, url_prefix='/airlines')

# Función auxiliar para guardar archivos
def save_file(file, folder='uploads'):
    if file:
        filename = secure_filename(file.filename)
        # Generar nombre único para evitar colisiones
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        
        # Crear ruta para guardar el archivo físicamente
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder, unique_filename)
        
        # Asegurarse de que el directorio existe
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Guardar el archivo
        file.save(file_path)
        
        # Devolver ruta para URL usando barras normales (/) en lugar de barras invertidas (\)
        return f"{folder}/{unique_filename}".replace('\\', '/')
    return None

@airlines.route('/')
@login_required
def index():
    """Lista de aerolíneas"""
    airlines_list = Airline.query.all()
    return render_template('airlines/index.html', airlines=airlines_list)

@airlines.route('/new', methods=['GET', 'POST'])
@login_required
def new_airline():
    """Crear nueva aerolínea"""
    # Verificar si el usuario es administrador
    if not current_user.is_admin():
        abort(403)  # Forbidden
    
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        description = request.form.get('description')
        logo = request.files.get('logo')
        
        # Validar si el código de aerolínea ya existe
        if Airline.query.filter_by(code=code).first():
            flash('El código de aerolínea ya está en uso', 'danger')
            return render_template('airlines/new.html')
        
        # Guardar logo si se proporciona
        logo_path = None
        if logo and logo.filename:
            logo_path = save_file(logo, 'uploads/airlines')
        
        # Crear nueva aerolínea
        new_airline = Airline(
            code=code,
            name=name,
            description=description,
            logo_path=logo_path
        )
        
        db.session.add(new_airline)
        db.session.commit()
        
        flash('Aerolínea creada correctamente', 'success')
        return redirect(url_for('airlines.index'))
    
    return render_template('airlines/new.html')

@airlines.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_airline(id):
    """Editar aerolínea"""
    # Verificar si el usuario es administrador
    if not current_user.is_admin():
        abort(403)  # Forbidden
    
    airline = Airline.query.get_or_404(id)
    
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        description = request.form.get('description')
        logo = request.files.get('logo')
        
        # Validar si el nuevo código ya está en uso por otra aerolínea
        existing_airline = Airline.query.filter_by(code=code).first()
        if existing_airline and existing_airline.id != id:
            flash('El código de aerolínea ya está en uso', 'danger')
            return render_template('airlines/edit.html', airline=airline)
        
        # Actualizar aerolínea
        airline.code = code
        airline.name = name
        airline.description = description
        
        # Actualizar logo si se proporciona uno nuevo
        if logo and logo.filename:
            airline.logo_path = save_file(logo, 'uploads/airlines')
        
        db.session.commit()
        
        flash('Aerolínea actualizada correctamente', 'success')
        return redirect(url_for('airlines.index'))
    
    return render_template('airlines/edit.html', airline=airline)

@airlines.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_airline(id):
    """Eliminar aerolínea"""
    # Verificar si el usuario es administrador
    if not current_user.is_admin():
        abort(403)  # Forbidden
    
    airline = Airline.query.get_or_404(id)
    
    # Verificar si hay contratos asociados a esta aerolínea
    if airline.contracts:
        flash('No se puede eliminar la aerolínea porque tiene contratos asociados', 'danger')
        return redirect(url_for('airlines.index'))
    
    db.session.delete(airline)
    db.session.commit()
    
    flash('Aerolínea eliminada correctamente', 'success')
    return redirect(url_for('airlines.index'))

@airlines.route('/<int:id>/view')
@login_required
def view_airline(id):
    """Ver detalles de aerolínea y sus contratos"""
    airline = Airline.query.get_or_404(id)
    contracts = Contract.query.filter_by(airline_id=id).all()
    
    return render_template('airlines/view.html', airline=airline, contracts=contracts)

# Rutas para contratos
@airlines.route('/<int:airline_id>/contracts/new', methods=['GET', 'POST'])
@login_required
def new_contract(airline_id):
    """Crear nuevo contrato para una aerolínea"""
    # Verificar si el usuario es administrador
    if not current_user.is_admin():
        abort(403)  # Forbidden
    
    airline = Airline.query.get_or_404(airline_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        contract_file = request.files.get('contract_file')
        
        # Guardar archivo del contrato si se proporciona
        file_path = None
        if contract_file and contract_file.filename:
            file_path = save_file(contract_file, 'uploads/contracts')
        
        # Crear nuevo contrato
        new_contract = Contract(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            airline_id=airline_id,
            file_path=file_path
        )
        
        db.session.add(new_contract)
        db.session.commit()
        
        flash('Contrato creado correctamente', 'success')
        return redirect(url_for('airlines.view_airline', id=airline_id))
    
    return render_template('airlines/contracts/new.html', airline=airline)

@airlines.route('/contracts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_contract(id):
    """Editar contrato"""
    # Verificar si el usuario es administrador
    if not current_user.is_admin():
        abort(403)  # Forbidden
    
    contract = Contract.query.get_or_404(id)
    airline = Airline.query.get_or_404(contract.airline_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
        contract_file = request.files.get('contract_file')
        
        # Actualizar contrato
        contract.title = title
        contract.description = description
        contract.start_date = start_date
        contract.end_date = end_date
        
        # Actualizar archivo del contrato si se proporciona uno nuevo
        if contract_file and contract_file.filename:
            contract.file_path = save_file(contract_file, 'uploads/contracts')
        
        db.session.commit()
        
        flash('Contrato actualizado correctamente', 'success')
        return redirect(url_for('airlines.view_airline', id=contract.airline_id))
    
    return render_template('airlines/contracts/edit.html', contract=contract, airline=airline)

@airlines.route('/contracts/<int:id>/delete', methods=['POST'])
@login_required
def delete_contract(id):
    """Eliminar contrato"""
    # Verificar si el usuario es administrador
    if not current_user.is_admin():
        abort(403)  # Forbidden
    
    contract = Contract.query.get_or_404(id)
    airline_id = contract.airline_id
    
    db.session.delete(contract)
    db.session.commit()
    
    flash('Contrato eliminado correctamente', 'success')
    return redirect(url_for('airlines.view_airline', id=airline_id))

@airlines.route('/contracts/<int:id>/view')
@login_required
def view_contract(id):
    """Ver detalles de un contrato y sus documentos"""
    contract = Contract.query.get_or_404(id)
    documents = ContractDocument.query.filter_by(contract_id=id).all()
    
    return render_template('airlines/contracts/view.html', contract=contract, documents=documents)

# Rutas para documentos de contratos
@airlines.route('/contracts/<int:contract_id>/documents/new', methods=['GET', 'POST'])
@login_required
def new_document(contract_id):
    """Añadir nuevo documento a un contrato"""
    # Verificar si el usuario es administrador
    if not current_user.is_admin():
        abort(403)  # Forbidden
    
    contract = Contract.query.get_or_404(contract_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        document_file = request.files.get('document_file')
        
        # Validar que se proporciona un archivo
        if not document_file or not document_file.filename:
            flash('Debe proporcionar un archivo', 'danger')
            return render_template('airlines/contracts/documents/new.html', contract=contract)
        
        # Guardar archivo del documento
        file_path = save_file(document_file, 'uploads/documents')
        
        # Crear nuevo documento
        new_document = ContractDocument(
            name=name,
            description=description,
            file_path=file_path,
            contract_id=contract_id
        )
        
        db.session.add(new_document)
        db.session.commit()
        
        flash('Documento añadido correctamente', 'success')
        return redirect(url_for('airlines.view_contract', id=contract_id))
    
    return render_template('airlines/contracts/documents/new.html', contract=contract)

@airlines.route('/documents/<int:id>/delete', methods=['POST'])
@login_required
def delete_document(id):
    """Eliminar documento"""
    # Verificar si el usuario es administrador
    if not current_user.is_admin():
        abort(403)  # Forbidden
    
    document = ContractDocument.query.get_or_404(id)
    contract_id = document.contract_id
    
    db.session.delete(document)
    db.session.commit()
    
    flash('Documento eliminado correctamente', 'success')
    return redirect(url_for('airlines.view_contract', id=contract_id))

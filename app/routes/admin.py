from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.agency import Agency
from werkzeug.security import generate_password_hash

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Middleware para verificar si el usuario es administrador
@admin.before_request
def check_admin():
    if not current_user.is_authenticated:
        flash('Debe iniciar sesión para acceder a esta página', 'danger')
        return redirect(url_for('auth.login'))
    
    if not current_user.is_admin():
        flash('No tiene permisos para acceder a esta sección. Se requiere rol de administrador.', 'danger')
        return redirect(url_for('main.dashboard'))

@admin.route('/')
@login_required
def index():
    """Panel de administración principal"""
    return render_template('admin/index.html')

# Gestión de Usuarios
@admin.route('/users')
@login_required
def users():
    """Lista de usuarios"""
    users_list = User.query.all()
    return render_template('admin/users/index.html', users=users_list)

@admin.route('/users/new', methods=['GET', 'POST'])
@login_required
def new_user():
    """Crear nuevo usuario"""
    agencies = Agency.query.all()
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        agency_id = request.form.get('agency_id')
        
        # Validar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'danger')
            return render_template('admin/users/new.html', agencies=agencies)
        
        if User.query.filter_by(email=email).first():
            flash('El correo electrónico ya está en uso', 'danger')
            return render_template('admin/users/new.html', agencies=agencies)
        
        # Convertir agency_id a None si es un string vacío
        if agency_id == '':
            agency_id = None
        else:
            agency_id = int(agency_id)
        
        # Crear nuevo usuario
        new_user = User(
            username=username,
            email=email,
            password=password,
            role=role,
            agency_id=agency_id
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Usuario creado correctamente', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/new.html', agencies=agencies)

@admin.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """Editar usuario"""
    user = User.query.get_or_404(id)
    agencies = Agency.query.all()
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        agency_id = request.form.get('agency_id')
        is_active = 'is_active' in request.form
        
        # Validar si el nuevo nombre de usuario ya está en uso por otro usuario
        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.id != id:
            flash('El nombre de usuario ya está en uso', 'danger')
            return render_template('admin/users/edit.html', user=user, agencies=agencies)
        
        # Validar si el nuevo correo electrónico ya está en uso por otro usuario
        existing_email = User.query.filter_by(email=email).first()
        if existing_email and existing_email.id != id:
            flash('El correo electrónico ya está en uso', 'danger')
            return render_template('admin/users/edit.html', user=user, agencies=agencies)
        
        # Actualizar usuario
        user.username = username
        user.email = email
        user.role = role
        user.is_active = is_active
        
        # Convertir agency_id a None si es un string vacío
        if agency_id == '':
            user.agency_id = None
        else:
            user.agency_id = int(agency_id)
        
        # Actualizar contraseña si se proporciona una nueva
        password = request.form.get('password')
        if password:
            user.set_password(password)
        
        db.session.commit()
        
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/edit.html', user=user, agencies=agencies)

@admin.route('/users/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    """Eliminar usuario"""
    user = User.query.get_or_404(id)
    
    # No permitir eliminar el propio usuario
    if user.id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('admin.users'))

# Gestión de Agencias
@admin.route('/agencies')
@login_required
def agencies():
    """Lista de agencias"""
    agencies_list = Agency.query.all()
    return render_template('admin/agencies/index.html', agencies=agencies_list)

@admin.route('/agencies/new', methods=['GET', 'POST'])
@login_required
def new_agency():
    """Crear nueva agencia"""
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        
        # Validar si el código de agencia ya existe
        if Agency.query.filter_by(code=code).first():
            flash('El código de agencia ya está en uso', 'danger')
            return render_template('admin/agencies/new.html')
        
        # Crear nueva agencia
        new_agency = Agency(
            code=code,
            name=name,
            address=address,
            phone=phone,
            email=email
        )
        
        db.session.add(new_agency)
        db.session.commit()
        
        flash('Agencia creada correctamente', 'success')
        return redirect(url_for('admin.agencies'))
    
    return render_template('admin/agencies/new.html')

@admin.route('/agencies/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_agency(id):
    """Editar agencia"""
    agency = Agency.query.get_or_404(id)
    
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        email = request.form.get('email')
        
        # Validar si el nuevo código ya está en uso por otra agencia
        existing_agency = Agency.query.filter_by(code=code).first()
        if existing_agency and existing_agency.id != id:
            flash('El código de agencia ya está en uso', 'danger')
            return render_template('admin/agencies/edit.html', agency=agency)
        
        # Actualizar agencia
        agency.code = code
        agency.name = name
        agency.address = address
        agency.phone = phone
        agency.email = email
        
        db.session.commit()
        
        flash('Agencia actualizada correctamente', 'success')
        return redirect(url_for('admin.agencies'))
    
    return render_template('admin/agencies/edit.html', agency=agency)

@admin.route('/agencies/<int:id>/delete', methods=['POST'])
@login_required
def delete_agency(id):
    """Eliminar agencia"""
    agency = Agency.query.get_or_404(id)
    
    # Verificar si hay usuarios asociados a esta agencia
    if agency.agents:
        flash('No se puede eliminar la agencia porque tiene usuarios asociados', 'danger')
        return redirect(url_for('admin.agencies'))
    
    db.session.delete(agency)
    db.session.commit()
    
    flash('Agencia eliminada correctamente', 'success')
    return redirect(url_for('admin.agencies'))

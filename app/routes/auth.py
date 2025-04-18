from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash
from datetime import timedelta

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            # Hacer la sesión permanente para que no expire tan rápido
            session.permanent = True
            # Iniciar sesión con remember=True para mantener la sesión activa
            login_user(user, remember=True, duration=timedelta(days=1))
            # Regenerar el ID de sesión para prevenir ataques de fijación de sesión
            session.modified = True
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Perfil de usuario"""
    if request.method == 'POST':
        # Actualizar información del perfil
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        
        # Verificar si se está cambiando la contraseña
        password = request.form.get('password')
        if password:
            current_user.set_password(password)
        
        db.session.commit()
        flash('Perfil actualizado correctamente', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html')

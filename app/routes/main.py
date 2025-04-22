from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

main = Blueprint('main', __name__)

def email_confirmed_required(f):
    """Decorador para requerir confirmación de correo electrónico"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and not current_user.email_confirmed:
            flash('Por favor confirma tu correo electrónico antes de acceder a esta página.', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def index():
    """Página principal"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
@email_confirmed_required
def dashboard():
    """Dashboard principal para usuarios autenticados"""
    return render_template('dashboard.html')

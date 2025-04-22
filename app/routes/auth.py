from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, mail
from app.models.user import User
from app.models.agency import Agency
from werkzeug.security import generate_password_hash
from datetime import timedelta, datetime
from app.utils.email import send_email
import logging
import os

# Configurar el registro
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'auth.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('auth_service')

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
        
        if user and user.check_password(password):
            if not user.email_confirmed:
                flash('Por favor, confirma tu correo electrónico antes de iniciar sesión.', 'warning')
                return redirect(url_for('auth.login'))
            
            if not user.is_active:
                flash('Tu cuenta está desactivada. Contacta al administrador.', 'danger')
                return redirect(url_for('auth.login'))
            
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

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de nuevos agentes"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    agencies = Agency.query.all()
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        agency_id = request.form.get('agency_id')
        
        # Validaciones
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('auth/register.html', agencies=agencies)
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'danger')
            return render_template('auth/register.html', agencies=agencies)
        
        if User.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado', 'danger')
            return render_template('auth/register.html', agencies=agencies)
        
        # Crear nuevo usuario (agente)
        new_user = User(
            username=username,
            email=email,
            password=password,
            role='user',  # Rol de agente por defecto
            agency_id=agency_id,
            is_active=False,  # Inactivo hasta confirmar correo
            email_confirmed=False
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generar token y enviar correo de confirmación
        try:
            logger.debug(f"Generando token para usuario: {new_user.username}, email: {new_user.email}")
            token = new_user.generate_confirmation_token()
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)
            logger.debug(f"URL de confirmación generada: {confirm_url}")
            
            # Intentar enviar el correo usando la función send_email
            logger.debug("Intentando enviar correo de confirmación")
            send_email(
                to=new_user.email,
                subject='Confirma tu cuenta - Sistema de Agencias de Viajes',
                template='confirm_email',
                user=new_user,
                url=confirm_url,
                year=datetime.now().year
            )
            logger.info(f"Correo de confirmación enviado a: {new_user.email}")
            
            # Enviar correo de respaldo directamente con Flask-Mail si es necesario
            try:
                from flask_mail import Message
                with current_app.app_context():
                    msg = Message(
                        subject='Confirma tu cuenta - Sistema de Agencias de Viajes (Respaldo)',
                        recipients=[new_user.email]
                    )
                    msg.body = f"""Hola {new_user.username},

Gracias por registrarte en el Sistema de Agencias de Viajes.

Por favor, confirma tu cuenta haciendo clic en el siguiente enlace:
{confirm_url}

Si no has solicitado este registro, puedes ignorar este correo.

Saludos,
El equipo de Paseo Travel"""
                    msg.html = f"""<h2>Confirmación de Cuenta</h2>
<p>Hola {new_user.username},</p>
<p>Gracias por registrarte en el Sistema de Agencias de Viajes.</p>
<p>Por favor, confirma tu cuenta haciendo clic en el siguiente enlace:</p>
<p><a href="{confirm_url}">Confirmar mi cuenta</a></p>
<p>Si no has solicitado este registro, puedes ignorar este correo.</p>
<p>Saludos,<br>El equipo de Paseo Travel</p>"""
                    mail.send(msg)
                    logger.info(f"Correo de respaldo enviado a: {new_user.email}")
            except Exception as e:
                logger.error(f"Error al enviar correo de respaldo: {str(e)}")
            
            flash('Se ha enviado un correo de confirmación a tu dirección de correo electrónico.', 'info')
        except Exception as e:
            logger.error(f"Error en el proceso de envío de correo: {str(e)}")
            flash('Se ha registrado tu cuenta, pero hubo un problema al enviar el correo de confirmación. Contacta al administrador.', 'warning')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', agencies=agencies)

@auth.route('/confirm/<token>')
def confirm_email(token):
    """Confirmar correo electrónico"""
    if current_user.is_authenticated and current_user.email_confirmed:
        return redirect(url_for('main.dashboard'))
    
    email = User.verify_confirmation_token(token)
    if not email:
        flash('El enlace de confirmación es inválido o ha expirado.', 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('auth.login'))
    
    if user.email_confirmed:
        flash('Tu cuenta ya ha sido confirmada. Por favor, inicia sesión.', 'info')
    else:
        user.confirm_email()
        flash('¡Has confirmado tu cuenta correctamente! Ahora puedes iniciar sesión.', 'success')
    
    return redirect(url_for('auth.login'))

@auth.route('/resend-confirmation')
@login_required
def resend_confirmation():
    """Reenviar correo de confirmación"""
    if current_user.email_confirmed:
        flash('Tu cuenta ya ha sido confirmada.', 'info')
        return redirect(url_for('main.dashboard'))
    
    token = current_user.generate_confirmation_token()
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    
    send_email(
        to=current_user.email,
        subject='Confirma tu cuenta - Sistema de Agencias de Viajes',
        template='confirm_email',
        user=current_user,
        url=confirm_url,
        year=datetime.now().year
    )
    
    flash('Se ha enviado un nuevo correo de confirmación.', 'info')
    return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    """Página para usuarios no confirmados"""
    if current_user.email_confirmed:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/unconfirmed.html')

from flask import render_template, current_app
from flask_mail import Message
from app import mail
from threading import Thread
import logging
import os

# Configurar el registro
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'email.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('email_service')

def send_async_email(app, msg):
    """Envía un correo electrónico de forma asíncrona"""
    try:
        with app.app_context():
            logger.debug(f"Intentando enviar correo a: {msg.recipients}")
            mail.send(msg)
            logger.info(f"Correo enviado exitosamente a: {msg.recipients}")
    except Exception as e:
        logger.error(f"Error al enviar correo a {msg.recipients}: {str(e)}")

def send_email(to, subject, template, **kwargs):
    """
    Envía un correo electrónico usando una plantilla
    
    Args:
        to: Destinatario del correo
        subject: Asunto del correo
        template: Nombre de la plantilla (sin extensión)
        **kwargs: Variables para la plantilla
    """
    try:
        logger.debug(f"Preparando correo para: {to}, plantilla: {template}")
        app = current_app._get_current_object()
        msg = Message(subject, recipients=[to])
        
        try:
            msg.body = render_template(f'email/{template}.txt', **kwargs)
            logger.debug(f"Plantilla de texto renderizada correctamente: email/{template}.txt")
        except Exception as e:
            logger.error(f"Error al renderizar plantilla de texto: {str(e)}")
            msg.body = f"Por favor confirma tu cuenta haciendo clic en el siguiente enlace: {kwargs.get('url', '')}"  # Fallback básico
        
        try:
            msg.html = render_template(f'email/{template}.html', **kwargs)
            logger.debug(f"Plantilla HTML renderizada correctamente: email/{template}.html")
        except Exception as e:
            logger.error(f"Error al renderizar plantilla HTML: {str(e)}")
            msg.html = f"<p>Por favor confirma tu cuenta haciendo clic en el siguiente enlace: <a href='{kwargs.get('url', '')}'>Confirmar cuenta</a></p>"  # Fallback básico
        
        # Enviar el correo en un hilo separado para no bloquear la aplicación
        logger.debug("Iniciando hilo para envío de correo")
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        return thr
    except Exception as e:
        logger.error(f"Error general al enviar correo: {str(e)}")
        # No propagar la excepción para evitar que la aplicación falle
        return None

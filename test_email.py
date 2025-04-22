from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'Sistema de Agencias <no-reply@paseotravel.com>')

# Verificar que las credenciales estén configuradas
if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    print("ERROR: Las credenciales de correo electrónico no están configuradas.")
    print("Por favor, configure las variables de entorno MAIL_USERNAME y MAIL_PASSWORD.")
    print("Puede crear un archivo .env basado en .env.example con sus credenciales.")
    exit(1)

mail = Mail(app)

def send_test_email():
    with app.app_context():
        try:
            msg = Message(
                subject='Prueba de Correo - Sistema de Agencias',
                recipients=['paseotravelinc@gmail.com'],  # Enviar a la misma cuenta para prueba
                body='Este es un correo de prueba para verificar que el sistema de envío de correos funciona correctamente.',
                html='<h1>Prueba de Correo</h1><p>Este es un correo de prueba para verificar que el sistema de envío de correos funciona correctamente.</p>'
            )
            mail.send(msg)
            print("¡Correo enviado exitosamente!")
            return True
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
            return False

if __name__ == '__main__':
    send_test_email()

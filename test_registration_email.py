from flask import Flask
from flask_mail import Mail, Message
import os
import sys
from itsdangerous import URLSafeTimedSerializer as Serializer

# Añadir el directorio actual al path para poder importar los módulos de la aplicación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Crear una aplicación Flask de prueba
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-predeterminada'

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

def generate_confirmation_token(email):
    """Genera un token para confirmar el correo electrónico"""
    serializer = Serializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')

def verify_confirmation_token(token, expiration=3600):
    """Verifica el token de confirmación"""
    serializer = Serializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
        return email
    except:
        return None

def test_token_generation():
    """Prueba la generación y verificación de tokens"""
    email = 'test@example.com'
    token = generate_confirmation_token(email)
    print(f"Token generado: {token}")
    
    # Verificar el token
    verified_email = verify_confirmation_token(token)
    print(f"Email verificado: {verified_email}")
    
    if verified_email == email:
        print("✅ La generación y verificación de tokens funciona correctamente")
    else:
        print("❌ Error en la generación o verificación de tokens")

def test_email_sending():
    """Prueba el envío de correos con un token de confirmación"""
    test_email = 'paseotravelinc@gmail.com'  # Usar la misma cuenta para pruebas
    
    # Generar token
    token = generate_confirmation_token(test_email)
    
    # Crear URL de confirmación
    confirm_url = f"http://localhost:5000/confirm/{token}"
    
    with app.app_context():
        try:
            # Crear mensaje
            msg = Message(
                subject='Prueba de Confirmación - Sistema de Agencias',
                recipients=[test_email]
            )
            
            # Contenido del mensaje
            msg.body = f"""
            Hola,
            
            Gracias por registrarte en el Sistema de Agencias de Viajes.
            
            Por favor, confirma tu cuenta haciendo clic en el siguiente enlace:
            {confirm_url}
            
            Si no has solicitado este registro, puedes ignorar este correo.
            
            Saludos,
            El equipo de Paseo Travel
            """
            
            msg.html = f"""
            <h2>Confirmación de Cuenta</h2>
            <p>Gracias por registrarte en el Sistema de Agencias de Viajes.</p>
            <p>Por favor, confirma tu cuenta haciendo clic en el siguiente enlace:</p>
            <p><a href="{confirm_url}">Confirmar mi cuenta</a></p>
            <p>Si no has solicitado este registro, puedes ignorar este correo.</p>
            <p>Saludos,<br>El equipo de Paseo Travel</p>
            """
            
            # Enviar correo
            mail.send(msg)
            print("✅ Correo de prueba enviado exitosamente")
            return True
        except Exception as e:
            print(f"❌ Error al enviar el correo: {e}")
            return False

if __name__ == '__main__':
    print("=== Prueba de generación y verificación de tokens ===")
    test_token_generation()
    
    print("\n=== Prueba de envío de correo de confirmación ===")
    test_email_sending()

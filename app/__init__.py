from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
import os

# Inicializar extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'clave-secreta-predeterminada')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    
    # Configuración de sesión
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 horas en segundos
    app.config['SESSION_COOKIE_SECURE'] = False  # Cambiar a True en producción con HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'Sistema de Agencias <no-reply@paseotravel.com>')
    
    # Verificar que las credenciales de correo estén configuradas
    if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
        print("ADVERTENCIA: Las credenciales de correo electrónico no están configuradas.")
        print("Por favor, configure las variables de entorno MAIL_USERNAME y MAIL_PASSWORD.")
        print("La funcionalidad de envío de correos no estará disponible.")
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Configurar login_manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Registrar blueprints
    from app.routes.auth import auth as auth_blueprint
    from app.routes.main import main as main_blueprint
    from app.routes.admin import admin as admin_blueprint
    from app.routes.airlines import airlines as airlines_blueprint
    from app.routes.agencies import agencies as agencies_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(airlines_blueprint)
    app.register_blueprint(agencies_blueprint)
    
    # Asegurarse de que exista el directorio de uploads
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app

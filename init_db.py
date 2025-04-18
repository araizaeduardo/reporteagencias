from app import create_app, db
from app.models.user import User
from app.models.agency import Agency
from app.models.airline import Airline
import os

def init_database():
    """Inicializa la base de datos y crea un usuario administrador por defecto"""
    app = create_app()
    
    with app.app_context():
        # Crear las tablas de la base de datos
        db.create_all()
        
        # Verificar si ya existe un usuario administrador
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Creando usuario administrador por defecto...")
            admin = User(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuario administrador creado con éxito.")
            print("Usuario: admin")
            print("Contraseña: admin123")
        else:
            print("El usuario administrador ya existe.")
        
        # Crear directorios para uploads si no existen
        uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
        airlines_dir = os.path.join(uploads_dir, 'airlines')
        contracts_dir = os.path.join(uploads_dir, 'contracts')
        documents_dir = os.path.join(uploads_dir, 'documents')
        
        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(airlines_dir, exist_ok=True)
        os.makedirs(contracts_dir, exist_ok=True)
        os.makedirs(documents_dir, exist_ok=True)
        
        print("Directorios para archivos creados con éxito.")
        print("Inicialización de la base de datos completada.")

if __name__ == '__main__':
    init_database()

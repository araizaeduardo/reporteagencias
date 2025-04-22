import os
import sys
from datetime import datetime

# Añadir el directorio actual al path para poder importar los módulos de la aplicación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User

def activate_admin_user():
    """Activa el usuario administrador sin requerir confirmación de correo"""
    app = create_app()
    
    with app.app_context():
        # Buscar el usuario administrador
        admin = User.query.filter_by(role='admin').first()
        
        if not admin:
            print("No se encontró ningún usuario administrador en la base de datos.")
            return
        
        print(f"Usuario encontrado: {admin.username} ({admin.email})")
        print(f"Estado actual: Email confirmado: {admin.email_confirmed}, Activo: {admin.is_active}")
        
        # Activar el usuario
        admin.email_confirmed = True
        admin.is_active = True
        admin.email_confirm_date = datetime.utcnow()
        
        db.session.commit()
        
        print(f"Usuario administrador activado correctamente.")
        print(f"Nuevo estado: Email confirmado: {admin.email_confirmed}, Activo: {admin.is_active}")

if __name__ == '__main__':
    activate_admin_user()

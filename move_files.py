import os
import shutil
from app import create_app, db
from app.models.airline import Airline
from app.models.contract import Contract, ContractDocument

def move_files():
    """
    Mueve los archivos físicos a las ubicaciones correctas según las rutas en la base de datos.
    """
    app = create_app()
    with app.app_context():
        base_dir = os.path.join(app.root_path, 'static')
        
        # Mover documentos de contratos
        documents = ContractDocument.query.filter(ContractDocument.file_path.isnot(None)).all()
        for document in documents:
            if document.file_path and document.file_path.startswith('uploads/'):
                # Ruta de origen (donde podría estar el archivo actualmente)
                possible_sources = [
                    os.path.join(base_dir, document.file_path.replace('uploads/', '')),  # /static/documents/...
                    os.path.join(base_dir, 'documents', os.path.basename(document.file_path))  # /static/documents/filename.pdf
                ]
                
                # Ruta de destino (donde debería estar según la base de datos)
                dest_path = os.path.join(base_dir, document.file_path)
                
                # Asegurarse de que el directorio de destino existe
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Intentar mover el archivo desde posibles ubicaciones
                file_moved = False
                for src_path in possible_sources:
                    if os.path.exists(src_path) and not os.path.exists(dest_path):
                        try:
                            shutil.copy2(src_path, dest_path)
                            print(f"Archivo copiado: {src_path} -> {dest_path}")
                            file_moved = True
                            break
                        except Exception as e:
                            print(f"Error al copiar {src_path}: {e}")
                
                if not file_moved:
                    print(f"No se pudo mover el archivo para {document.name}. Posibles fuentes no encontradas.")
        
        print("Proceso de movimiento de archivos completado.")

if __name__ == "__main__":
    move_files()

from app import create_app, db
from app.models.airline import Airline
from app.models.contract import Contract, ContractDocument

def fix_file_paths():
    """
    Corrige las rutas de archivos en la base de datos para asegurar que sean consistentes.
    
    Problemas a corregir:
    1. Rutas duplicadas como 'uploads/uploads/...' -> 'uploads/...'
    2. Rutas sin el prefijo 'uploads/' -> añadir 'uploads/'
    3. Rutas que comienzan con 'airlines/' -> cambiar a 'uploads/airlines/'
    """
    app = create_app()
    with app.app_context():
        # Corregir rutas de logos de aerolíneas
        airlines = Airline.query.filter(Airline.logo_path.isnot(None)).all()
        for airline in airlines:
            if airline.logo_path:
                # Caso 1: Si tiene 'uploads/uploads/', eliminar uno
                if 'uploads/uploads/' in airline.logo_path:
                    airline.logo_path = airline.logo_path.replace('uploads/uploads/', 'uploads/')
                    print(f"Corregida ruta duplicada para aerolínea {airline.name}: {airline.logo_path}")
                
                # Caso 3: Si comienza con 'airlines/' sin 'uploads/', añadir 'uploads/'
                elif airline.logo_path.startswith('airlines/'):
                    airline.logo_path = f"uploads/{airline.logo_path}"
                    print(f"Corregida ruta de logo para aerolínea {airline.name}: {airline.logo_path}")
                
                # Caso 2: Si no comienza con 'uploads/' y no es una ruta absoluta, añadir el prefijo
                elif not airline.logo_path.startswith('uploads/') and not airline.logo_path.startswith('/'):
                    airline.logo_path = f"uploads/{airline.logo_path}"
                    print(f"Añadido prefijo 'uploads/' para aerolínea {airline.name}: {airline.logo_path}")
        
        # Corregir rutas de archivos de contratos
        contracts = Contract.query.filter(Contract.file_path.isnot(None)).all()
        for contract in contracts:
            if contract.file_path:
                # Caso 1: Si tiene 'uploads/uploads/', eliminar uno
                if 'uploads/uploads/' in contract.file_path:
                    contract.file_path = contract.file_path.replace('uploads/uploads/', 'uploads/')
                    print(f"Corregida ruta duplicada para contrato {contract.title}: {contract.file_path}")
                
                # Caso 2: Si no comienza con 'uploads/' y no es una ruta absoluta, añadir el prefijo
                elif not contract.file_path.startswith('uploads/') and not contract.file_path.startswith('/'):
                    contract.file_path = f"uploads/{contract.file_path}"
                    print(f"Añadido prefijo 'uploads/' para contrato {contract.title}: {contract.file_path}")
        
        # Corregir rutas de documentos de contratos
        documents = ContractDocument.query.filter(ContractDocument.file_path.isnot(None)).all()
        for document in documents:
            if document.file_path:
                # Caso 1: Si tiene 'uploads/uploads/', eliminar uno
                if 'uploads/uploads/' in document.file_path:
                    document.file_path = document.file_path.replace('uploads/uploads/', 'uploads/')
                    print(f"Corregida ruta duplicada para documento {document.name}: {document.file_path}")
                
                # Caso 3: Si comienza con 'documents/' sin 'uploads/', añadir 'uploads/'
                elif document.file_path.startswith('documents/'):
                    document.file_path = f"uploads/{document.file_path}"
                    print(f"Corregida ruta de documento para {document.name}: {document.file_path}")
                
                # Caso 2: Si no comienza con 'uploads/' y no es una ruta absoluta, añadir el prefijo
                elif not document.file_path.startswith('uploads/') and not document.file_path.startswith('/'):
                    document.file_path = f"uploads/{document.file_path}"
                    print(f"Añadido prefijo 'uploads/' para documento {document.name}: {document.file_path}")
        
        # Guardar cambios en la base de datos
        db.session.commit()
        print("Corrección de rutas completada con éxito.")

if __name__ == "__main__":
    fix_file_paths()

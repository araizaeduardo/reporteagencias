# Sistema de Gestión para Agencias de Viajes

Este sistema web desarrollado con Flask permite a las agencias de viajes gestionar contratos de aerolíneas, administrar usuarios, registrar ventas y generar reportes. La aplicación proporciona una interfaz intuitiva y segura para la gestión completa de las operaciones de agencias de viajes.

## Características

### Gestión de Usuarios y Agencias
- Sistema de autenticación con roles de administrador y agente
- Verificación de correo electrónico para nuevos registros
- Gestión completa de usuarios (crear, editar, eliminar)
- Administración de agencias de viajes
- Perfiles de usuario con información detallada

### Aerolíneas y Contratos
- Administración de aerolíneas con logos y descripciones
- Gestión de contratos con fechas de vigencia
- Subida y gestión de documentos adjuntos
- Búsqueda avanzada de contratos

### Ventas y Reportes
- Registro y seguimiento de ventas
- Cálculo de comisiones
- Filtros avanzados para búsqueda de ventas
- Preparado para futuras integraciones con APIs externas

### Interfaz y Experiencia de Usuario
- Diseño responsive con Bootstrap 5
- Interfaz intuitiva y moderna
- Iconografía con Font Awesome
- Validación de formularios en tiempo real

### Seguridad
- Hashing seguro de contraseñas
- Verificación de correo electrónico para nuevos usuarios
- Gestión avanzada de sesiones
- Protección contra ataques comunes
- Control de acceso basado en roles

## Estructura del Proyecto

```
websiteAgencias/
├── app/
│   ├── models/          # Modelos de la base de datos
│   │   ├── user.py      # Modelo de usuarios
│   │   ├── agency.py    # Modelo de agencias
│   │   ├── airline.py   # Modelo de aerolíneas
│   │   ├── contract.py  # Modelo de contratos
│   │   └── sale.py      # Modelo de ventas
│   ├── routes/          # Rutas de la aplicación
│   │   ├── auth.py      # Autenticación
│   │   ├── admin.py     # Panel de administración
│   │   ├── airlines.py  # Gestión de aerolíneas
│   │   ├── agencies.py  # Gestión de agencias
│   │   └── main.py      # Rutas principales
│   ├── static/          # Archivos estáticos
│   │   ├── css/         # Hojas de estilo
│   │   ├── js/          # JavaScript
│   │   └── uploads/     # Archivos subidos (logos, documentos)
│   ├── templates/       # Plantillas HTML
│   └── __init__.py      # Inicialización de la aplicación
├── migrations/          # Migraciones de la base de datos
├── run.py               # Script para ejecutar la aplicación
├── init_db.py           # Script para inicializar la base de datos
├── fix_file_paths.py    # Utilidad para corregir rutas de archivos
├── CHANGELOG.md         # Registro de cambios
└── requirements.txt     # Dependencias del proyecto
```

## Requisitos

- Python 3.8 o superior
- SQLite (incluido en Python)
- Dependencias listadas en requirements.txt:
  - Flask
  - Flask-SQLAlchemy
  - Flask-Login
  - Flask-WTF
  - Flask-Migrate
  - Flask-Mail
  - Werkzeug
  - Jinja2
  - itsdangerous
  - email-validator

## Instalación

1. Clonar el repositorio o descargar los archivos
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   ```

3. Activar el entorno virtual:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Inicializar la base de datos:
   ```bash
   python init_db.py
   ```

6. Ejecutar la aplicación:
   ```bash
   python run.py
   ```

7. Acceder a la aplicación en el navegador: `http://localhost:5001`

## Uso

### Acceso al Sistema
- **Usuario administrador predeterminado**:
  - Usuario: admin@example.com
  - Contraseña: admin123

### Panel de Administración
- Gestión de usuarios: crear, editar y eliminar usuarios
- Administración de aerolíneas: añadir nuevas aerolíneas, subir logos, gestionar contratos
- Gestión de agencias: crear y administrar agencias de viajes

### Panel de Agente
- Buscar contratos de aerolíneas
- Registrar ventas
- Ver comisiones
- Acceder a documentos de contratos

## Estructura de Directorios para Archivos Subidos

Los archivos subidos se almacenan en las siguientes ubicaciones:

- Logos de aerolíneas: `app/static/uploads/airlines/`
- Documentos de contratos: `app/static/uploads/contracts/`
- Documentos adicionales: `app/static/uploads/documents/`

## Desarrollo

### Migraciones de Base de Datos

Para realizar cambios en la estructura de la base de datos:

```bash
# Inicializar migraciones (solo la primera vez)
flask db init

# Crear una nueva migración
flask db migrate -m "Descripción de los cambios"

# Aplicar migraciones
flask db upgrade
```

### Solucionar Problemas con Rutas de Archivos

Si experimentas problemas con las rutas de archivos subidos, puedes ejecutar el script de corrección:

```bash
python fix_file_paths.py
```

## Despliegue en Producción

Para desplegar en un entorno de producción:

1. Configurar una clave secreta segura en una variable de entorno:
   ```bash
   export SECRET_KEY="tu_clave_secreta_segura"
   ```

2. Configurar la aplicación para usar HTTPS

3. Utilizar un servidor WSGI como Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 "run:app"
   ```

4. Configurar un servidor proxy inverso como Nginx

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.

## Contacto

Para más información o soporte, contactar a:
- Email: info@paseotravel.com
- Sitio web: https://paseotravel.com
   python -m venv venv
   ```
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```
5. Inicializar la base de datos:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. Ejecutar la aplicación:
   ```
   python run.py
   ```

## Uso

1. Acceder a la aplicación en `http://localhost:5000`
2. Iniciar sesión con las credenciales de administrador
3. Configurar agencias, aerolíneas y usuarios desde el panel de administración
4. Los agentes pueden acceder para buscar contratos de aerolíneas

## Entidades Principales

- **Usuarios**: Administradores y agentes de viajes
- **Agencias**: Empresas de viajes con múltiples agentes
- **Aerolíneas**: Compañías aéreas con sus respectivos contratos
- **Contratos**: Documentos legales entre aerolíneas y agencias
- **Ventas**: (Funcionalidad futura) Registro de ventas de boletos

## Futuras Mejoras

- Integración con API externa para ventas
- Sistema de reportes y estadísticas
- Notificaciones por correo electrónico para eventos importantes
- Panel de control avanzado con gráficos
- Recuperación de contraseña por correo electrónico

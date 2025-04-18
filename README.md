# Sistema de Gestión para Agencias de Viajes

Este sistema web desarrollado con Flask permite a las agencias de viajes buscar contratos de aerolíneas, gestionar usuarios, y en futuras versiones, registrar ventas y generar reportes.

## Características

- Dashboard para agencias de viajes
- Búsqueda de contratos de aerolíneas
- Administración de usuarios (administradores y agentes)
- Gestión de aerolíneas con documentos adjuntos
- CRUD completo para todas las entidades
- Base de datos SQLite
- Interfaz responsive con Bootstrap 5

## Estructura del Proyecto

```
websiteAgencias/
├── app/
│   ├── models/          # Modelos de la base de datos
│   ├── routes/          # Rutas de la aplicación
│   ├── static/          # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/       # Plantillas HTML
│   └── __init__.py      # Inicialización de la aplicación
├── run.py               # Script para ejecutar la aplicación
└── requirements.txt     # Dependencias del proyecto
```

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en requirements.txt

## Instalación

1. Clonar el repositorio o descargar los archivos
2. Crear un entorno virtual:
   ```
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
- Notificaciones por correo electrónico
- Panel de control avanzado con gráficos

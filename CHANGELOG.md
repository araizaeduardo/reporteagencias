# Changelog - Sistema de Agencias de Viajes

Este archivo documenta todos los cambios notables en el proyecto Sistema de Agencias de Viajes.

## [1.1.0] - 2025-04-22

### Corregido
- Solucionado problema con rutas de archivos que causaba errores 404 al acceder a logos de aerolíneas y documentos de contratos
- Corregida la función `save_file` para evitar la duplicación de directorios (`uploads/uploads/`)
- Implementada solución para asegurar que todas las rutas de archivos en la base de datos comiencen con 'uploads/'
- Corregido manejo de rutas para ser consistente en diferentes sistemas operativos (usando '/' en lugar de '\')

### Mejorado
- Añadidas verificaciones adicionales en las funciones de subida de archivos para garantizar rutas consistentes
- Implementadas validaciones para asegurar que los logos de aerolíneas siempre se guarden con el prefijo 'uploads/airlines/'
- Mejorado el manejo de rutas de documentos de contratos para asegurar accesibilidad
- Creados scripts de utilidad para corregir rutas de archivos en la base de datos (`fix_file_paths.py`)

### Seguridad
- Mejorada la configuración de sesiones para mayor seguridad
- Implementadas sesiones permanentes con tiempo de vida configurable
- Añadidas opciones de seguridad para cookies de sesión

## [1.0.0] - 2025-04-17

### Características
- Sistema de autenticación con roles de administrador y agente
- Gestión completa de usuarios (crear, editar, eliminar)
- Administración de aerolíneas con logos y descripciones
- Gestión de contratos con documentos adjuntos
- Administración de agencias de viajes
- Registro y seguimiento de ventas
- Panel de control para administradores
- Interfaz responsiva con Bootstrap 5
- Subida y gestión de archivos para contratos y logos

### Técnico
- Implementación basada en Flask
- Base de datos SQLite con SQLAlchemy
- Sistema de autenticación con Flask-Login
- Formularios con Flask-WTF
- Migraciones de base de datos con Flask-Migrate
- Estructura modular con Blueprints

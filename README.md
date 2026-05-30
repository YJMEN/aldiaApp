# AldiaApp

AldiaApp es una aplicación web desarrollada con Flask para gestionar usuarios, pagos mensuales y el estado de cuentas. Permite a los administradores agregar usuarios, registrar pagos, generar facturas mensuales automáticamente y visualizar estadísticas e historial.

## Características

- **Autenticación de administradores**: Sistema de login seguro con credenciales almacenadas en base de datos.
- **Gestión de usuarios**: Agregar, ver y gestionar usuarios con saldos a favor.
- **Sistema de pagos**: Registrar pagos completos o parciales, con manejo de saldos a favor.
- **Generación automática de facturas**: Cada mes se generan facturas pendientes para todos los usuarios.
- **Estadísticas y reportes**: Visualización de estadísticas mensuales y historial completo de pagos.
- **Interfaz web**: Templates HTML con CSS y JavaScript para una experiencia de usuario intuitiva.

## Requisitos

- **Python**: Versión 3.8 o superior (recomendado 3.14).
- **Dependencias**: Las bibliotecas necesarias se instalan automáticamente (ver sección de instalación).

## Instalación

1. **Clona el repositorio**:

   ```bash
   git clone <url-del-repositorio>
   cd aldiaApp
   ```

2. **Crea un ambiente virtual**:

   ```bash
   python -m venv .venv
   ```

3. **Activa el ambiente virtual**:
   - En Windows (PowerShell):
     ```powershell
     & ".\.venv\Scripts\Activate.ps1"
     ```
   - En Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Instala las dependencias**:

   ```bash
   pip install flask apscheduler
   ```

   Opcionalmente, crea un archivo `requirements.txt` con:

   ```
   flask
   apscheduler
   ```

   Y ejecuta:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración

- **Base de datos**: La aplicación utiliza SQLite. Las tablas se crean automáticamente al ejecutar la aplicación por primera vez.
- **Variables de entorno** (recomendado en producción):
   - `SECRET_KEY`: Clave secreta para sesiones (obligatoria en producción). No dejar un valor fijo en el código.
   - `ADMIN_USERNAME` y `ADMIN_PASSWORD`: Si se definen, se creará ese usuario administrador al inicializar la base de datos. No incluyas credenciales por defecto en el repositorio.
   - Para configurar, copia `.env.example` a `.env` o exporta variables en tu entorno (PowerShell: `$env:VARIABLE="valor"`).

## Ejecución

1. Asegúrate de que el ambiente virtual esté activado.
2. Ejecuta la aplicación:
   ```bash
   python run.py
   ```
3. Abre tu navegador y ve a `http://localhost:5001`.
4. Inicia sesión con las credenciales de administrador.

La aplicación se ejecutará en modo debug en el puerto 5001. Para producción, ajusta la configuración en `app.py`.

## Uso

- **Login**: Accede con usuario y contraseña de administrador.
- **Inicio**: Vista principal con estadísticas del mes actual.
- **Usuarios**: Agrega nuevos usuarios y ve su estado de pagos.
- **Detalle de usuario**: Registra pagos, ve historial y maneja saldos.
- **Historial**: Vista completa de todos los pagos.
- **Reset**: Opción para reiniciar la base de datos (solo para desarrollo).

## Estructura del proyecto

```
aldiaApp/
├── run.py                 # Archivo principal para ejecutar la aplicación Flask
├── reset_db.py            # Script para reiniciar la base de datos
├── app/
│   ├── __init__.py        # Inicialización de la aplicación y funciones de base de datos
│   ├── routes.py          # Definición de todas las rutas de la aplicación
│   ├── database.py        # Conexión a la base de datos
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css      # Estilos CSS
│   │   ├── js/
│   │   │   ├── common.js       # Funciones JavaScript comunes (confirmaciones)
│   │   │   ├── user_detail.js  # JavaScript para detalle de usuario
│   │   │   └── users.js        # JavaScript para gestión de usuarios
│   └── templates/
│       ├── history.html       # Plantilla de historial
│       ├── index.html         # Plantilla principal
│       ├── login.html         # Plantilla de login
│       ├── user_detail.html   # Plantilla de detalle de usuario
│       └── users.html         # Plantilla de usuarios
└── README.md              # Este archivo
```

## Notas adicionales

- La aplicación genera facturas automáticamente el primer día de cada mes a las 00:00 usando APScheduler.
- Los pagos se calculan sobre una mensualidad fija de 12,000 (ajustable en el código).
- Para desarrollo, el modo debug está habilitado. Desactívalo en producción.
- **Seguridad**: Las plantillas usan Jinja2 que escapa automáticamente el HTML. El JavaScript está organizado para evitar vulnerabilidades comunes como XSS. No se usan eval() ni innerHTML con datos no sanitizados. Se recomienda agregar tokens CSRF en producción para mayor seguridad.
- Si encuentras problemas, verifica que todas las dependencias estén instaladas y que el puerto 5001 esté disponible.

## Despliegue en PythonAnywhere

Pasos rápidos para desplegar en PythonAnywhere:

- Sube el código (git clone o SFTP) a tu cuenta.
- Crea y activa un virtualenv y ejecuta `pip install -r requirements.txt`.
- En la sección `Web`, configura el archivo WSGI para importar la aplicación:

```python
import sys
project_home = '/home/yourusername/path/to/aldiaApp'
if project_home not in sys.path:
   sys.path.insert(0, project_home)

from app import app as application
```

- Configura las `Environment variables` (SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD).
- No uses `APScheduler` dentro del WSGI para tareas programadas; crea una tarea en la sección `Tasks` que ejecute `generate_facturas.py` mensualmente.

Consulta `deploy/pythonanywhere.md` para instrucciones completas.

## Contribución

Si deseas contribuir, por favor crea un issue o pull request en el repositorio.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

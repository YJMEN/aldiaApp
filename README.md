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
- **Variables de entorno** (opcional):
  - `SECRET_KEY`: Clave secreta para sesiones. Si no se define, usa un valor por defecto (cambiar en producción).
  - `ADMIN_USERNAME`: Nombre de usuario del administrador por defecto (por defecto: "admin1").
  - `ADMIN_PASSWORD`: Contraseña del administrador por defecto (por defecto: "cocorote2026").
  - Para configurar, copia `.env.example` a `.env` y ajusta los valores. En Windows PowerShell: `$env:VARIABLE="valor"`.
- **Credenciales de administrador por defecto**:
  - Usuario: Definido por `ADMIN_USERNAME`
  - Contraseña: Definida por `ADMIN_PASSWORD`
  - Estas credenciales se crean automáticamente en la base de datos si no existen.

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

## Contribución

Si deseas contribuir, por favor crea un issue o pull request en el repositorio.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

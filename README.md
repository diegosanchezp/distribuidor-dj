# Distribuidor: Proyecto Comercio Electrónico 2-2021

## Setup ambiente de desarrollo
Para Windows se recomienda utilizar el subsistema de Linux

### Instalación de dependencias de sistema
Estas son las dependencias que tienen que tener instaladas en su sistema operativo
1. PostgreSQL:
   - **Archlinux**: seguir los pasos de las secciones
     1. https://wiki.archlinux.org/title/PostgreSQL#Installation
     2. https://wiki.archlinux.org/title/PostgreSQL#Initial_configuration
   - **Windows**: les toca de tarea a ustedes ver como instalar PostgreSQL en Windows, tiene que tener la configuración de instalación, sin usuarios ni autenticación
2. Python3.9
3. Poetry ( Gestor de dependencias de python )
   - https://python-poetry.org/docs/#installation

### Instalación de dependencias de python

```sh
# Instalar dependencias de python del proyecto
poetry install
```

### Correr script de setup de desarrollo
Este script de python crea
- Una base de datos en PostgreSQL
- Usuario administrador para django

Antes de ejecutar el script hay que tener el entorno virtual de python activado

```bash
# Activar entorno virtual de python
source .venv/bin/activate

# Correr script de setup
python django/setup_dev.py

# Al final te pedirá una contraseña para el usuario administrador de django
```
Correr el servidor para ver si todo funciona

```bash
python django/manage.py runserver
```

Si el servidor inicio exitosamente deberías de poder ingresar a http://127.0.0.1:8000

### Crear app de django
Las apps de django se crean en la carpeta `django/distribuidor-dj/apps`

Para crear una app ejecute el siguiente comando

```bash
APP_NAME="myapp"
mkdir django/distribuidor-dj/apps/$APP_NAME
python django/manage.py startapp $APP_NAME django/distribuidor-dj/apps/$APP_NAME
```

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

## Flujo de desarrollo

### Servidores
Para desarrollar tienes que tener los siguientes servidores levantados

```bash
# Servidor de django
python django/manage.py runserver

# Servidor que sincroniza archivos de tailwind
python django/manage.py tailwind start
```

### Flujo de commits
Antes de hacer un commit se ejecutan varios programas que verifican el código que se va a añadir al control de versiones, algunos de estos son

```bash
Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Check Yaml...........................................(no files to check)Skipped
Check for added large files..............................................Passed
Debug Statements (Python)................................................Passed
Check python ast.........................................................Passed
flake8...................................................................Passed
isort....................................................................Passed
black....................................................................Passed
```

Usted verá un log similar a ese cuando intente hacer commit, si observan el estado `Failed`, tienen que arreglar modificar su código para arreglarlo

Flake8 verifica que el código de python tenga un estilo predeterminado, si este programa llega a fallar puedes entrar en esta página

https://www.flake8rules.com/

Para saber como arreglar esos errores, con el código que te dice

Si no quieres que ninguna de las verificaciones corra, en caso de tener un problema con alguno de los programas, puedes ejecutar tu commit con el flag `--no-verify`.

```bash
# NO HAGAS ESTO, a menos que no tengas otra opción
git commit . -m 'quick fix' --no-verify
```

### Crear app de django
Las apps de django se crean en la carpeta `django/distribuidor-dj/apps`

Para crear una app ejecute el siguiente comando

```bash
APP_NAME="myapp"
mkdir django/distribuidor-dj/apps/$APP_NAME
python django/manage.py startapp $APP_NAME django/distribuidor-dj/apps/$APP_NAME
```

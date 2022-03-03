# Distribuidor: Proyecto Comercio Electrónico 2-2021

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

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
3. Nodejs 17
4. Poetry ( Gestor de dependencias de python )
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
### Coding
Se recomienda utilizar [tipos](https://docs.python.org/3/library/typing.html) en el código de python que se escriba para mejorar la legibilidad y evitar menos bugs.

Por ejemplo

```py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# HttpRequest y HttpResponse provenientes de django se utilizan para los tipos de
# la función home_view
def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="home.html", context={})
```

Para checkear los tipos puedes instalar la extensión de Visual Estudio Code [Pyright](https://github.com/microsoft/pyright#vs-code-integration)

Para mayor información
https://github.com/typeddjango/django-stubs
https://sobolevn.me/2019/08/typechecking-django-and-drf


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
### Aprender sobre django
[Páginas web para aprender sobre django](docs/learning-resources/django.md)

### Crear app de django
Las apps de django se crean en la carpeta `django/distribuidor-dj/apps`

Para crear una app ejecute el siguiente comando

```bash
APP_NAME="myapp"
mkdir django/distribuidor_dj/apps/$APP_NAME
python django/manage.py startapp $APP_NAME django/distribuidor_dj/apps/$APP_NAME
```

## Respaldo y carga de datos para la base de datos
### Respaldar datos

```
# Manera general de como respaldar los datos
python django/manage.py dumpdata --natural-foreign --natural-primary --indent 4 -o django/fixtures/name.json [app_label[.ModelName] ...]

# -- Ejemplos ---

# shipments
python django/manage.py dumpdata --natural-foreign --natural-primary --indent 4 -o django/fixtures/shipments.json shipment.Shipment shipment.ShipmentStatusDate shipment.ProductQuantity

# invoices
python django/manage.py dumpdata --natural-foreign --natural-primary --indent 4 -o django/fixtures/invoices.json invoice.Invoice invoice.InvoiceStatusDate
```

### Cargar datos respaldados

```bash
python django/manage.py loaddata django/fixtures/{customers.json,address-state.json,address.json,products-standalone.json,shipments.json,invoices.json}
```

## Borrar base de datos
Con el siguiente comando puedes borrar la base de datos y cargar los datos respaldados, ten en cuenta que el servidor de desarrollo de django no puede estar levantado porque tiene una conexión activa con postgres, si no el comando se quedara pegado por un rato hasta darte error.

```bash
# Borrar base de datos y cargar datos respaldados
python django/setup_dev.py --reset-db
```

## Comandos para servidor de producción heroku
```bash
# Conectarse al dyno de heroku
heroku run bash
# Crear admin
python django/manage.py createsuperuser --username dev --email dev@dev.com --settings distribuidor_dj.settings.production

```

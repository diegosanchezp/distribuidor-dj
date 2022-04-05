# Comandos para el Demo QA

Borrar base de datos
```
heroku pg:reset
```

```
heroku run python django/manage.py migrate --noinput --settings distribuidor_dj.settings.production
```
Cargar data

```bash
heroku run python django/manage.py loaddata --settings distribuidor_dj.settings.production django/fixtures/{dj_groups.json,address-state.json,address.json}
```

Crear admin

```bash
heroku run python django/manage.py createsuperuser --username dev --email dev@dev.com --settings distribuidor_dj.settings.production

```

Subir data para background task check_invoices

```
heroku run python django/manage.py loaddata --settings distribuidor_dj.settings.production django/fixtures/{dj_groups.json,customers.json,address-state.json,address.json,products-standalone.json,shipments.json,invoices.json,bg_task.json,invoice_bg_task.json}
```

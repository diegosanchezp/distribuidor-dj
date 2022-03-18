python django/manage.py migrate --noinput --settings distribuidor_dj.settings.production
python django/manage.py loaddata --settings distribuidor_dj.settings.production django/fixtures/{address-state.json,address.json,bg_task.json}

python django/manage.py migrate --noinput --settings distribuidor_dj.settings.production
python django/manage.py loaddata django/fixtures/{address-state.json,address.json} --settings distribuidor_dj.settings.production

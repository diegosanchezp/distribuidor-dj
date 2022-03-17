python django/manage.py migrate --noinput --settings distribuidor_dj.settings.production
python django/manage.py --settings distribuidor_dj.settings.production loaddata django/fixtures/{address-state.json,address.json}

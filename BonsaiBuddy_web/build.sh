#/bin/sh

pip install -r requirements.txt
cp /etc/secrets/production.py BonsaiBuddy/settings/
python manage.py collectstatic --no-input --settings BonsaiBuddy.settings.production
#/bin/sh

python3 -m pip install -r requirements.txt
# cp /etc/secrets/production.py BonsaiBuddy/settings/
python3 manage.py collectstatic --no-input
python3 manage.py migrate
python3 manage.py createsuperuser --no-input
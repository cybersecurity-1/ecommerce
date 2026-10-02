#!/usr/bin/env bash
# exit on error
set -o errexit

# If running from repo root, cd into the Django project directory
if [ -d "djangostack/project1/website1" ]; then
    cd djangostack/project1/website1
fi

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate


#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

cd fitubi_django/

python3 manage.py collectstatic --no-input
python3 manage.py migrate
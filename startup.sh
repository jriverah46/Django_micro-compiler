#!/bin/bash

# Migraciones y archivos estáticos
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Iniciar servidor con Gunicorn
gunicorn my_project.wsgi --bind=0.0.0.0 --timeout 600


release: python manage.py migrate
web: gunicorn medconsulting.wsgi
web: python heartcare/manage.py runserver 0.0.0.0:$PORT
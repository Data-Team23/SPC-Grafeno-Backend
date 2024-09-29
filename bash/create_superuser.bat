REM create_superuser.bat

REM Create superuser
docker-compose run app sh -c "python manage.py createsuperuser --noinput --username admin --email admin@admin.com"
docker-compose run app sh -c "python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin')\""

echo Superuser created.

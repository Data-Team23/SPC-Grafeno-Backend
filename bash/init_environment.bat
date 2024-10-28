REM init_environment.bat

REM Start containers
docker-compose up --build -d

REM Wait for the containers to be fully up (you may need to adjust the timeout)
timeout /t 10 /nobreak

REM Run initial migrations
docker-compose run app sh -c "python manage.py makemigrations"
docker-compose run app sh -c "python manage.py migrate"

REM Create superuser
docker-compose run app sh -c "python manage.py createsuperuser --noinput --username admin --email admin@admin.com"
docker-compose run app sh -c "python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin')\""

echo Environment setup complete and superuser created.
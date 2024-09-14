REM apply_migrations.bat

REM Apply migrations
docker-compose run app sh -c "python manage.py makemigrations"
docker-compose run app sh -c "python manage.py migrate"

echo Migrations applied.

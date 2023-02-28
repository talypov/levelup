
# Steps to setup development
1. Download project from git
2. docker build -t levelup_app .
3. docker-compose up -d --build
4. docker-compose exec web python manage.py migrate
5. docker-compose exec web python manage.py createsuperuser
6. http://localhost:8000/api/products/
7. http://localhost:8000/product/
8. http://localhost:8000/api/upload/

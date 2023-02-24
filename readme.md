
# Steps to setup development
1. docker-compose up -d --build
2. docker-compose exec web python manage.py migrate
3. docker-compose exec web python manage.py createsuperuser
4. http://localhost:8000/api/products/
5. http://localhost:8000/product/

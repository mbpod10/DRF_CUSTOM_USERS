# Django REST Framework Custom Users / Login / Auth

```
django-admin start-project backend
cd backend
django-admin start-app api
```

In `backend/setting.py` import rest_framework, authoken, and api app
```py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
]
```

## Migrate and CreateSuperUser Runserver
```
python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py createsuperuser
python3 manage.py runserver
```

Go to http://127.0.0.1:8000/admin/auth/ and login to make sure the server is running
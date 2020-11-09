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

# Create Url Endpoints

In `backend/urls.py`:
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```
Now, create a `urls.py` file in `/api` and in the file, we will deal with this later.

## There are Three Steps We Need to Take To Get Our URLs

### 1. Create User Serializers
- Create a `serializers.py` file in `/api`
- We will import the Django Default User Model by `from django.contrib.auth.models import User`, this model comes with built-in fields that we can choose to return to the client when we return the user. The fields are as follows: 
```json
{
        "id": 1,
        "password": "",
        "last_login": "",
        "is_superuser": true,
        "username": "",
        "first_name": "",
        "last_name": "",
        "email": "",
        "is_staff": true,
        "is_active": true,
        "date_joined": "",
        "groups": [],
        "user_permissions": []
    }
```
Lets specify what we want to return to the client. 
- import serializers: `from rest_framework import serializers`
- import User model:  `from django.contrib.auth.models import User`
- create a User serializer class and declare the model (User) and fields we want to return from the default User fields

```py
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

```

### 2. Create UserViewSet
- in `api/views` we need to import viewsets from restframework: `from rest_framework import viewsets`
- create a class `UserViewSet`
  - This will show the whole list of Users and comes with full CRUD functionality
    - WE WILL REVISIT THIS
- within the viewset, query all of the users and declare the serializer we just made

```py
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

### 3. Change URLs
- import routers and create the 'users' endpoint with the UserViewSet as the view
- include the urls
```py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
```
#### NOTE: users is the endpoint for all our user functionality

Now, go to http://127.0.0.1:8000/api/users/ all users AND information we specified in the serializers FIELDS will be displayed along with a HASHED PASSWORD. <b>For security reasons, we want to remove that hashed password and only display username and id</b>

Go back to UserSerializiers and add extra_kwargs. The field is still there but only allow for posting. 
```py
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
```

Refresh http://127.0.0.1:8000/api/users/ to see that password is now gone

### Crud Functionality
Go to http://127.0.0.1:8000/admin/auth/user/ and create a new user. Then in Postman, send a DELETE request to http://127.0.0.1:8000/api/users/2/ to see that the new user is deleted. All Crud functions work this way. 

#### NOTE: The integer at the endpoint is the user id

- ENDPOINTS FOR CRUD:
```
CREATE NEW USER: http://127.0.0.1:8000/api/users/
RETRIEVE USER: http://127.0.0.1:8000/api/users/2/
UPDATE USER: http://127.0.0.1:8000/api/users/2/
DELETE USER: http://127.0.0.1:8000/api/users/2/
```

## Custom Login Functionality

First and foremost, the UserViewSet allows us to make custome url endpoints using function names. So within our UserViewSet, we can name a function `login`, and it will us to do some logic through the endpoint http://127.0.0.1:8000/api/users/login/ client-side. 

Also, we need to import various modules from django and rest_framework. Most important is the Token from restframework models. This a unique token for a user that will allow client-side authorization. 
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
- We will import the Django Default User Model by `from django.contrib.auth.models import User`, this model comes with built-in fields that we can choose to return to the client when we return the user. 

The fields are as follows: 
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
- in `api/views` we need to import viewsets from restframework: `from rest_framework import viewsets` and the serializer we just made `from .serializers import UserSerializer`
- create a class `UserViewSet`
  - This will show the whole list of Users and comes with full CRUD functionality
    - WE WILL REVISIT THIS
- within the viewset, query all of the users and declare the serializer we just made

```py
from rest_framework import viewsets
from .serializers import UserSerializer

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
RETRIEVE ALL USERS: http://127.0.0.1:8000/api/users/
RETRIEVE USER: http://127.0.0.1:8000/api/users/2/
UPDATE USER: http://127.0.0.1:8000/api/users/2/
DELETE USER: http://127.0.0.1:8000/api/users/2/
```

## Custom User Functionality

First and foremost, the UserViewSet allows us to make custom url endpoints using function names. So within our UserViewSet, we can name a function `login`, and it will allow us to do some logic through the endpoint http://127.0.0.1:8000/api/users/login/ client-side and we can specify the type of request for that particular endpoint. 

Also, we need to import various modules from django and rest_framework. Most important is the Token from rest_framework models. This a unique token for a user that will allow client-side authorization and this need to be created whenever a new user registers. 

<b>The purpose of custom user urls is to allow us to dictate how the backend communicates with the client. We want to be in control of how that works and control the logic of how we would like our users to register/login/authenticate</b>

We will discuss the imports as we go. They are as follows:

```py
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
```

## Register
Lets make a method called `register` that will allow us to create a new user. 

First, we need to create it with an `@action` decorator that will dictate that only POST requests are allowed at the `register` endpoint. SO WHENEVER A CLIENT GOES TO http://127.0.0.1:8000/api/users/register/ THEY CAN <b>ONLY</b> DO POST REQUESTS. 

Moreover, the `detail` is a boolean indicating if the current action is configured for a list or detail view. Generally, registration is done in a list view.

Also, we are going to send a message as and object as well as a `Response` that will allow JSON to be sent to the client along with a status. Client-side servers need this to identify if the request was good. Especially React.js

It will look like this:

```py
  @action(detail=False, methods=['POST'])
  def register(self, request):
    print(request.data)
    message = {'message': "Register"}   
    return Response(message, status=status.HTTP_200_OK)
```

#### Postman
go to Postman, select `POST` request and go to `BODY` then `form-data` and insert the following:

|   Key    | Value     |
| username | brock2    | 
| password | password1 | 

Hit send    

Within the `request` argument of `register` method, is the body within our post request. so when we post to this endpoint, the request is this printed in the console:

```
<QueryDict: {'username': ['brock2'], 'password': ['password1']}>
```

We can now set up variables to pick out those elements within `request.data`. So, to extract the password and username, we will do:

```py
username = request.data['username']
password = request.data['password']
```

As the first part of logic, we will see if this username already exists in the database. We will do this by creating a dummy valiable and seeing if it exists.

```py
search_username = User.objects.filter(username=username)
```

Now we see if it exists, and if it does, we want to send a message saying that it already exists

```py
if search_username:
    message = {'message': "Username Already Exists"}
    return Response(message, status=status.HTTP_200_OK)
```

so our function should look like this:
```py
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def register(self, request):
        print(request.data)

        username = request.data['username']
        password = request.data['password']       

        search_username = User.objects.filter(username=username)

        if search_username:
            message = {'message': "Username Already Exists"}
            return Response(message, status=status.HTTP_200_OK)

```

Now make a POST request in Postman with the username of your superuser or a user that exists in the database, it should send a json message as: 

```json
{
    "message": "Username Already Exists"
}
```

Before we get into the weeds, lets now create and register a new user. So based on username and password, we will create the user by: 

1. Create a new user instance with username and password we extracted from the post response
2. Serialize the user object so it can be sent as json and specify that its only one object
3. Create a new token for the new user and will be sent to the client
4. Create a response that sends a message, the user data, and the unique token of the user
5. Return a Reponse with the data and an HTTP status

```py
user = User.objects.create_user(username=username, password=password)
serializer = UserSerializer(user, many=False)
token = Token.objects.create(user=user)
message = {'message': "User Created",
            'user': serializer.data, 'token': token.key}
return Response(message, status=status.HTTP_200_OK)

```

WHOLE METHOD:
```py
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def register(self, request):
        print(request.data)

        username = request.data['username']
        password = request.data['password']       

        search_username = User.objects.filter(username=username)

        if search_username:
            message = {'message': "Username Already Exists"}
            return Response(message, status=status.HTTP_200_OK)

        user = User.objects.create_user(username=username, password=password)
        serializer = UserSerializer(user, many=False)
        token = Token.objects.create(user=user)
        message = {'message': "User Created",
                   'user': serializer.data, 'token': token.key}
        return Response(message, status=status.HTTP_200_OK)
```

Now, create a new user with a unique username, the response should be something like this:
```json
{
    "message": "User Created",
    "user": {
        "id": 3,
        "username": "brock1"
    },
    "token": "11b5047df0925e16d2b4c814b08eb13e67beea05"
}
```

## Password Specific 

We can create logic similar to what we have already to send messages that passwords are not strong enough or long enough. As long as you know how to extract the body of the request, the variations are endless. Let's just send a message that the password is not long enough. This is within the register method still

```py
    if len(password) < 8:
        message = {'message': "Password Must Be Longer Than 8 Characters"}
        return Response(message, status=status.HTTP_200_OK)
```
Enter a password that is less than 8 characters long, the response:

```json
{
    "message": "Password Must Be Longer Than 8 Characters"
}
```

## Login

Now that we have created user, we need to allow us to login. 

This is similar to register but it includes a built in Django method called `authenticate()` This will allow us to compare usernames with passwords. 

Also, if there is no user, we want to send a message back to the client saying that credentials are invalid. We don't want to specify if its the wrong username or password due to security risks. We will call this method `login` and its on the same level as `register`. 

Therefore, endpoint for this method will be http://127.0.0.1:8000/api/users/login/ as a POST request

1. Extract the username and password from request
2. If username and password exist, create a variable user and authenticate
3. If no user variable exists (invalid username or pass), send a message of invalid credentials
4. If there is a user, serialize the user object and many to false
5. Query the token associated with that user
6. Create a response that sends a message, the user data, and the unique token of the user
7. Return the message and the HTTP status

```py
    @action(detail=False, methods=['POST'])
    def login(self, request):

        username = request.data['username']
        password = request.data['password']

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                message = {'message': 'Invalid Password or Username.'}
                return Response(message, status=status.HTTP_200_OK)

            serializer = UserSerializer(user, many=False)
            token = Token.objects.get(user=user)
            message = {'message': 'LOGGED_IN',
                       'user': serializer.data, 'token': token.key}
            return Response(message, status=status.HTTP_200_OK)

```

At the endpoint http://127.0.0.1:8000/api/users/login/ as a POST request, enter the valid password and username of an existing user in Postman

Reponse:

```json
{
    "message": "LOGGED_IN",
    "user": {
        "id": 1,
        "username": "brock"
    },
    "token": "28474bb92ffb01fbc8a1874cf6ecc8c11cdadda7"
}
```
<b>You may need to go to http://127.0.0.1:8000/admin/authtoken/tokenproxy/ and add a token to the superuser if you are getting an error. There was no token created when we initially created the superuser</b>

## Change Password

This is also similar but we are going to be using some different methods

1. declare `change_password` function and have `@action` as PUT
2. get password, and username from the body request
3. make sure the new password is more than 7 characters
4. get the user that with the username that wishes to change password
5. apply `user.set_password(password)` to the user
6. save the user
7. once again, get the token associated with that user
8. created a message that the password was created successfully
9. return the message with HTTP status

```py
@action(detail=False, methods=['PUT'])
    def change_password(self, request, pk='username'):
        password = request.data['password']
        username = request.data['username']

        if len(password) < 8:
            message = {'message': "Password Must Be Longer Than 8 Characters"}
            return Response(message, status=status.HTTP_200_OK)

        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        token = Token.objects.get(user=user)
        message = {'message': "Password Successfully Changed",
                   'token': token.key}
        return Response(message, status=status.HTTP_200_OK)
```

<b>NOTE</b>: the endpoint is http://127.0.0.1:8000/api/users/change_password/ and the Postman request is PUT

Try to change the password of an existing user and then try to login with the old password, then the new password

## Nested User Models With Related Models

We want to attach a seperate model to the user model so we have data whenever we get the user object client side. 

1. Create New Model Called Book in `models.py`
2. Create a foreignkey to the User and add a related_name field that will be added to User Model
3. Create Book Serializer in `serializers.py`
4. add books field to UserSerializer
5. add 'books' to User field

```py
#api/models.py
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    user = models.ForeignKey(User, related_name='books',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)

    def __str__(self):
        return self.title

```

```py
#api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('user', 'title', 'author')


class UserSerializer(serializers.ModelSerializer):
    # this field is added to the User Meta fields below
    books = BookSerializer(read_only=True, many=True)

    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'books')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
```

Go to http://127.0.0.1:8000/api/users/ and see that books is now in the user field
```json
[
    {
        "id": 1,
        "username": "brock",
        "books": [
            {
                "user": 1,
                "title": "Code",
                "author": "Rumplestillskin"
            }
        ]
    },
    {
        "id": 3,
        "username": "brock1",
        "books": []
    },
    {
        "id": 4,
        "username": "brock3",
        "books": []
    }
]
```
# Project Setup: Django REST Framework API with React Frontend Integration

refactor your code from traditional Django views to Django REST Framework (DRF) for handling API requests,
This guide will help you restart your Django project, better organize it, set up APIs using Django REST Framework, and connect them with your React frontend.

## 1. **Restarting the Django Project**

If you're restarting the Django project, ensure you clean up any unnecessary files or configurations to maintain an organized project structure. Follow these steps to set up your project for API and frontend integration.

## 2. **Install Required Dependencies**

Install the necessary dependencies in your virtual environment to set up the Django REST Framework and handle cross-origin requests from your React frontend.

```bash
pip install djangorestframework django-cors-headers
```

## 3. **Set Up API using Django REST Framework (DRF)**

To interact with the React frontend, expose APIs using Django REST Framework.

### 3.1 **Create Serializers**

Serializers are needed to convert your Django models into JSON for the frontend.

Create `profiles/serializers.py`:

```python
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'user_name', 'company_name', 'job_title', 'years_of_experience', 'bio', 'phone', 'image', 'email']
```

### 3.2 **Create Views**

In `profiles/views.py`, define the views to expose your API.

```python
from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
```

### 3.3 **Set Up URLs**

In `profiles/urls.py`, register the API endpoint.

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

### 3.4 **Include the API URLs in Project-Level URLs**

In your project-level `urls.py` (e.g., `revenue_hive_backend/urls.py`), include the `profiles` URLs.

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
]
```

## 4. **Enable Cross-Origin Resource Sharing (CORS)**

Since React and Django will run on different ports during development, you need to enable CORS to allow the frontend to communicate with the Django API.

### 4.1 **Install django-cors-headers**

Install `django-cors-headers` to handle cross-origin requests.

```bash
pip install django-cors-headers
```

### 4.2 **Add CORS Configuration to Settings**

In `revenue_hive_backend/settings.py`, add `corsheaders` to `INSTALLED_APPS` and the middleware stack.

```python
INSTALLED_APPS = [
    # other apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # other middleware
]

CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (you can restrict this later)
```

## 5. **Connect the Django API to React**

Now that your Django backend API is set up, you can connect it to your React frontend.

### 5.1 **Make HTTP Requests from React**

In your React frontend, you can use `axios` (or any other HTTP library) to interact with the Django API. Below is an example using `axios` to fetch profiles:

```javascript
import axios from 'axios';
import { useEffect } from 'react';

const fetchProfiles = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/profiles/');
    console.log(response.data);
  } catch (error) {
    console.error('Error fetching profiles:', error);
  }
};

useEffect(() => {
  fetchProfiles();
}, []);
```

### 5.2 **Run Both Servers**

#### **Start Django Backend:**

To run the Django server, use:

```bash
python manage.py runserver
```

#### **Start React Frontend:**

In the React project directory, start the frontend:

```bash
npm start
```

Now, your Django API and React frontend are connected, and you can make requests from the frontend to interact with your backend.

---

## Conclusion

This guide sets up a clean, modular Django project with a connected React frontend using Django REST Framework and `django-cors-headers` to manage cross-origin requests.

---

Let me know if you need more information or if there’s anything else you’d like to add!


![ApiRoot_image](profiles/dev_sc/ApiRoot.png)


<!--  -->

Here's a `README.md` formatted guide for refactoring your Django project to use Django REST Framework (DRF) and testing APIs with Postman:

---

# Django Project Refactor Guide: Using Django REST Framework (DRF) and Testing with Postman

This guide outlines the steps to refactor your Django project to use Django REST Framework (DRF), set up necessary APIs, and test them with Postman.

## Steps to Refactor Your Project for DRF

### 1. Install Django REST Framework

If you haven’t installed DRF yet, do so by running:

```bash
pip install djangorestframework
```

Next, add it to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # other apps
    'rest_framework',
    'profiles',  # Add your profiles app here
]
```

### 2. Create Serializers for User and Profile

Your project likely already has `Profile` and `User` models, so create serializers for them in `profiles/serializers.py`:

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'profileID', 'user_name', 'company_name', 'job_title', 'years_of_experience', 'bio', 'phone', 'image', 'email', 'has_completed_questionnaire']
```

### 3. Create API Views Using DRF Viewsets

In `profiles/views.py`, refactor your views using DRF’s `ModelViewSet` for CRUD operations:

```python
from rest_framework import viewsets
from .models import Profile
from .serializers import ProfileSerializer, UserSerializer
from django.contrib.auth.models import User

# API view for User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# API view for Profile
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
```

This will automatically provide CRUD operations for both users and profiles (`list`, `retrieve`, `create`, `update`, `delete`).

### 4. Set Up URLs for the API

Create or update `profiles/urls.py` to define routes for your API:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

Ensure that the `profiles` URLs are included in your project’s main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
]
```

### 5. Test API with Postman

Now that your API is set up, you can test it using Postman.

Run your Django server:

```bash
python manage.py runserver
```

Open Postman and test the following API endpoints:

#### **User API Endpoints:**
- **GET**: `http://localhost:8000/api/users/` - List all users
- **POST**: `http://localhost:8000/api/users/` - Create a new user
- **GET**: `http://localhost:8000/api/users/<id>/` - Retrieve a specific user
- **PUT**: `http://localhost:8000/api/users/<id>/` - Update a specific user
- **DELETE**: `http://localhost:8000/api/users/<id>/` - Delete a specific user

#### **Profile API Endpoints:**
- **GET**: `http://localhost:8000/api/profiles/` - List all profiles
- **POST**: `http://localhost:8000/api/profiles/` - Create a new profile
- **GET**: `http://localhost:8000/api/profiles/<id>/` - Retrieve a specific profile
- **PUT**: `http://localhost:8000/api/profiles/<id>/` - Update a specific profile
- **DELETE**: `http://localhost:8000/api/profiles/<id>/` - Delete a specific profile

Test CRUD operations by sending requests to these endpoints using Postman. For **POST** requests, use JSON data to create or update records. Example data for creating a user:

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "password123"
}
```

### 6. Login and Logout APIs

For token-based authentication, you can set up authentication endpoints.

#### **Install Django REST Framework’s authtoken package:**

```bash
pip install djangorestframework-authtoken
```

#### **Add it to `INSTALLED_APPS`:**

```python
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'profiles',
]
```

#### **Create Token-based Authentication Endpoints:**

Add the following to `profiles/urls.py`:

```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns += [
    path('api/token-auth/', obtain_auth_token, name='api_token_auth'),
]
```

#### **Test with Postman:**

- **Login (Get Token)**:
  - **Endpoint**: `http://localhost:8000/api/token-auth/`
  - **Method**: POST
  - **Body** (as raw JSON):

    ```json
    {
      "username": "testuser",
      "password": "password123"
    }
    ```

This will return an authentication token, which you can use for further API requests by adding it to the request headers in Postman:

```
Authorization: Token <your_token>
```

### 7. Test and Verify

After refactoring your code, test all your endpoints with Postman, ensuring you can successfully perform create, retrieve, update, and delete operations on users and profiles.


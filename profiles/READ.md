

# Project Setup: Django REST Framework API with React Frontend Integration

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
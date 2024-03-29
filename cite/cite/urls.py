"""cite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from .view import unknown_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls.auth', namespace='auth'), name='auth'),
    path('', include('main.urls.users', namespace='users'), name='users'),
    path('', include('main.urls.other', namespace='other'), name='other'),
    path('duty/', include('main.urls.duty', namespace='duty'), name='duty'),
    path('unknown_error', unknown_error, name='unknown_error'),
]

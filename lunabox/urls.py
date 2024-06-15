"""lunabox URL Configuration

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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from estoque.views import ItemListView, LocalidadeCreateView
from estoque.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('itens/', include('estoque.urls')),  # Inclua as URLs do aplicativo estoque
    path('usuarios/', include('estoque.urls')),  # Inclua as URLs do aplicativo estoque
    path('login/', CustomLoginView.as_view(), name='login'),  # Rota para a página de login
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Rota para a página de logout
    path('localidade/', include('estoque.urls')),  # Inclua as URLs do aplicativo estoque
]

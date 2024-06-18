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
from estoque.views import ItemListView, LocalidadeCreateView, UserListView, ItemCreateView, ItemUpdateView, UserCreateView, export_items_to_csv, ItemDeleteView, ItemDetailView, DashboardView, UserDetailView, LocalDetailView
from estoque.views import CustomLoginView, CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static
from estoque import views


urlpatterns = [
  path('itens/', ItemListView.as_view(), name='item-list'),
  path('itens/novo', ItemCreateView.as_view(), name='item-create'),
  path('itens/<int:pk>/editar/', ItemUpdateView.as_view(), name='item-update'),
  path('usuarios/', UserListView.as_view(), name='user-list'),
  path('usuarios/novo', UserCreateView.as_view(), name='user-create'),
  path('itens/export', export_items_to_csv, name='export-items'),
  path('localidade/', LocalidadeCreateView.as_view(), name='local-create'),
  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', CustomLogoutView.as_view(), name='logout'),
  path('itens/<int:pk>;deletar', ItemDeleteView.as_view(), name='item-delete'),
  path('itens/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
  path('', DashboardView.as_view(), name='dashboard'),
  path('grappelli/', include('grappelli.urls')),  # Adiciona esta linha
  path('admin/', admin.site.urls, name='admin'),
  path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
  path('localidades/', views.localidade_list, name='localidade-list'),
  path('localidades/<int:pk>/', LocalDetailView.as_view(), name='local-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

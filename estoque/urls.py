from django.urls import path, include
from .views import ItemCreateView, ItemUpdateView, ItemListView, UserCreateView, UserListView, export_items_to_csv, LocalidadeCreateView, ItemDeleteView, ItemDetailView, DashboardView, CustomLogoutView, UserDetailView, LocalDetailView
from django.contrib.auth import views as auth_views
from django.contrib import admin
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
  path('logout/', CustomLogoutView.as_view(template_name='logout.html'), name='logout'),
  path('itens/<int:pk>;deletar', ItemDeleteView.as_view(), name='item-delete'),
  path('itens/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
  path('', DashboardView.as_view(), name='dashboard'),
  path('grappelli/', include('grappelli.urls')),  # Adiciona esta linha
  path('admin/', admin.site.urls, name='admin'),
  path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
  path('localidades/', views.localidade_list, name='localidade-list'),
  path('localidades/<int:pk>/', LocalDetailView.as_view(), name='local-detail'),
]

from django.urls import path
from .views import ItemCreateView, ItemUpdateView, ItemListView, UserCreateView, UserListView, export_items_to_csv, LocalidadeCreateView


urlpatterns = [
  path('itens/', ItemListView.as_view(), name='item-list'),
  path('itens/novo', ItemCreateView.as_view(), name='item-create'),
  path('itens/<int:pk>/editar/', ItemUpdateView.as_view(), name='item-update'),
  path('usuarios/', UserListView.as_view(), name='user-list'),
  path('usuarios/novo', UserCreateView.as_view(), name='user-create'),
  path('itens/export', export_items_to_csv, name='export-items'),
  path('localidade/', LocalidadeCreateView.as_view(), name='local-create'),
]

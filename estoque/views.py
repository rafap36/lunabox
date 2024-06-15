from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Item, Localidade
from .forms import Itemform, Localform
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.models import User
from .forms import UserCreationForm
import csv
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.

class ItemCreateView(LoginRequiredMixin, CreateView):
  model = Item
  form_class = Itemform
  template_name = 'item_form.html'
  success_url = '/itens/'

  def form_valid(self, form):
        form.instance.criador_por = self.request.user  # Associa o item ao usuário logado
        return super().form_valid(form)


class ItemUpdateView(UpdateView):
  model = Item
  form_class = Itemform
  template_name = 'item_form.html'
  success_url = '/itens/'

class ItemListView(ListView):
  model = Item
  template_name = 'item_list.html'
  context_object_name = 'items'

  def get_queryset(self):
    queryset = super().get_queryset()
    localidade = self.request.GET.get('localidade')
    nome_item = self.request.GET.get('nome_item')

    if localidade:
      queryset = queryset.filter(localidade__nome__icontains=localidade)
    if nome_item:
      queryset = queryset.filter(nome__icontains=nome_item)

    return queryset

class UserCreateView(CreateView):
  model = User
  form_class = UserCreationForm
  template_name = 'user_form.html'
  success_url = '/usuarios/'

class UserListView(ListView):
  model = User
  template_name = 'user_list.html'
  context_object_name = 'users'


def export_items_to_csv(request):
    items = Item.objects.all()  # Obtém todos os itens do modelo Item

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items.csv"'

    writer = csv.writer(response)
    writer.writerow(['nome', 'quantity', 'preco', 'localidade', 'GL_category', 'descricao', 'asset_class'])

    for item in items:
        writer.writerow([item.nome, item.quantity, item.preco, item.localidade, item.GL_category, item.descricao, item.asset_class])

    return response


class LocalidadeCreateView(CreateView):
  model = Localidade
  form_class = Localform
  template_name = 'local_form.html'
  success_url = '/itens/'


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Nome do template de login (deve estar em templates/registration/)


class CustomLogoutView(LogoutView):
    # Personalize conforme necessário
    pass

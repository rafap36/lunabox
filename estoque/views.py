from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Localidade, UserActionLog
from .forms import Itemform, Localform
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.models import User
from .forms import UserCreationForm
import csv
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


@method_decorator(login_required, name='dispatch')
class ItemCreateView(LoginRequiredMixin, CreateView):
  model = Item
  form_class = Itemform
  template_name = 'item_form.html'
  success_url = '/itens/'

  def form_valid(self, form):
        form.instance.criador_por = self.request.user  # Associa o item ao usuário logado
        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class ItemUpdateView(UpdateView):
  model = Item
  form_class = Itemform
  template_name = 'item_form.html'
  success_url = '/itens/'


@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class UserCreateView(CreateView):
  model = User
  form_class = UserCreationForm
  template_name = 'user_form.html'
  success_url = '/usuarios/'

@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
  model = User
  template_name = 'user_list.html'
  context_object_name = 'users'


@method_decorator(login_required, name='dispatch')
def export_items_to_csv(request):
    items = Item.objects.all()  # Obtém todos os itens do modelo Item

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items.csv"'

    writer = csv.writer(response)
    writer.writerow(['nome', 'quantity', 'preco', 'localidade', 'GL_category', 'descricao', 'asset_class'])

    for item in items:
        writer.writerow([item.nome, item.quantity, item.preco, item.localidade, item.GL_category, item.descricao, item.asset_class])

    return response


@method_decorator(login_required, name='dispatch')
class LocalidadeCreateView(CreateView):
  model = Localidade
  form_class = Localform
  template_name = 'local_form.html'
  success_url = '/itens/'


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Nome do template de login (deve estar em templates/registration/)
    success_url = '/itens/'


class CustomLogoutView(LogoutView):
    success_url = '/login/'
    template_name = 'logout.html'


@method_decorator(login_required, name='dispatch')
class ItemDeleteView(DeleteView):
  model = Item
  success_url = reverse_lazy('item-list')
  template_name = 'item_confirm_delete.html'


@method_decorator(login_required, name='dispatch')
class ItemDetailView(DetailView):
   model = Item
   template_name = 'item_detail.html'


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    def get(self, request):
        categoria = request.GET.get('categoria')
        filial = request.GET.get('filial')

        itens = Item.objects.all()

        if categoria:
            itens = itens.filter(GL_category=categoria)

        if filial:
            itens = itens.filter(localidade__id=filial)

        total_itens = itens.count()
        total_localidades = Item.objects.values('localidade').distinct().count()
        valor_total_estoque = sum(item.preco * item.quantity for item in itens)
        custo_medio = valor_total_estoque / total_itens if total_itens > 0 else 0

        categorias = itens.values('GL_category').annotate(count=Count('GL_category'))
        filiais = Localidade.objects.all()

        context = {
            'total_itens': total_itens,
            'total_localidades': total_localidades,
            'valor_total_estoque': valor_total_estoque,
            'custo_medio': custo_medio,
            'categorias': categorias,
            'itens': itens,
            'filiais': filiais,
            'heatmap_data': list(itens.values('nome', 'quantity').annotate(count=Count('id')))
        }
        return render(request, 'dashboard.html', context)


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_actions'] = UserActionLog.objects.filter(user=self.object).order_by('-action_date')
        return context


def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    UserActionLog.objects.create(user=request.user, action_type=f'Deleted item {item.name}')
    return redirect('item-list')


def update_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            UserActionLog.objects.create(user=request.user, action_type=f'Updated item {item.name}')
            return redirect('item-list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_form.html', {'form': form})



def localidade_list(request):
    localidades = Localidade.objects.all()
    return render(request, 'localidade_list.html', {'localidades': localidades})


@method_decorator(login_required, name='dispatch')
class LocalDetailView(DetailView):
   model = Localidade
   template_name = 'local_detail.html'
   context_object_name = 'localidade'


   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')

        if search_query:
            itens = Item.objects.filter(localidade=self.object, nome__icontains=search_query)
        else:
            itens = Item.objects.filter(localidade=self.object)

        itens = itens.order_by('-quantity')

        context['itens'] = itens
        context['total_itens'] = itens.count()
        context['valor_total_estoque'] = sum(item.valor_total for item in itens)
        return context

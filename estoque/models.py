from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Localidade(models.Model):
  nome = models.CharField(max_length=100)

  def __str__(self):
    return self.nome

class Item(models.Model):
  nome = models.CharField(max_length=100)
  quantity = models.IntegerField()
  preco = models.DecimalField(max_digits=10, decimal_places=2)
  localidade = models.ForeignKey(Localidade, on_delete=models.CASCADE)
  data_criacao = models.DateTimeField(auto_now_add=True)
  data_atualizacao = models.DateTimeField(auto_now=True)
  criador_por = models.ForeignKey(User, on_delete=models.CASCADE)
  GL_category = models.CharField(max_length=100)
  descricao = models.CharField(max_length=250)
  asset_class = models.IntegerField()

  def __str__(self):
    return self.nome

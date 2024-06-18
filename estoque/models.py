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
  image = models.ImageField(upload_to='item_images/', blank=True, null=True)

  def __str__(self):
    return self.nome

  @property
  def valor_total(self):
    return self.quantity * self.preco


class UserActionLog(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  action_date = models.DateTimeField(auto_now_add=True)
  action_type = models.CharField(max_length=100)

  def __str__(self):
    return f"{self.user.username} - {self.action_type} at {self.action_date}"

from django import forms
from .models import Item, Localidade
from django.contrib.auth.models import User, Group


class Itemform(forms.ModelForm):
  class Meta:
    model = Item
    fields = ['nome', 'quantity', 'preco', 'localidade', 'GL_category', 'descricao', 'asset_class', 'image']


class UserCreationForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput)
  groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)

  class Meta:
    model = User
    fields = ['username', 'password', 'groups']

  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password'])
    if commit:
      user.save()
      self.save_m2m()
    return user


class Localform(forms.ModelForm):
  class Meta:
    model = Localidade
    fields = ['nome']

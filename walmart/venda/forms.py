# -*- coding: utf-8 -*-
from django import forms
from django.utils.formats import localize
from walmart.venda.models import Produto

####### FORM DE CADASTRO DE PRODUTO ######
class ProdutoForm(forms.ModelForm):
    nome = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    preco = forms.DecimalField(widget=forms.TextInput(attrs={"class": "form-control"}), localize=True)
    descricao = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Produto
        fields = '__all__'

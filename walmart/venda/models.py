# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import Decimal

TIPO_PAGAMENTO = (
    (1, ("Boleto")),
)

##### Tambem utilizado como endereco de Cobranca #####
class UserEndereco(models.Model):
    user = models.OneToOneField(User)
    endereco = models.CharField(max_length=100, default="Rua Zezinho")
    numero = models.CharField(max_length=20, default="111")
    bairro = models.CharField(max_length=20, default="Vila Junina")
    estado = models.CharField(max_length=2, default="SP")
    tel = models.CharField(max_length=15, default="(11)9999-9999")
    cep = models.CharField(max_length=9, default="12236-700")

class EnderecoEntrega(models.Model):
    user = models.OneToOneField(User)
    endereco = models.CharField(max_length=100, default="Rua Joaozinho")
    numero = models.CharField(max_length=20, default="222")
    bairro = models.CharField(max_length=20, default="Vila Sao Joao")
    estado = models.CharField(max_length=2, default="SP")
    cep = models.CharField(max_length=9, default="12236-720")

##### Modelo bem basico de produto #####
class Produto(models.Model):
    nome =  models.CharField(max_length=150)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    descricao = models.TextField(null=True, blank=True)
    foto = models.ImageField("Foto", upload_to='media/fotos/', blank = False)

    def __unicode__(self):
        return self.nome

    def get_preco(self):
        return self.preco


class Carrinho(models.Model):
    user = models.OneToOneField(User, null=True)
    criado = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __unicode__(self):
        return self.user.nome
	
	##### Calculo de descontos de acordo com o Enunciado ####
    def calcula_desconto(self):
        perc = 0
        if self.subtotal >= 500.00:
            perc = 0.05
        elif self.subtotal >= 600.00:
            perc = 0.1
        else:
            self.subtotal >= 700.00
            perc = 0.15
        self.desconto = self.subtotal * perc
        self.total = self.subtotal - self.desconto

	##### Metodo p/ calculo de total dos produtos ##### 
    def add_item_carrinho(self, produto, quantidade):
        item_carro = ItemCarrinho.objects.create(carrinho=self, produto=produto)
        self.subtotal = self.subtotal + quantidade * produto.preco
        item_carro.quantidade = quantidade
        item_carro.save()
        self.save()
	##### Metodo p/atualizar o subtotal de acordo com a quantidade ####
    def atualiza_subtotal(self):
        t = 0.00
        for item in ItemCarrinho.objects.all():
            t = t + float(item.quantidade) * float(item.produto.preco)
            self.subtotal = t
	
	#### Metodo para atualizar quantidade/deletar o item no carrinho #####
    def update_item_carrinho(self, produto, quantidade):
        self.save()
        item_carro = None
        try:
            item_carro = ItemCarrinho.objects.get(carrinho=self, produto=produto)
        except:
            item_carro = ItemCarrinho.objects.create(carrinho=self, produto=produto, quantidade=quantidade)
        if quantidade == 0:
            item_carro.delete()
        else:
            item_carro.quantidade = quantidade
            item_carro.save()
	##### Super save dos metodos Atualiza Subtotal e Calculo Desconto #####
    def save(self, *args, **kwargs):
        self.atualiza_subtotal()
        self.calcula_desconto()
        super(Carrinho, self ).save( *args, **kwargs )


class ItemCarrinho(models.Model):
    quantidade = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2, default=1.00)
    carrinho = models.ForeignKey(Carrinho, null=True, blank=True)
    produto = models.ForeignKey(Produto)

    def __unicode__(self):
        return self.produto.nome


class Pedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    carrinho = models.ForeignKey(Carrinho)
    cobranca = models.ForeignKey(UserEndereco, related_name='Cobranca')
    entrega = models.ForeignKey(EnderecoEntrega, related_name='Entrega')
    tipo_pagamento = models.IntegerField(choices=TIPO_PAGAMENTO, default=1)
    data_pedido = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.pedido_id

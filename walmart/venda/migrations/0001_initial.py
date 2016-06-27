# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criado', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('total', models.DecimalField(max_digits=8, null=True, decimal_places=2)),
                ('subtotal', models.DecimalField(max_digits=8, decimal_places=2, default=0)),
                ('desconto', models.DecimalField(max_digits=8, decimal_places=2, default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnderecoEntrega',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('endereco', models.CharField(max_length=100, default='Rua Joaozinho')),
                ('numero', models.CharField(max_length=20, default='222')),
                ('bairro', models.CharField(max_length=20, default='Vila Sao Joao')),
                ('estado', models.CharField(max_length=2, default='SP')),
                ('cep', models.CharField(max_length=9, default='12236-720')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('subtotal', models.DecimalField(max_digits=8, decimal_places=2, default=1.0)),
                ('carrinho', models.ForeignKey(to='venda.Carrinho', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_pagamento', models.IntegerField(choices=[(1, 'Boleto')], default=1)),
                ('data_pedido', models.DateTimeField(auto_now_add=True)),
                ('carrinho', models.ForeignKey(to='venda.Carrinho')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=150)),
                ('preco', models.DecimalField(max_digits=8, decimal_places=2)),
                ('descricao', models.TextField(null=True, blank=True)),
                ('foto', models.ImageField(verbose_name='Foto', upload_to='media/fotos/')),
            ],
        ),
        migrations.CreateModel(
            name='UserEndereco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('endereco', models.CharField(max_length=100, default='Rua Zezinho')),
                ('numero', models.CharField(max_length=20, default='111')),
                ('bairro', models.CharField(max_length=20, default='Vila Junina')),
                ('estado', models.CharField(max_length=2, default='SP')),
                ('tel', models.CharField(max_length=15, default='(11)9999-9999')),
                ('cep', models.CharField(max_length=9, default='12236-700')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='cobranca',
            field=models.ForeignKey(related_name='Cobranca', to='venda.UserEndereco'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='entrega',
            field=models.ForeignKey(related_name='Entrega', to='venda.EnderecoEntrega'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='itemcarrinho',
            name='produto',
            field=models.ForeignKey(to='venda.Produto'),
        ),
    ]

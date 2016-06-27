from django.contrib import admin
from walmart.venda.models import *

# Register your models here.
admin.site.register(Carrinho)
admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(EnderecoEntrega)
admin.site.register(UserEndereco)

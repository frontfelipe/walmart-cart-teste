# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from walmart.venda.forms import *
from walmart.venda.models import *
from django.core.exceptions import *

###### Exibe todos os produtos na Home ######
def produtos(request):
    try:
        produtos = Produto.objects.all()
    except:
        produtos = None
        carrinho = None
    try:
        carro_id = request.session['carrinho_id']
        carrinho = Carrinho.objects.get(id=carro_id)
    except:
        carrinho = None
    return render_to_response('home.html',
                              {'produtos':produtos,'carrinho':carrinho},
                              context_instance=RequestContext(request))


###### ADD Produto no Carrinho ######
def add_produto(request):
	form = ProdutoForm()
	msg = ''
	try:
		if request.method == "POST":
			form = ProdutoForm(request.POST, request.FILES)
			if form.is_valid():
				produto = form.save(commit=False)
				produto.save()
				msg = "Produto Cadastrado"
	except:
		return HttpResponseRedirect(reverse("produtos"))

	return render_to_response('cadastro_produto.html',
                              {'form':form,'msg':msg},
                              context_instance=RequestContext(request))

							  
###### Exibe Carrinho e produtos adicionados #####
def carrinho(request):
	context = None
	try:
		carro_id = request.session['carrinho_id']
		carrinho = Carrinho.objects.get(id=carro_id)
		context = {"carrinho": carrinho}
	except:
		carro_id = None
		msg_vazio = "Seu carrinho esta vazio!"
		context = {"vazio": True, "msg_vazio": msg_vazio}

	template = "carrinho.html"
	return render(request, template, context)

###### ADD Item ao Carrinho ######
def add_carrinho(request,pk):
	request.session.set_expiry(1)
	carro_id = request.session.get('carrinho_id')

	try:
		carro = Carrinho.objects.get(id=carro_id)
	except:
		carro = Carrinho()
		carro.save()
		request.session['carrinho_id'] = carro.id
		carro_id = carro.id

	try:
		produto = Produto.objects.get(pk=pk)
		if request.method == "POST":
			qtd = request.POST.get('quantidade', 1)
			carro.update_item_carrinho(produto, qtd)
			return HttpResponseRedirect(reverse("produtos"))
	except Produto.DoesNotExist:
		pass

	return render_to_response('carrinho.html',
                              context_instance=RequestContext(request))

''' Atualiza as infos dos produtos dentro do carrinho, 
usado no ajax do campo Quantidade '''
def update_carrinho(request):
	response_data = {}
	try:
		carro_id = request.session['carrinho_id']
		carrinho = Carrinho.objects.get(id=carro_id)
		produto_id = request.GET.get('produto_id')
		produto = Produto.objects.get(id=produto_id)
		item_carro = ItemCarrinho.objects.get(carrinho=carrinho, produto=produto)
		quantidade = request.GET.get('quantidade')
		carrinho.update_item_carrinho(item_carro.produto,quantidade)
		response_data['total'] = str(carrinho.total)
		response_data['subtotal'] = str(carrinho.subtotal)
		response_data['desconto'] = str(carrinho.desconto)
	except ObjectDoesNotExist:
		print ("Nao existe")
	return HttpResponse(json.dumps(response_data), content_type="application/json")

###### Remove Item do carrinho ######
def remover_do_carrinho(request, id):
	try:
		carro_id = request.session['carrinho_id']
		carrinho = Carrinho.objects.get(id=carro_id)
		item_carro = ItemCarrinho.objects.get(id=id)
		carrinho.update_item_carrinho(item_carro.produto.id,0)
	except:
		return HttpResponseRedirect(reverse("carrinho"))

	return HttpResponseRedirect(reverse("carrinho"))

	
'''Pela falta de tempo acabei utilizando o User/Admin do Django, 
Desculpe a falta de um Login/Perfil de usuario melhor '''
##### Finalizacao do carrinho e resumo do Pedido de Compra #####
@login_required
def checkout(request):
	cobranca = UserEndereco.objects.get(user=request.user)
	entrega = EnderecoEntrega.objects.get(user=request.user)
	msg = ""
	context = None
	try:
		carro_id = request.session['carrinho_id']
		carrinho = Carrinho.objects.get(id=carro_id)
	except:
		return HttpResponseRedirect(reverse("carrinho"))

	try:
		novo_pedido = Pedido.objects.get(carrinho=carrinho)
	except Pedido.DoesNotExist:
		novo_pedido = Pedido()
		novo_pedido.carrinho = carrinho
		novo_pedido.user = request.user
		novo_pedido.entrega = entrega
		novo_pedido.cobranca = cobranca
		novo_pedido.save()
	except:
		novo_pedido = None
		msg = "Seu carrinho esta vazio!"
		return HttpResponseRedirect(reverse("carrinho"))

	context = {
	"pedido": novo_pedido,
	"msg": msg,
	}
	template = "checkout.html"
	return render(request, template, context)

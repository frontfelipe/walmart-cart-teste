# Teste Walmart - Vaga FullStack Python/Django
Teste para o processo seletivo FullStack Walmart

#Requisitos mínimos do Teste:
 - Usuário pode criar mais de um produto com o Nome e Valor como requisitos mínimos.
 - Aplicação deve exibir todos os produtos cadastrados e permitir que o usuário altere a quantidade de cada produto que deseja comprar na tela de Carrinho.
 - A compra mínima (soma de todos os valores e quantidades dos produtos) deve ser de 200 reais, impossibilitando a ida para a tela de Conclusão de Compra no caso de valores menores.
Caso a compra total for maior que 400 reais, deve ser aplicado alguns dos descontos:
-Se maior que 500 reais, desconto de 5% no valor total da compra.
-Se maior que 600 reais, desconto de 10% no valor total da compra.
-Se maior que 700 reais, desconto de 15% no valor total da compra.
Caso seja entre 200 e 400 reais, não aplicar nenhum desconto.
Após os cálculos, exibir na tela de Conclusão de Compra o valor final da compra e o desconto obtido.

#Tecnologias Utilizadas
 - Python 3
 -- Utilizei python 3 porque ainda eu nao tinha utilizado e um projeto, sendo assim aproveitei o teste para ver o que tinha de novo em relacao ao python 2.7.

 - Django 1.8
 -- Utilizei Django porque é o framework que tenho mais dominio e isso iria me ajudar a produzir com mais rapidez o teste. 

#Design/Layout
 - Walmart web-style-guide https://walmartlabs.github.io/web-style-guide/
 -- Apos uma rapida pesquisa no google eu encontrei este guia de estilos do proprio Walmart EUA e vi que ficaria mais fiel ao layout do walmart Brasil se eu utilizasse.
 
#Requirements
Django==1.8.4

#Setup
- Banco: SQLITE3

- Initial Data
Foi criado uma fixture com os dados iniciais e tambem algumas imagens de produtos pre cadastrados (media/produtos)

         python manage.py loaddata /venda/fixtures/initial_data.json
         python manage.py makemigrations
         python manage.py migrate
         python manage.py runserver

#Observacoes
Tive 7 dias para produzir este teste e infelizmente por causa de um problema de saude que tive essa semana (pneumonia) acabei perdendo tempo para produzir,
sendo assim peço desculpas por eventuais erros no projeto...



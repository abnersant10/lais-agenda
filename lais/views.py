from tokenize import Name
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, UserManager
# Exibir mensagens ao usuario
from django.contrib import messages
# Autenticação Django e importar models
from lais.models import cidadao
# Biblioteca de validação de dados
from lais.validacoes import validaCPF, validaData
# extrair dados do XML
import xml.etree.ElementTree as ET


# Create your views here.


def login(request):
    if request.method == 'POST':
        return HttpResponse("aeeer")
    return render(request, "login.html")


def cadastro(request):
    # Receber os dados
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        nasc = request.POST.get('nasc')
        grp = request.POST.get('grp')
        teve_covid = request.POST.get('teve_covid')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
        print(grp)
        print(type(grp))
    # validar os dados recebidos
    # validar CPF
        salvar == True
        if validaCPF(cpf) == False:
            messages.error(request, 'CPF Inválido!')
            salvar = False

    # Validar a Data Nascimento
        if validaData(nasc) == False:
            messages.error(request, 'Data inválida | Menor de 18 anos!')
            salvar = False
    # Validar a senha
        if senha1 != senha2:
            messages.error(request, 'As senhas não conferem!')
            salvar = False
        if teve_covid == 'sim':
            messages.error(request, 'Você teve COVID nos ultimos 30 dias!')
            salvar = False
        if grp == "67" or grp == "65" or grp == "70":
            messages.error(
                request, 'Seu grupo de atendimento não permite cadastrar!')
            salvar = False
        if salvar == True:
            user = User.objects.create_user(
                username='nancy',
                password='opensesame',
                email='nancy@nancy.com')
            user.save()
            messages.success(
                request, 'Cadastro realizado com sucesso!')
    # extrair o nome do grupo de atendimento XML
    tree = ET.parse(
        'C:\\Users\\abner\Desktop\\backup\lais\\templates\\grupos_atendimento.xml')
    xml = tree.getroot()
    grp_atend = {}
    i = 1
    for filho in xml:
        grp_atend[str(i)] = filho[0].text
        i = i + 1

    # for ide in grp_atend:
    #    print(grp_atend[ide])
    # print(grp_atend)

    return render(request, "cadastro.html", {"grp_atend": grp_atend})
    # return HttpResponse(grp_atend)

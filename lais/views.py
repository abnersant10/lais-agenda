import http
from pyexpat import model
from urllib.request import Request
from django import views
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import *
from django.shortcuts import redirect
# Exibir mensagens ao usuario
from django.contrib import messages
# Autenticação Django e importar models
from lais.models import cidadao
# Biblioteca de validação de dados
from lais.validacoes import validaData
from validate_docbr import CPF
# extrair dados do XML
import xml.etree.ElementTree as ET
import datetime
import calendar

# Create your views here.


def home(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')
        # verrificar se CPF e Senha informada é igual no BD
        user = authenticate(request, username=cpf, password=senha)
        if user is not None:
            login(request, user)
            return redirect('pag_inicial')
        else:
            messages.error(request, 'CPF ou Senha Incorreta!')
    return render(request, "home.html")


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
    # validar os dados recebidos
    # validar CPF
        salvar = True
        _cpf = CPF()
        if _cpf.validate(cpf) == False:
            messages.error(request, 'CPF Inválido!')
            salvar = False

    # Validar a Data Nascimento
        if validaData(nasc) == False:
            messages.error(request, 'Data inválida ou Menor de 18 anos!')
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
        # Se o CPF NÃO estiver cadastrado, então salve os dados user
        if salvar and True:
            try:
                user = User.objects.create_user(
                    username=cpf,
                    password=senha1,)
                user.save()
                cid = cidadao(nome=nome, cpf=user, nasc=nasc,
                              grp_atend=grp, teve_covid=teve_covid, senha=senha1)
                cid.save()
                messages.success(
                    request, 'Cadastro realizado com sucesso!')
            except:
                messages.error(
                    request, 'CPF inválido ou já está cadastrado')
                salvar = False
    # extrair o nome do grupo de atendimento XML
    tree = ET.parse(
        'C:\\Users\\abner\\Desktop\\lais-agenda\\lais\\templates\\grupos_atendimento.xml')
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


def pag_inicial(request):
    if request.user.is_authenticated == True:
        cpf = request.user.username
        x = 0
        # x = cidadao.objects.values_list('nome', 'cpf', 'cpf_id')
        # x = cidadao.objects.all().values('nome', 'cpf__username')
        user = list(cidadao.objects.filter(
            cpf__username=request.user.username).values_list('nome', 'nasc', 'teve_covid', 'grp_atend'))
        # print(cpf)
        # print(user)
        dias_ano = 365.2425
        idade = int((datetime.date.today() - user[0][1]).days / dias_ano)
        context = {
            'nome': str(user[0][0]),
            'cpf': str(cpf),
            'nasc': (user[0][1]),
            # adicionar biblioteca date pegar idade
            'idade': str(idade)
        }
        return render(request, 'pag_inicial.html', context)
    else:
        return redirect('/')  # não estando autenticado volta pra home

# Logout


def logout_view(request):
    logout(request)
    return redirect('/')


def agendamento(request):
    if request.user.is_authenticated == True:
        cpf = request.user.username
        x = 0
        # x = cidadao.objects.values_list('nome', 'cpf', 'cpf_id')
        # x = cidadao.objects.all().values('nome', 'cpf__username')
        user = list(cidadao.objects.filter(
            cpf__username=request.user.username).values_list('nome', 'nasc', 'teve_covid', 'grp_atend'))
        # print(cpf)
        # print(user)
        tree = ET.parse(
            'C:\\Users\\abner\\Desktop\\lais-agenda\\lais\\templates\\estabelecimentos_pr.xml')
        xml = tree.getroot()
        unidades = {}
        for filho in xml:
            unidades[filho[6].text] = filho[1].text

        dias_ano = 365.2425
        idade = int((datetime.date.today() - user[0][1]).days / dias_ano)
        context = {
            'nome': str(user[0][0]),
            'cpf': str(cpf),
            'nasc': (user[0][1]),
            # adicionar biblioteca date pegar idade
            'idade': str(idade),
            'unidades': unidades
        }
        if request.method == "POST":
            cod_unid = request.POST.get('unidade')
            data = request.POST.get('data')
            hora = request.POST.get('hora')
            print(cod_unid)
            print(data)
            print(hora)

        return render(request, 'agendamento.html', context)
    else:
        return redirect('/')  # não estando autenticado volta pra home

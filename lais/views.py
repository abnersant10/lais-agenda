import http
from pyexpat import model
from urllib.request import Request
from django import views
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import *
from django.shortcuts import redirect
# Exibir mensagens ao usuario
from django.contrib import messages
# Autenticação Django e importar models
from lais.models import cidadao, agendado
# Biblioteca de validação de dados
from lais.validacoes import validaData
from validate_docbr import CPF
# extrair dados do XML
import xml.etree.ElementTree as ET
import datetime
import calendar
from time import sleep, time

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
        # if teve_covid == 'sim':
        #    messages.error(request, 'Você teve COVID nos ultimos 30 dias!')
        #    salvar = False
        # if grp == "67" or grp == "65" or grp == "70":
        #    messages.error(
        #        request, 'Seu grupo de atendimento não permite cadastrar!')
        #    salvar = False
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

    return render(request, "cadastro.html", {"grp_atend": grp_atend})


def pag_inicial(request):
    if request.user.is_authenticated == True:
        cpf = request.user.username
        user = list(cidadao.objects.filter(
            cpf__username=request.user.username).values_list('nome', 'nasc', 'teve_covid', 'grp_atend'))
        dias_ano = 365.2425
        idade = int((datetime.date.today() - user[0][1]).days / dias_ano)
        context = {
            'nome': str(user[0][0]),
            'cpf': str(cpf),
            'nasc': (user[0][1]),
            # adicionar biblioteca date pegar idade
            'idade': str(idade)
        }
        # pegar a lista dos cpf agendados
        agendados = str(agendado.objects.values_list('cpf'))
        # se o CPF do usuário estiver na lista dos CPFS agendados não pode agendar
        if cpf in agendados:
            messages.error(
                request, 'O seu CPF já foi cadastrado na lista agendamento do sistema, contate do administrador para liberar um novo agendamento')
        elif user[0][2] == 'sim':
            messages.error(
                request, 'Não está apto  para agendafmento, você teve covid nos ultimos 30 dias!')
        # se pertencer a um dos 3 grupos não realize agendamento
        elif user[0][3] == '65' or user[0][3] == '67' or user[0][3] == '70':
            messages.error(
                request, 'Não é permitido agendar para seu grupo de atendimento!')
        else:
            messages.success(
                request, 'Está apto para fazer o primeiro agendamento, clique no botão para ir para página de agendamento')
        # print(user[0][1])
        # se teve covid nos ultimos 30 dias

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
        salvar = True
        # x = cidadao.objects.values_list('nome', 'cpf', 'cpf_id')
        # x = cidadao.objects.all().values('nome', 'cpf__username')
        user = list(cidadao.objects.filter(
            cpf__username=request.user.username).values_list('nome', 'nasc', 'teve_covid', 'grp_atend'))

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
            # debug test
            # se for hoje ou domingo, segunda ou terça (não cadastre)
            data = datetime.datetime.strptime(data, "%Y-%m-%d")
            if data <= datetime.datetime.today() or calendar.day_name[data.weekday()] == ('Sunday' or 'Monday' or 'Tuesday'):
                salvar = False
                messages.error(
                    request, 'Esta data não é permitida')

            # se for 13 horas e idade tiver fora do intervalo (18-29) não cadastrar
            if hora == '13' and not (18 <= idade <= 29):
                salvar = False
                messages.error(
                    request, '13:00 é reservado para idades 18-29 anos!')
            if hora == '14' and not (30 <= idade <= 39):
                salvar = False
                messages.error(
                    request, '14:00 é reservado para idades 30 - 39 anos!')
            if hora == '15' and not (40 <= idade <= 49):
                salvar = False
                messages.error(
                    request, '15:00 é reservado para idades 40 - 49 anos!')
            if hora == '16' and not (50 <= idade <= 59):
                salvar = False
                messages.error(
                    request, '16:00 é reservado para idades 50 - 59 anos!')
            if hora == '17' and not (idade >= 60):
                salvar = False
                messages.error(
                    request, '16:00 é reservado para 60 anos ou mais!')
            # se pertencer aos grupos restritos ou tiver covid nos ultimos 30 dias então voltar pra pagina inicial
            if user[0][3] == '65' or user[0][3] == '67' or user[0][3] == '70':
                return redirect('pag_inicial')
            if user[0][2] == 'sim':
                return redirect('pag_inicial')
            # se o nom_und tiver cadasterado no BD
            ag_bd = (agendado.objects.values_list('nome_und', 'ag_data'))

            nome_unid = list(unidades.keys())[list(
                unidades.values()).index(cod_unid)]
            # agendamentos disponivels se nome_und dia e hora baterem
            ag_disp = {13: 0, 14: 0, 15: 0, 16: 0, 17: 0}
            for ind in ag_bd:
                # se o nome da unidade == nome_und (BD) então:
                if nome_unid == ind[0]:
                    # se data informada == data BD etão
                    if data.date() == ind[1].date():
                        # se a hora inforamda == hora BD então:
                        if hora == str(ind[1].hour):
                            ag_disp[int(ind[1].hour)] = ag_disp[int(
                                ind[1].hour)] + 1
            # se tiver vaga no horario cadastre
            print(ag_disp[int(hora)])
            print(salvar)
            if ag_disp[int(hora)] < 5 and salvar == True:
                agend = agendado(
                    cod_und=int(cod_unid), nome_und=nome_unid, cpf=cpf, ag_data=datetime.datetime(int(data.year), int(data.month), int(data.day), int(hora)))
                agend.save()
                return redirect('listagem')
            elif ag_disp[int(hora)] > 5:
                messages.error(
                    request, 'Não há mais vagas neste horario!')

        agendados = str(agendado.objects.values_list('cpf'))
        # se o CPF do usuário estiver na lista dos CPFS agendados não pode agendar
        if cpf in agendados:
            # não pode agendar então volta p pagina inicial
            return redirect('pag_inicial')
        # if teve covid if pertence ao grupo => voltar p pagina inicial

        return render(request, 'agendamento.html', context)
    else:
        return redirect('/')  # não estando autenticado volta pra home


def listagem(request):
    if request.user.is_authenticated == True:
        agend = agendado.objects.values_list('ag_data', 'cod_und', 'nome_und')

        today = datetime.datetime.now()
        context = {
            'agend': agend,
            'today': today
        }
        return render(request, 'listagem.html', context)
    else:
        return redirect('/')  # não estando autenticado volta pra home


def administrativo(request):
    if request.user.is_authenticated == True and request.user.is_superuser:
        # listar as unidades XML
        resp_nome = {}
        resp_cod = {}
        tree = ET.parse(
            'C:\\Users\\abner\\Desktop\\lais-agenda\\lais\\templates\\estabelecimentos_pr.xml')
        xml = tree.getroot()
        unidades = {}
        for filho in xml:
            unidades[filho[6].text] = filho[1].text

        if request.method == "POST":
            nome_rec = request.POST.get('nome_est')
            cod_rec = request.POST.get('cod_est')

        # valores de busca do nome digitado
            if len(nome_rec) != 0:
                for nome in unidades:
                    if nome_rec in nome:
                        resp_nome[nome] = unidades[nome]

            # retorna valor do codigo digitado
            for cod in unidades:
                print(cod_rec)
                print(unidades[cod])
                if cod_rec == unidades[cod]:
                    resp_cod[cod] = cod_rec
        context = {
            'unidades': unidades,
            'resp_cod': resp_cod,
            'resp_nome': resp_nome
        }
        if len(resp_cod) != 0:
            messages.success(
                request, 'Resultado : Codigo: ')
        if len(resp_nome) != 0:
            messages.info(
                request, 'Resultado : Nome: ')

        return render(request, 'administrativo.html', context)
    else:
        return redirect('/')  # não estando autenticado volta pra home

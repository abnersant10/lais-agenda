from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, Template
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
        # return HttpResponse(grp)
    # tratar os dados recebidos

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

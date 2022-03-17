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
    # extrair o nome do grupo de atendimento XML
    tree = ET.parse(
        'C:\\Users\\abner\Desktop\\backup\lais\\templates\\grupos_atendimento.xml')
    xml = tree.getroot()

    grp_atend = {71: "Casinha "}
    i = 1
    for filho in xml:
        grp_atend[i] = filho[0].text
        i = i + 1
    return render(request, "cadastro.html", grp_atend)

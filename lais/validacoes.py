import datetime
from xml.dom import ValidationErr
# Função para validar o CPF


def validaCPF(CPF):
    cpf = []
    primeiroDigito = []
    segundoDigito = []
    for n in CPF:
        cpf.append(int(n))
    tam = len(cpf)
    if tam > 11 or tam < 11:
        return False
    # Contadores
    i = 0
    # posição igual
    psi = 0
    # primeiro Digito
    pd = 10
    # segundo Digito
    sd = 11
    # Flag
    igual = False

    # Verifica se todos os digitos são iguais
    while psi < (11-1):
        if (cpf[psi] == cpf[psi+1]) and (cpf[psi-1] == cpf[psi]):
            igual = True
        psi += 1

    if igual:
        return False

    # Percorre o vetor cpf e multiplica cada posição de 10 até 2. Após percorrer, adiciona esses novos valores no vetor primeiroDigito
    while i < 9:
        primeiroDigito.append(cpf[i]*pd)
        i += 1
        pd -= 1
    # print(cpf[0:9:1])
    # print(primeiroDigito)

    # Está fazendo a soma dos números, que estão dentro do vetor primeiroDigito e multiplicando por 10, e depois pegando o resto da divisão por 11

    soma = (sum(primeiroDigito)*10) % 11
    if soma == cpf[9]:
        i = 0
        while i < 10:
            segundoDigito.append(cpf[i]*sd)
            i += 1
            sd -= 1
        somaSD = (sum(segundoDigito)*10) % 11
        if somaSD == cpf[10]:
            return True
        else:
            return False
    else:
        return False
# Função pra validar a Data


def validaData(data):
    try:
        data = datetime.date.fromisoformat(data)
    except ValueError or AttributeError:
        return False
    dias_ano = 365.2425
    idade = int((datetime.date.today() - data).days / dias_ano)
    if idade >= 18:
        return True
    else:
        return False

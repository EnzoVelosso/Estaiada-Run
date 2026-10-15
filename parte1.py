def obter_idade():
    while True:
        try:
            idade = int(input("Digite a idade: "))
            if idade >= 0:
                return idade
            print("A idade não pode ser negativa.")
        except ValueError:
            print("Digite uma idade válida usando números inteiros.")


def obter_distancia():
    while True:
        distancia = input("Escolha a distância (5 ou 10 km): ").strip()
        if distancia in ("5", "10"):
            return int(distancia)
        print("Distância inválida! Digite 5 ou 10.")


def obter_lote():
    while True:
        lote = input("Escolha o lote (1 ou 2): ").strip()
        if lote in ("1", "2"):
            return int(lote)
        print("Lote inválido! Digite 1 ou 2.")


def calcular_valor_inscricao(idade, distancia, lote):
    valor = 80 if lote == 1 else 100

    if distancia == 10:
        valor += 20

    if idade >= 60:
        valor /= 2

    return valor


def obter_categoria(idade):
    if 16 <= idade <= 19:
        return "Juvenil"
    elif 20 <= idade <= 39:
        return "Adulto"
    elif 40 <= idade <= 59:
        return "Master"
    elif idade >= 60:
        return "Veterano"
    else:
        return "Não elegível"


def gerar_codigo(nome, idade):
    partes = nome.strip().split()
    primeiro_nome = partes[0]
    ultimo_sobrenome = partes[-1]

    codigo = (
        primeiro_nome[:3] +
        ultimo_sobrenome[:3] +
        str(idade)
    )

    return codigo.upper()


def obter_primeiro_nome(nome):
    nome = nome.strip()
    posicao = nome.find(" ")
    if posicao == -1:
        return nome

    return nome[:posicao]


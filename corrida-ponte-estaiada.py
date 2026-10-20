CATEGORIAS = (
    ("Juvenil", 16, 19, 25 * 60, 52 * 60),
    ("Adulto", 20, 39, 22 * 60, 46 * 60),
    ("Master", 40, 59, 25 * 60, 52 * 60),
    ("Veterano", 60, 150, 30 * 60, 63 * 60)
)

#ENTRADA DE INFORMAÇOES

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
        return "Inválido"

def obter_primeiro_nome(nome):
    nome = nome.strip()
    posicao = nome.find(" ")
    if posicao == -1:
        return nome
    return nome[:posicao]

def receber_tempo():
    while True:
        tempo = input("DIgite o tempo desta maneira (HH:MM:SS): ").strip()
        segundos = tempo_em_segundos(tempo)
        if segundos:
            return segundos
        print("Digite desta maneira (HH:MM:SS)")

#REGRAS DE NEGÓCIO

def calcular_valor_inscricao(idade, distancia, lote):
    valor = 80 if lote == 1 else 100

    if distancia == 10:
        valor += 20
    if idade >= 60:
        valor /= 2

    return valor

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

def tempo_em_segundos(tempo):
    partes = tempo.split(":")
    if tempo.count(":") != 2:
        return None

    horas = int(partes[0])
    minutos = int(partes[1])
    segundos = int(partes[2])

    if minutos > 59 or segundos > 59:
        return None
    total = horas * 3600 + minutos * 60 + segundos
    return total

def calcular_pace(segundos, distancia):
    segundos_km = segundos // distancia
    minutos_pace = int(segundos_km // 60)
    segundos_restantes = int(segundos_km % 60)

    return f"{minutos_pace}'{segundos_restantes:02d}"


def verificar_premiacao(categoria, distancia, segundos):
    if categoria == "Juvenil":
        if distancia == 5:
            valor_maximo = 25 * 60
        else:
            valor_maximo = 52 * 60

    elif categoria == "Adulto":
        if distancia == 5:
            valor_maximo = 22 * 60
        else:
            valor_maximo = 46 * 60

    elif categoria == "Master":
        if distancia == 5:
            valor_maximo = 25 * 60
        else:
            valor_maximo = 52 * 60

    elif categoria == "Veterano":
        if distancia == 5:
            valor_maximo = 30 * 60
        else:
             valor_maximo = 63 * 60
    return segundos <= valor_maximo

def realizar_inscrição():
    nome = input("Digite seu nome completo: ").strip()
    while not nome:
        print("Nome vazio!")
        nome = input("Digite seu nome completo: ").strip()

    idade = obter_idade()

    if idade < 16:
        print("Idade mínima de 16 anos!")
        return None

    distancia = obter_distancia()
    lote = obter_lote()

    categoria = obter_categoria(idade)
    codigo = gerar_codigo(nome, idade)
    primeiro_nome = obter_primeiro_nome(nome)
    valor = calcular_valor_inscricao(idade, distancia, lote)

    print("== Dados da Inscrição ==")
    print(f"Nome: {primeiro_nome}")
    print(f"Código: {codigo}")
    print(f"Categoria: {categoria}")
    print(f"Distância: {distancia} km")
    print(f"Valor a pagar: R$ {valor:.2f}")

    return codigo

def calcular_resultado():
    idade = obter_idade()

    if idade < 16:
        print("Idade abaixo da mínima para participar da corrida.")
        return

    distancia = obter_distancia()
    tempo_segundos = receber_tempo()

    categoria = obter_categoria(idade)
    pace = calcular_pace(tempo_segundos, distancia)

    premiado = verificar_premiacao(
        categoria, distancia, tempo_segundos
    )

    print("\n== RESULTADO DA PROVA ==")
    print(f"Categoria: {categoria}")
    print(f"Distância: {distancia} km")
    print(f"Tempo em segundos: {tempo_segundos}")
    print(f"Pace: {pace}")

    if premiado:
        print("Premiado: Sim")
    else:
        print("Premiado: Não")

    print("==")

def obter_opcao_menu():
    while True:
        opcao = input(
            "\n1 - Fazer inscrição\n"
            "2 - Calcular resultado\n"
            "3 - Sair\n"
            "Escolha uma opção: "
        ).strip()

        if opcao in ("1", "2", "3"):
            return opcao

        print("Opção inválida! Escolha 1, 2 ou 3.")

def main():
    quantidade_incritos = 0
    valor_arrecadado = 0.0

    while True:
      opcao = obter_opcao_menu()

      if opcao == "1":
        inscricao = realizar_inscrição()

      elif opcao == "2":
        calcular_resultado()

      elif opcao == "3":
        print(f"total de inscrições: {quantidade_incritos}")    
        print(f"total arrecadado: {valor_arrecadado}")
        print("Sistema encerrado")
        break
     
main()

def listar_categorias(corredores):
    contagem = {
        "Juvenil": 0,
        "Adulto": 0,
        "Master": 0,
        "Veterano": 0
    }
    for corredor in corredores:
        categoria = corredor["categoria"]
        contagem[categoria] += 1

    print(" INSCRITOS POR CATEGORIA ")
    for categoria, quantidade in contagem.items():
        print(f"{categoria}: {quantidade}")
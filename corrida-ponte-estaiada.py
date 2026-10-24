#CONSTANTES DO SISTEMA
CATEGORIAS = (
    ("Juvenil", 16, 19, 25 * 60, 52 * 60),
    ("Adulto", 20, 39, 22 * 60, 46 * 60),
    ("Master", 40, 59, 25 * 60, 52 * 60),
    ("Veterano", 60, 150, 30 * 60, 63 * 60)
)

# RECEBER INFORMAÇÕES

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

def receber_tempo():
    while True:
        tempo = input("DIgite o tempo desta maneira (HH:MM:SS): ").strip()
        segundos = tempo_em_segundos(tempo)
        if segundos:
            return segundos
        print("Digite desta maneira (HH:MM:SS)")

def obter_opcao_menu():
    print("1 - Fazer inscrição")
    print("2 - Buscar corredor pelo código")
    print("3 - Registrar tempo de prova")
    print("4 - Quantidade por categoria")
    print("5 - Listar inscritos")
    print("6 - Calcular resultado")
    print("7 - Sair")

    opcao = input("Escolha uma opção: ").strip()

    while opcao not in ("1", "2", "3", "4", "5", "6", "7"):
        print("Opção inválida! Tente novamente.")
        opcao = input("Escolha uma opção: ").strip()

    return opcao

# REGRAS DE NEGÓCIO

def identificar_categoria(idade):
    for categoria, idade_minima, idade_maxima, limite_5km, limite_10km in CATEGORIAS:
        if idade_minima <= idade <= idade_maxima:
            return categoria
    return "Inválido"

def obter_primeiro_nome(nome):
    nome = nome.strip()
    posicao = nome.find(" ")
    if posicao == -1:
        return nome
    return nome[:posicao]

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

    codigo = (primeiro_nome[:3] + ultimo_sobrenome[:3] + str(idade))
    return codigo.upper()

def converter_segundos_tempo(segundos):
    minutos_totais = segundos // 60

    horas = minutos_totais // 60
    minutos = minutos_totais % 60
    segundos_restantes = segundos % 60

    return f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"

def tempo_em_segundos(tempo):
    if tempo[2:3] != ":" or tempo[5:6] != ":":
        return None
    if tempo[7:8] == "" or tempo[8:] != "":
        return None
    horas_texto = tempo[:2]
    minutos_texto = tempo[3:5]
    segundos_texto = tempo[6:8]

    numeros = "0123456789"

    for caractere in horas_texto + minutos_texto + segundos_texto:
        if caractere not in numeros:
            return None
    horas = int(horas_texto)
    minutos = int(minutos_texto)
    segundos = int(segundos_texto)
    if minutos > 59 or segundos > 59:
        return None
    return horas * 3600 + minutos * 60 + segundos

def formatar_tempo(segundos):
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    resto = segundos % 60
    return f"{horas:02d}:{minutos:02d}:{resto:02d}"

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

# DADOS DE CORREDORES 

def encontrar_corredor(corredores, codigo):
    codigo = codigo.strip().upper()
    encontrado = None

    for corredor in corredores:
        if corredor["codigo"] == codigo:
            encontrado = corredor
            break
    return encontrado

def exibir_corredor(corredor):
    print(f"Nome: {corredor['nome']}")
    print(f"Idade: {corredor['idade']}")
    print(f"Categoria: {corredor['categoria']}")
    print(f"Distância: {corredor['distancia']} km")
    print(f"Lote: {corredor['lote']}")
    print(f"Código: {corredor['codigo']}")
    print(f"Valor: R$ {corredor['valor']:.2f}")

    if corredor["tempo"] is None:
        print("Tempo: ainda não registrado")
        return

    tempo = corredor["tempo"]
    pace = calcular_pace(tempo, corredor["distancia"])
    premiado = verificar_premiacao(corredor["categoria"], corredor["distancia"],tempo)

    print(f"Tempo: {converter_segundos_tempo(tempo)} ({tempo} segundos)")
    print(f"Pace: {pace}/km")
    print(f"Premiado: {'Sim' if premiado else 'Não'}")

def buscar_corredor_por_codigo(corredores, codigo):
    for corredor in corredores:
        if corredor["codigo"] == codigo.strip().upper():
            return corredor

def buscar_corredor(corredores):
    codigo = input("Digite o código do corredor: ").strip().upper()
    corredor = buscar_corredor_por_codigo(corredores, codigo)

    if corredor is None:
        print("Nenhum corredor encontrado com esse código.")
        return
    print("Corredor encontrado")
    exibir_corredor(corredor)

def listar_inscritos(corredores):
    if not corredores:
        print("Ainda não existem corredores inscritos.")
        return

    print("\n== LISTA DE INSCRITOS ==")

    for corredor in corredores:
        print("\n-------------------------")
        exibir_corredor(corredor)

# FUNCIONALIDADES DA CORRIDA 

def realizar_inscrição(corredores):
    nome = input("Digite seu nome completo: ").strip()
    while not nome:
        print("Nome vazio!")
        nome = input("Digite seu nome completo: ").strip()

    idade = obter_idade()
    if idade < 16:
        print("Idade mínima de 16 anos!")
        return

    distancia = obter_distancia()
    lote = obter_lote()

    categoria = identificar_categoria(idade)
    codigo = gerar_codigo(nome, idade)
    valor = calcular_valor_inscricao(idade, distancia, lote)

    # Cada corredor é armazenado em um dicionário.
    corredor = {
        "nome": nome,
        "idade": idade,
        "categoria": categoria,
        "distancia": distancia,
        "lote": lote,
        "codigo": codigo,
        "valor": valor,
        "tempo": None}
    
    # O dicionário é adicionado à lista de corredores.
    corredores.append(corredor)
    print("\n== DADOS DA INSCRIÇÃO ==")
    print(f"Nome: {obter_primeiro_nome(nome)}")
    print(f"Código: {codigo}")
    print(f"Categoria: {categoria}")
    print(f"Distância: {distancia} km")
    print(f"Lote: {lote}")
    print(f"Valor a pagar: R$ {valor:.2f}")
    print("Inscrição realizada com sucesso!")

def registrar_tempo(corredores):
    print("--- Registrar tempo de prova ---")
    codigo = input("Digite o código do corredor: ").strip().upper()
    corredor = buscar_corredor_por_codigo(corredores, codigo)
    if corredor is None:
        print("Código não encontrado. Cadastre o corredor.")
        return
    
    tempo_segundos = receber_tempo()
    corredor["tempo"] = tempo_segundos
    print("Tempo registrado!")
    exibir_corredor(corredor)

def quantidade_por_categoria(corredores):
    quantidades = {}

    for categoria, idade_minima, idade_maxima, limite_5km, limite_10km in CATEGORIAS:
        quantidades[categoria] = 0

    for corredor in corredores:
        quantidades[corredor["categoria"]] += 1

    return quantidades

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

def exibir_quantidade_por_categoria(corredores):
    quantidades = quantidade_por_categoria(corredores)

    print("\n--- Inscritos por categoria ---")
    for categoria, quantidade in quantidades.items():
        print(f"{categoria}: {quantidade}")


def calcular_resultado():
    idade = obter_idade()

    if idade < 16:
        print("Idade abaixo da mínima para participar da corrida.")
        return

    distancia = obter_distancia()
    tempo_segundos = receber_tempo()

    categoria = identificar_categoria(idade)
    pace = calcular_pace(tempo_segundos, distancia)

    premiado = verificar_premiacao(
        categoria, distancia, tempo_segundos
    )

    print("== RESULTADO DA PROVA ==")
    print(f"Categoria: {categoria}")
    print(f"Distância: {distancia} km")
    print(f"Tempo em segundos: {tempo_segundos}")
    print(f"Pace: {pace}")

    if premiado:
        print("Premiado: Sim")
    else:
        print("Premiado: Não")

    print("==")

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

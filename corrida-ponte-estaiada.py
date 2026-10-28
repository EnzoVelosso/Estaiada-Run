#CONSTANTES DO SISTEMA
'''Os tempos-limites são listados em segundos para facilitar as comparações
None na idade máxima significa que a categoria não tem limite.'''
CATEGORIAS = (
    ("Juvenil", 16, 19, 25 * 60, 52 * 60),
    ("Adulto", 20, 39, 22 * 60, 46 * 60),
    ("Master", 40, 59, 25 * 60, 52 * 60),
    ("Veterano", 60, None, 30 * 60, 63 * 60)
)
DISTANCIAS = (5, 10)

# RECEBER INFORMAÇÕES
# as funções abaixo conversam com o usuário e validam o que foi digitado.

def obter_nome_completo():
    """Solicita um nome com pelo menos um espaço entre nome e sobrenome."""
    while True:
        nome = input("Digite seu nome completo: ").strip()
        if nome and " " in nome:
            return nome
        print("Digite o nome completo, incluindo o sobrenome.")

def obter_idade():
    '''Solicita idade.'''
    while True:
        try:
            idade = int(input("Digite a idade: "))
            if idade >= 0:
                return idade
            print("A idade não pode ser negativa.")
        except ValueError:
            print("Digite uma idade válida usando números inteiros.")

def obter_distancia():
    '''Solicita a distancia(5 ou 10).'''
    while True:
        distancia = input("Escolha a distância (5 ou 10 km): ").strip()
        if distancia in ("5", "10"):
            return int(distancia)
        print("Distância inválida! Digite 5 ou 10.")

def obter_lote():
    '''Solicita um lote válido'''
    while True:
        lote = input("Escolha o lote (1 ou 2): ").strip()
        if lote in ("1", "2"):
            return int(lote)
        print("Lote inválido! Digite 1 ou 2.")

def receber_tempo():
    '''Solicita tempo no modelo HH:MM:SS'''
    while True:
        tempo = input("DIgite o tempo desta maneira (HH:MM:SS): ").strip()
        segundos = tempo_em_segundos(tempo)
        if segundos:
            return segundos
        print("Digite desta maneira (HH:MM:SS)")

def obter_opcao_menu():
    '''Exibe o menu principal com escolhas apartir de enumeração em texto.'''
    print("========== CORRIDA NOTURNA DA PONTE ESTAIADA ==========")
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
# Estas funções recebem dados por parâmetros e retornam resultados.

def identificar_categoria(idade):
    """Retorna a categoria da idade ou Inválido quando não existe categoria."""
    for categoria, idade_minima, idade_maxima, limite_5km, limite_10km in CATEGORIAS:
        if idade_minima <= idade <= idade_maxima:
            return categoria
    return "Inválido"

def obter_primeiro_nome(nome):
    """Retorna o primeiro nome usando slicing."""
    nome = nome.strip()
    posicao = nome.find(" ")
    if posicao == -1:
        return nome
    return nome[:posicao]

def calcular_valor_inscricao(idade, distancia, lote):
    """Calcula o preço considerando lote, distância e desconto por idade."""
    if lote == 1:
            valor = 80.0
    else:
            valor = 100.0
    # A prova de 10 km tem acréscimo antes da aplicação do desconto.
    if distancia == 10:
            valor += 20.0
    # Pessoas com 60 anos ou mais pagam metade do valor total.
    if idade >= 60:
            valor /= 2
    return valor

def gerar_codigo(nome, idade):
    '''Gera código por slicing do nome
    O formato usa três letras do primeiro nome, três do último sobrenome e a idade.'''
    partes = nome.strip().split()
    primeiro_nome = partes[0]
    ultimo_sobrenome = partes[-1]

    codigo = (primeiro_nome[:3] + ultimo_sobrenome[:3] + str(idade))
    return codigo.upper()

def converter_segundos_tempo(segundos):
    """Converte de segundos para HH:MM:SS."""
    minutos_totais = segundos // 60

    horas = minutos_totais // 60
    minutos = minutos_totais % 60
    segundos_restantes = segundos % 60

    return f"{horas:02d}:{minutos:02d}:{segundos_restantes:02d}"

def tempo_em_segundos(tempo):
    """Converte HH:MM:SS em segundos; retorna None se o formato for inválido.
    O fatiamento verifica as posições dos separadores e dos números."""

    # As duas verificações finais garantem que a string tenha exatamente 8 caracteres.
    if tempo[2:3] != ":" or tempo[5:6] != ":":
        return None
    if tempo[7:8] == "" or tempo[8:] != "":
        return None
    
    horas_texto = tempo[:2]
    minutos_texto = tempo[3:5]
    segundos_texto = tempo[6:8]
    numeros = "0123456789"

    # Todos os caracteres que representam tempo precisam ser algarismos.
    for caractere in horas_texto + minutos_texto + segundos_texto:
        if caractere not in numeros:
            return None
    horas = int(horas_texto)
    minutos = int(minutos_texto)
    segundos = int(segundos_texto)

    # Horas podem passar de 23, mas minutos e segundos devem ficar entre 00 e 59.
    if minutos > 59 or segundos > 59:
        return None
    return horas * 3600 + minutos * 60 + segundos

def calcular_pace(segundos, distancia):
    """Calcula o pace em minutos e segundos por quilômetro."""
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

def quantidade_por_categoria(corredores):
    quantidades = {}

    # Cria uma contagem inicial de zero para cada categoria.
    for categoria in CATEGORIAS:
        nome_categoria = categoria[0]
        quantidades[nome_categoria] = 0

    # Conta os corredores inscritos em cada categoria.
    for corredor in corredores:
        categoria = corredor["categoria"]
        quantidades[categoria] += 1

    return quantidades

def obter_premiados(corredores):
    premiados = []
    for corredor in corredores:

        # Ignora corredores que ainda não têm tempo registrado.
        if corredor["tempo"] is not None:

            categoria = corredor["categoria"]
            distancia = corredor["distancia"]
            tempo = corredor["tempo"]

            # Verifica se o corredor atingiu o limite de premiação.
            if verificar_premiacao(categoria, distancia, tempo):
                premiados.append(corredor)

    return premiados

def calcular_tempo_medio(corredores, distancia):
    """Retorna a média dos tempos registrados de uma distância, em segundos.
    Retorna None quando ainda não existem tempos registrados para a distância.
    """
    tempos = [
        corredor["tempo"] for corredor in corredores
        if corredor["distancia"] == distancia and corredor["tempo"] is not None
    ]

    if not tempos:
        return None
    return round(sum(tempos) / len(tempos))

def encontrar_corredor_mais_rapido(corredores, distancia):
    mais_rapido = None
    for corredor in corredores:

        # Considera somente corredores da distância escolhida
        if corredor["distancia"] == distancia and corredor["tempo"] is not None:

            # O primeiro corredor válido se torna o mais rápido.
            if mais_rapido is None:
                mais_rapido = corredor

            # Compara o tempo atual com o menor tempo encontrado.
            elif corredor["tempo"] < mais_rapido["tempo"]:
                mais_rapido = corredor

    return mais_rapido

def exibir_corredor(corredor):
    """Exibe os dados da inscrição e, se houver, o resultado do corredor."""
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
    """Procura um corredor pelo código e retorna seus dados, se encontrado."""
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
    """Exibe os corredores cadastrados."""
    if corredores:
        print("== LISTA DE INSCRITOS ==")
        for corredor in corredores:
            print("-------------------------")
            exibir_corredor(corredor)
    else:
        print("Ainda não existem corredores inscritos.")

# FUNCIONALIDADES DA CORRIDA 

def realizar_inscrição(corredores, codigo_usado):
    """Cadastra um corredor, calcula o valor e guarda seus dados na lista."""
    nome = input("Digite seu nome completo: ").strip()
    while not nome:
        print("Nome vazio!")
        nome = input("Digite seu nome completo: ").strip()
    #O cadastro é recusado abaixo de 16.
    idade = obter_idade()
    if idade < 16:
        print("Idade mínima de 16 anos!")
        return

    distancia = obter_distancia()
    lote = obter_lote()

    # O código é criado sem colisão e registrado no set para os próximos cadastros.
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
        "tempo": None # O tempo só será preenchido quando for registrado.
        }
    
    # O dicionário é adicionado à lista de corredores.
    corredores.append(corredor)
    print("== DADOS DA INSCRIÇÃO ==")
    print(f"Nome: {obter_primeiro_nome(nome)}")
    print(f"Código: {codigo}")
    print(f"Categoria: {categoria}")
    print(f"Distância: {distancia} km")
    print(f"Lote: {lote}")
    print(f"Valor a pagar: R$ {valor:.2f}")
    print("Inscrição realizada com sucesso!")

def registrar_tempo(corredores):
    """Registra o tempo de um corredor que já está inscrito."""
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

def exibir_quantidade_por_categoria(corredores):
    """Exibe a quantidade de inscritos em cada categoria."""

    quantidades = quantidade_por_categoria(corredores)
    print("--- INSCRITOS POR CATEGORIA ---")

    for categoria in quantidades:
        quantidade = quantidades[categoria]
        print(f"{categoria}: {quantidade}")

def obter_tempo_corredor(corredor):
    """Retorna o tempo de um corredor para ordenar a classificação."""
    return corredor["tempo"]

def exibir_classificacao_geral(corredores):
    """Exibe a classificação dos corredores por distância."""
    print("========== CLASSIFICAÇÃO GERAL ==========")

    for distancia in DISTANCIAS:
        participantes = []

        # Seleciona corredores da distância que já possuem tempo.
        for corredor in corredores:
            if corredor["distancia"] == distancia:
                if corredor["tempo"] is not None:
                    participantes.append(corredor)

        # Ordena os corredores do menor para o maior tempo.
        participantes.sort(key=obter_tempo_corredor)

        print(f"\n--- CLASSIFICAÇÃO: {distancia} km ---")

        if not participantes:
            print("Ainda não há tempos registrados para esta distância.")
        else:
            posicao = 1

            for corredor in participantes:
                tempo = converter_segundos_tempo(corredor["tempo"])
                pace = calcular_pace(corredor["tempo"], distancia)

                
                print(f"{posicao}º - {corredor['nome']} | ")
                print(f"{tempo} | Pace: {pace}/km | ")
                print(f"Código: {corredor['codigo']}")
                posicao += 1


def exibir_premiados(corredores):
    """Exibe os corredores que atingiram o limite de premiação."""
    print("========== CORREDORES PREMIADOS ==========")
    encontrou_premiado = False

    for corredor in corredores:
        if corredor["tempo"] is not None:

            categoria = corredor["categoria"]
            distancia = corredor["distancia"]
            tempo = corredor["tempo"]

            if verificar_premiacao(categoria, distancia, tempo):
                tempo_formatado = converter_segundos_tempo(tempo)

                print(
                    f"{corredor['nome']} | "
                    f"{categoria} | {distancia} km | "
                    f"{tempo_formatado}"
                )

                encontrou_premiado = True

    if not encontrou_premiado:
        print("Nenhum corredor atingiu o tempo-limite de premiação.")

def calcular_resultado(corredores):
    """Exibe a classificação geral, os premiados e os pódios da corrida."""
    # Verifica se pelo menos um corredor já possui tempo registrado.
    tempos_registrados = False

    for corredor in corredores:
        if corredor["tempo"] is not None:
            tempos_registrados = True
            break

    # Se nenhum corredor tiver tempo, não há resultados para exibir.
    if not tempos_registrados:
        print("Ainda não existem tempos registrados.")
        print("Registre os tempos antes de calcular os resultados.")
        return

    # Exibe os resultados da corrida.
    exibir_classificacao_geral(corredores)
    exibir_premiados(corredores)

 # MENU PRINCIPAL

def main():
    """Controla o menu e mantém a lista de corredores durante a execução."""
    corredores = []
    codigo_usados = set()
    while True :
      opcao = obter_opcao_menu()

      if opcao == "1" :
        realizar_inscrição(corredores, codigo_usados)

      elif opcao == "2" :
        buscar_corredor(corredores)

      elif opcao == "3" :
        registrar_tempo(corredores)

      elif opcao == "4" :
        quantidade_por_categoria(corredores)
        
      elif opcao == "5":
        listar_inscritos(corredores)
        
      elif opcao == "6":
        calcular_resultado()
        
      elif opcao == "7":
         # Os totais são acumulados no programa principal, conforme o enunciado.
        total_inscritos = len(corredores)
        total_arrecadado = sum(corredor["valor"] for corredor in corredores)

        print(f"Total de inscrições: {total_inscritos}")
        print(f"Total arrecadado: R$ {total_arrecadado:.2f}")
        print("Sistema encerrado.")
        break
     
main()
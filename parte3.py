def obter_idade():
    while True:
        try:
            idade = int(input("Digite a idade: "))
            if idade >= 0:
                return idade
            print("A idade não pode ser negativa.")
        except ValueError:
            print("Digite uma idade inteira válida.")


def obter_distancia():
    while True:
        distancia = input("Distância (5 ou 10 km): ").strip()
        if distancia in ("5", "10"):
            return int(distancia)
        print("Digite 5 ou 10.")
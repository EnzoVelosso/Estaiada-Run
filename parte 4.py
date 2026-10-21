def obter_tempo():
    while True:
        tempo = input("Digite o tempo (HH:MM:SS): ").strip()
        segundos = converter_tempo(tempo)

        if segundos is not None:
            return tempo, segundos

        print("Tempo inválido! Use o formato HH:MM:SS.")
        print("Exemplo: 00:21:30")


def calcular_pace(segundos_totais, distancia):
    if distancia not in (5, 10):
        raise ValueError("A distância deve ser 5 ou 10 km.")

    segundos_por_km = segundos_totais // distancia
    minutos = segundos_por_km // 60
    segundos = segundos_por_km % 60

    return f"{minutos}'{segundos:02d}\"/km"

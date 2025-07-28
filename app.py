import random
import streamlit as st
import matplotlib.pyplot as plt

# Constantes
CUSTO = 0
IMPACTO_AMBIENTAL = 1
VALORIZACAO = 2
CASAS = 3
DISTANCIA = 4
MOBILIDADE = 5
INFRAESTRUTURA = 6

MINIMO_VALORIZACAO = 20
MINIMO_CASAS = 15
MAXIMO_CUSTO = 250000

PESO_CASAS = 10
PESO_VALORIZACAO = 5
PESO_MOBILIDADE = 20
PESO_INFRA = 20
PESO_IMPACTO = 15
PESO_DISTANCIA = 10
DIVISOR_CUSTO = 1000


def gerar_terrenos(qtd=100):
    terrenos = []
    print(
        f"Valor máximo de custo: {int(MAXIMO_CUSTO * 1.3)}\n Valor mínimo de custo: {int(MAXIMO_CUSTO * 0.7)}"
    )
    for _ in range(qtd):
        custo = random.randint(int(MAXIMO_CUSTO * 0.7), int(MAXIMO_CUSTO * 1.3))
        impacto_ambiental = random.randint(1, 10)
        valorizacao = random.randint(5, 50)
        casas = random.randint(5, 30)
        distancia = random.randint(1, 20)
        mobilidade = random.randint(1, 10)
        infraestrutura = random.randint(1, 10)
        terrenos.append(
            [
                custo,
                impacto_ambiental,
                valorizacao,
                casas,
                distancia,
                mobilidade,
                infraestrutura,
            ]
        )
        print(
            f"Terreno gerado: {custo}, {impacto_ambiental}, {valorizacao}, {casas}, {distancia}, {mobilidade}, {infraestrutura}"
        )

    return terrenos


terrenos_todos = gerar_terrenos()
terrenos = [t for t in terrenos_todos if t[CUSTO] <= MAXIMO_CUSTO]

globalSelecionados = []
def avaliar(individuo):
    custo_total = 0
    impacto_total = 0
    valorizacao_total = 0
    casas_total = 0
    distancia_total = 0
    mobilidade_total = 0
    infraestrutura_total = 0
    selecionados = 0

    for i, gene in enumerate(individuo):
        if gene == 1:
            terreno = terrenos[i]
            custo_total += terreno[CUSTO]
            impacto_total += terreno[IMPACTO_AMBIENTAL]
            valorizacao_total += terreno[VALORIZACAO]
            casas_total += terreno[CASAS]
            distancia_total += terreno[DISTANCIA]
            mobilidade_total += terreno[MOBILIDADE]
            infraestrutura_total += terreno[INFRAESTRUTURA]
            selecionados += 1
            globalSelecionados.append(i)

    if selecionados == 0:
        return 0

    media_custo = custo_total / selecionados
    media_valorizacao = valorizacao_total / selecionados
    media_casas = casas_total / selecionados
    media_distancia = distancia_total / selecionados
    media_mobilidade = mobilidade_total / selecionados
    media_infra = infraestrutura_total / selecionados

    # print(
    #     f"Custo Total: {media_custo} -> {media_custo > MAXIMO_CUSTO}\n"
    #     f"Valorização Total: {media_valorizacao} -> {media_valorizacao < MINIMO_VALORIZACAO}\n"
    #     f"Casas Total: {media_casas} -> {media_casas < MINIMO_CASAS}\n"
    # )

    if (
        media_custo > MAXIMO_CUSTO
        or media_valorizacao < MINIMO_VALORIZACAO
        or media_casas < MINIMO_CASAS
    ):
        return 0

    fitness = (
        casas_total * PESO_CASAS
        + valorizacao_total * PESO_VALORIZACAO
        + media_mobilidade * PESO_MOBILIDADE
        + media_infra * PESO_INFRA
    ) - (
        impacto_total * PESO_IMPACTO
        + media_distancia * PESO_DISTANCIA
        + custo_total / DIVISOR_CUSTO
    )

    return fitness


def criar_individuo():
    return [random.randint(0, 1) for _ in range(len(terrenos))]


def cruzar(pai1, pai2):
    filho1 = []
    filho2 = []
    for g1, g2 in zip(pai1, pai2):
        if random.random() < 0.5:
            filho1.append(g1)
            filho2.append(g2)
        else:
            filho1.append(g2)
            filho2.append(g1)
    return filho1, filho2


def mutar(individuo):
    i = random.randint(0, len(individuo) - 1)
    individuo[i] = 1 - individuo[i]


def algoritmo_genetico(geracoes, tamanho_pop):
    populacao = [criar_individuo() for _ in range(tamanho_pop)]

    for _ in range(geracoes):
        populacao.sort(key=avaliar, reverse=True)
        nova_populacao = populacao[:2]

        while len(nova_populacao) < tamanho_pop:
            pai1 = random.choice(populacao[:5])
            pai2 = random.choice(populacao[:5])
            filho1, filho2 = cruzar(pai1, pai2)
            if random.random() < 0.1:
                mutar(filho1)
            if random.random() < 0.1:
                mutar(filho2)
            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao

    melhor = max(populacao, key=avaliar)
    print(f"Melhor indivíduo: {melhor} com fitness {avaliar(melhor)}")
    return melhor


# --- Streamlit Interface ---

st.title("Algoritmo Genético para Seleção de Terrenos")

geracoes = st.slider("Número de Gerações", 1, 100, 80)
tamanho_pop = st.slider("Tamanho da População", 2, 100, 50)

if st.button("Executar Algoritmo Genético"):
    st.write("Executando... isso pode levar alguns segundos.")
    melhor = algoritmo_genetico(geracoes, tamanho_pop)
    fitness = avaliar(melhor)
    st.write(f"**Fitness (qualidade):** {fitness:.2f}")
    st.write(f"**Quantidade terrenos escolhidos:** {sum(melhor):.2f}")

    # Extrair custos dos terrenos selecionados
    custos = [terrenos[i][CUSTO] for i, gene in enumerate(melhor) if gene == 1]
    indices = [i for i, gene in enumerate(melhor) if gene == 1]

    if custos:
        fig, ax = plt.subplots(figsize=(18, 8))
        ax.bar(range(len(custos)), custos, tick_label=indices, color='skyblue', edgecolor='black')
        ax.set_xlabel("Índice do Terreno")
        ax.set_ylabel("Custo (R$)")
        ax.set_title("Custos dos Terrenos Selecionados")
        st.pyplot(fig)
    else:
        st.write("Nenhum terreno selecionado para mostrar gráfico.")

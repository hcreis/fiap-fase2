import random
import streamlit as st
import pandas as pd


evolucao_fitness = []
custos_geracao = []

# Parâmetros do Algoritmo Genético
MIN_TERRAINS = 3  # Mínimo de terrenos a selecionar
MAX_TERRAINS = 5  # Máximo de terrenos a selecionar

CUSTO = 0
IMPACTO_AMBIENTAL = 1
VALORIZACAO = 2
CASAS = 3
DISTANCIA = 4
MOBILIDADE = 5
INFRAESTRUTURA = 6

MINIMO_VALORIZACAO = 20
MINIMO_CASAS = 15
MAXIMO_CUSTO = 2000000

PESO_CASAS = 10
PESO_VALORIZACAO = 5
PESO_MOBILIDADE = 20
PESO_INFRA = 20
PESO_IMPACTO = 15
PESO_DISTANCIA = 10
DIVISOR_CUSTO = 1000


# Passo 1: Definição do Problema
# O problema consiste em selecionar um subconjunto de terrenos que otimize critérios como custo, distância ao centro,
# impacto ambiental, acesso a transporte e infraestrutura, respeitando restrições de orçamento, número de terrenos
# (mínimo e máximo) e infraestrutura média mínima. Cada terreno é representado como um dicionário com atributos.


def gerar_terrenos(num_terrenos):
    terrenos = []
    for _ in range(num_terrenos):
        custo = random.randint(int(MAXIMO_CUSTO * 0.7), int(MAXIMO_CUSTO))
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
    return terrenos


# Passo 2: Representação dos Indivíduos (Codificação)
# Cada indivíduo é uma lista binária onde 1 indica que o terreno está selecionado e 0 indica que não está.
# A codificação garante que o número de terrenos selecionados esteja entre MIN_TERRAINS e MAX_TERRAINS.
def criar_individuo():
    # Passo 3: Inicialização da População
    # Cria uma população inicial de indivíduos aleatórios, cada um com 3 a 5 terrenos selecionados.
    # Usa random.sample para evitar repetições e garantir diversidade na população inicial.
    num_terrains = random.randint(MIN_TERRAINS, MAX_TERRAINS)
    individual = [0] * len(terrenos)
    selected_indices = random.sample(range(len(terrenos)), num_terrains)
    for idx in selected_indices:
        individual[idx] = 1
    return individual


# Passo 4: Cálculo da Função de Aptidão (Fitness Function)
# Avalia a qualidade de cada indivíduo com base em cinco critérios: custo, distância ao centro,
# impacto ambiental, acesso a transporte e infraestrutura. Penaliza soluções que violam restrições.
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

    if selecionados == 0:
        return 0

    media_valorizacao = valorizacao_total / selecionados
    media_casas = casas_total / selecionados

    if media_valorizacao < MINIMO_VALORIZACAO or media_casas < MINIMO_CASAS:
        return 0

    fitness = (
        casas_total * 0.30
        + valorizacao_total * 0.15
        + mobilidade_total * 0.25
        + infraestrutura_total * 0.25
    )
    return fitness


## Passo 5: Seleção por Torneio
# Seleciona o melhor indivíduo de um torneio entre k competidores aleatórios da população
# Isso garante diversidade genética e evita que indivíduos com fitness muito baixo sejam selecionados.
def torneio(populacao, k=3):
    # Seleciona k indivíduos aleatórios e retorna o melhor entre eles
    competidores = random.sample(populacao, k)
    melhor = max(competidores, key=avaliar)
    return melhor


# Passo 6: Cruzamento (Uniform Crossover) (Sem ordem sequencial)
# Realiza o cruzamento entre dois pais para gerar dois filhos. Cada gene é escolhido aleatoriamente de um dos pais.
# Isso garante que os filhos herdem características de ambos os pais
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
    filho1 = ajustar_selecao(filho1)
    filho2 = ajustar_selecao(filho2)
    return filho1, filho2


# Passo 7: Como estamos trabalho com representações binárias, o uso da Bit Flip Mutation é o mais indicado pois, um gene aleatório
# de 0 para 1 ou de 1 para 0, garantindo que o número de terrenos selecionados
# ainda esteja dentro dos limites definidos.
def mutar(individuo):
    i = random.randint(0, len(individuo) - 1)
    individuo[i] = 1 - individuo[i]
    return ajustar_selecao(individuo)


def ajustar_selecao(individuo):
    selecionados = sum(individuo)

    # Reduz terrenos se ultrapassou o máximo
    while selecionados > MAX_TERRAINS:
        idx = random.choice([i for i, gene in enumerate(individuo) if gene == 1])
        individuo[idx] = 0
        selecionados -= 1

    # Adiciona terrenos se está abaixo do mínimo
    while selecionados < MIN_TERRAINS:
        idx = random.choice([i for i, gene in enumerate(individuo) if gene == 0])
        individuo[idx] = 1
        selecionados += 1

    return individuo


def avaliarMelhor(individuo):
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

    fitness = avaliar(individuo)

    media_custos = custo_total / selecionados if selecionados > 0 else 0
    media_impacto = impacto_total / selecionados
    media_valorizacao = valorizacao_total / selecionados
    media_casas = casas_total / selecionados
    media_distancia = distancia_total / selecionados
    media_mobilidade = mobilidade_total / selecionados
    media_infra = infraestrutura_total / selecionados

    return (
        fitness,
        media_custos,
        media_impacto,
        media_valorizacao,
        media_casas,
        media_distancia,
        media_mobilidade,
        media_infra,
    )


# Implementa o algoritmo genético completo, incluindo inicialização, seleção, cruzamento e mutação.
# O algoritmo itera por um número definido de gerações, melhorando a população a cada iteração.
# A cada geração, a população é ordenada por fitness e os melhores indivíduos são selecionados
# para gerar a próxima geração. O melhor indivíduo é retornado ao final do processo.
def algoritmo_genetico(geracoes, tamanho_pop, k_torneio):
    populacao = [criar_individuo() for _ in range(tamanho_pop)]
    status = st.empty()
    for generation in range(geracoes):
        populacao.sort(key=avaliar, reverse=True)

        nova_populacao = [populacao[0]]
        status.markdown(f"**Geração {generation + 1}/{geracoes}**")
        while len(nova_populacao) < tamanho_pop:
            pai1 = torneio(populacao, k_torneio)
            pai2 = torneio(populacao, k_torneio)

            filho1, filho2 = cruzar(pai1, pai2)

            if random.random() < 0.1:
                mutar(filho1)
            if random.random() < 0.1:
                mutar(filho2)

            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao[:tamanho_pop]

    melhor = max(populacao, key=avaliar)
    return melhor

# A visualização dos resultados é feita usando Streamlit para criar uma interface interativa.
st.title("Algoritmo Genético para Seleção de Terrenos")
num_terrenos = st.slider("Número de Terrenos", 100, 500, 10)
geracoes = st.slider("Número de Gerações", 1, 4999, 80)
tamanho_pop = st.slider("Tamanho da População", 2, 499, 50)
k_torneio = st.slider(
    "Número de competidores no Torneio (k)", min_value=2, max_value=10, value=3
)


# Exibe a tabela
def ajustar_largura_colunas(styler):
    return styler.set_table_styles(
        [
            {"selector": "th.col0", "props": [("min-width", "50px")]},
            {"selector": "td.col0", "props": [("min-width", "50px")]},
            {"selector": "th.col1", "props": [("min-width", "150px")]},
            {"selector": "td.col1", "props": [("min-width", "150px")]},
            {"selector": "th", "props": [("font-size", "14px")]},
            {"selector": "td", "props": [("font-size", "14px")]},
        ]
        + [
            {"selector": f"th.col{i}", "props": [("min-width", "70px")]}
            for i in range(2, len(df_terrenos.columns))
        ]
        + [
            {"selector": f"td.col{i}", "props": [("min-width", "70px")]}
            for i in range(2, len(df_terrenos.columns))
        ]
    )


if st.button("Executar Algoritmo Genético"):
    st.write("Executando... isso pode levar alguns segundos.")
    terrenos = gerar_terrenos(num_terrenos)
    melhor = algoritmo_genetico(geracoes, tamanho_pop, k_torneio)
    (
        fitness,
        media_custos,
        media_impacto,
        media_valorizacao,
        media_casas,
        media_distancia,
        media_mobilidade,
        media_infra,
    ) = avaliarMelhor(melhor)

    st.write("**Resultado Médio dos Terrenos escolhidos**")

    st.write(f"**Valor Medio**: R${media_custos:,.2f}")
    st.write(f"**Impacto Ambiental**: {media_impacto:.2f}")
    st.write(f"**Valorizacao**: {media_valorizacao:.2f}")
    st.write(f"**Casas possíveis**: {media_casas:.2f}")
    st.write(f"**Distância ao Centro**: {media_distancia:.2f} km")
    st.write(f"**Distância Transporte (Mobilidade Urbana)**: {media_mobilidade:.2f} km")
    st.write(f"**Infraestrutura**: {media_infra:.2f}")

    st.write(f"**Aptidão**: {fitness:.2f}")
    st.write(f"**Quantidade terrenos escolhidos:** {sum(melhor):.2f}")

    # Extrair custos dos terrenos selecionados
    custos = [terrenos[i][CUSTO] for i, gene in enumerate(melhor) if gene == 1]
    indices = [i for i, gene in enumerate(melhor) if gene == 1]

    if custos:
        dados_terrenos = []

        for i in indices:
            terreno = terrenos[i]
            dados_terrenos.append(
                {
                    "Índice do Terreno": i,
                    "Custo (R$)": terreno[CUSTO],
                    "Valorização (%)": terreno[VALORIZACAO],
                    "Número de Casas": terreno[CASAS],
                }
            )

        # Criação do DataFrame
        df_terrenos = pd.DataFrame(dados_terrenos)

        # Formata a coluna de custo para moeda (R$)
        df_terrenos["Custo (R$)"] = df_terrenos["Custo (R$)"].apply(
            lambda x: f"R$ {x:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        # Exibindo com largura customizada
        st.subheader("Detalhes dos Terrenos Selecionados")
        st.dataframe(
            df_terrenos.style.pipe(ajustar_largura_colunas), use_container_width=True
        )
    else:
        st.write("Nenhum terreno selecionado para mostrar gráfico.")

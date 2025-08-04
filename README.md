# 🧠 Seleção Inteligente de Terrenos com Algoritmo Genético

Este projeto aplica conceitos de **Inteligência Artificial**, especialmente **Algoritmos Genéticos**, para apoiar **decisores públicos na seleção ideal de terrenos** destinados à habitação social. A ideia é considerar múltiplos critérios (como custo, impacto ambiental, valorização, número de casas, infraestrutura etc.) e, com base neles, encontrar a melhor combinação possível.

A aplicação foi desenvolvida em **Python**, com interface via **Streamlit** e visualizações com **pandas** e **dataframes interativos**.

---

## 🧩 O Problema

O desafio é escolher um subconjunto de terrenos que **maximizem o benefício urbano e habitacional** e, ao mesmo tempo, respeitem:

- Custos máximos;
- Número mínimo e máximo de terrenos;
- Mínimo de valorização e casas possíveis por terreno.

Cada terreno é representado como uma lista de atributos (custo, impacto, valorização, casas, distância ao centro, mobilidade urbana e infraestrutura).

---

## 🚀 Solução: Algoritmo Genético

Utilizamos Otimização combinatória, como no problema do caixeiro viajante,  a solução visa auxiliar os gestores em relação a politicas publicas de moradia, no que diz respeito a escolha de locais para a construção de moradias populares. 

### ⚙️ Componentes principais do algoritmo:

- **Representação**: cada indivíduo é uma lista binária (0 = terreno não selecionado, 1 = selecionado).
- **Função de avaliação (`avaliar`)**: calcula um score para cada indivíduo com base nos critérios definidos.
- **Seleção (`torneio`)**: usa o algoritmo de **torneio com elitismo**, escolhendo os melhores entre grupos aleatórios.
- **Cruzamento (`cruzar`)**: implementa o **cruzamento uniforme (uniform crossover)**, trocando genes entre dois pais para formar dois filhos.
- **Mutação (`mutar`)**: utiliza **Bit Flip Mutation** (inversão binária) para manter diversidade genética na população.
- **Correção (`ajustar_selecao`)**: garante que o número de terrenos selecionados permaneça entre os limites mínimo e máximo.

---

## 📊 Interface e Visualização

Durante a execução da aplicação, você poderá:

- Ajustar parâmetros como:
  - Número de terrenos disponíveis;
  - Tamanho da população;
  - Número de gerações;
  - Número de competidores do torneio.
- Ver em tempo real:
  - Estatísticas médias dos terrenos escolhidos;
  - Aptidão da solução;
  - Tabela com os terrenos selecionados, incluindo custo formatado, valorização e número de casas.

---

## 🧪 Como usar

### 1. Clone o repositório
```bash
git clone git@github.com:hcreis/fiap-fase2.git
cd fiap-fase2
```

### 2. Crie o ambiente virtual (Python 3.9+ recomendado)
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Rode a aplicação
```bash
streamlit run app.py
```

---

## 🧰 Tecnologias utilizadas

- Python 3
- Streamlit (interface interativa)
- pandas (manipulação e exibição de dados)
- Algoritmos Genéticos (implementação manual)

---

## 👥 Equipe

- **Helen de Cassia dos Reis Cruz**  
  - E-mail: helen1705@hotmail.com  
  - Registro: RM364533

- **Leandro Bernardo dos Santos**  
  - E-mail: leandro.bernardos@gmail.com  
  - Registro: RM364534

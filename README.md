# 🧠 Seleção Inteligente de Terrenos com Algoritmo Genético

Olá! Este projeto foi criado com o objetivo de aplicar conceitos de **Inteligência Artificial**, mais especificamente **Algoritmos Genéticos**, para auxiliar na **escolha de terrenos ideais** considerando múltiplos critérios: custo, impacto ambiental, valorização futura, entre outros.

A aplicação foi desenvolvida usando **Python** com **Streamlit** para interface interativa e **matplotlib** para visualização gráfica.

O problema consiste em selecionar um subconjunto de terrenos que otimize critérios como custo, distância ao centro, impacto ambiental, acesso a transporte e infraestrutura, respeitando restrições de orçamento, número de terrenos (mínimo e máximo) e infraestrutura média mínima. Cada terreno é representado como um dicionário com atributos.

---

## 🚀 Como funciona

A lógica principal gira em torno de um Algoritmo Genético, que simula o processo de evolução natural. Ele tenta encontrar, dentre todos os terrenos disponíveis, a **combinação ideal de terrenos** que:

- **Maximizem a valorização** e o número de casas possíveis;
- **Minimizem o custo** e o impacto ambiental;
- Respeitem limites como orçamento máximo e impacto permitido.

A seleção dos indivíduos (soluções) é feita com **torneio com elitismo**, garantindo que as melhores soluções sejam preservadas a cada geração.

---

## 🧩 Principais componentes

- `avaliar(individuo)`: função de fitness que calcula a qualidade de cada solução.
- `selecionaPais(populacao)`: faz a seleção por torneio, priorizando indivíduos mais aptos. ( Algoritmo escolhido: Torneio com Elitismo )
- `cruzar(pai1, pai2)`: faz o cruzamento genético, gerando novos filhos. ( Algoritmo escolhido: Cruzamento uniforme (uniform crossover) )
- `mutar(individuo)`: aplica mutação aleatória para manter diversidade na população. ( Algoritmo escolhido: Bit Flip Mutation uso representação binária  )
- `extrair_terrenos_validos(individuo)`: garante que apenas terrenos realmente escolhidos e válidos sejam considerados nos gráficos e resultados.

---

## 🧪 Como usar

### 1. Clone o repositório
```bash
git git@github.com:hcreis/fiap-fase2.git
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
- Streamlit (interface)
- matplotlib (gráficos)
- Algoritmos Genéticos (implementação manual)

---

## 📊 Exemplo de execução

Durante a execução, você poderá:

- Ajustar os parâmetros do algoritmo via sliders (número de gerações, taxa de mutação, etc.)
- Visualizar em tempo real os terrenos selecionados no gráfico
- Ver quais terrenos foram escolhidos e como eles performam nos critérios definidos

---

## 📫 Contato

- Nome: Helen de Cassia dos Reis Cruz
- E-mail: helen1705@hotmail.com
- Registro: RM364533

- Nome: Leandro Bernardo dos Santos
- E-mail: leandro.bernardos@gmail.com
- Registro: RM364534
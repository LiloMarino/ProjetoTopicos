Ahhh agora **ficou MUITO mais claro** o que você está buscando! 👏 Agora estamos falando de um projeto de **"realidade virtual ecológica"** mesmo, onde:

- **Coelhos e lobos são controlados por NEAT**.
- **Cada um evolui separadamente** (coelhos para fugir melhor, lobos para caçar melhor).
- **O ambiente tem obstáculos e limites** (não é só plano vazio).
- **Tudo é representado graficamente** para visualizar a evolução.

Perfeito. Agora sim conseguimos desenhar um **roteiro técnico certinho**!

---

# 🧠 Algoritmo/Roteiro Geral de Execução

### 1. Inicialização
- Carregar o mapa (`ambiente.png`) e a máscara de colisões (`mask_ambiente.png`).
- Configurar NEAT:
  - **Um NEAT para coelhos**.
  - **Um NEAT para lobos** (opcionalmente separados ou juntos).

### 2. Criar a população
- Criar uma quantidade inicial de **coelhos** (cada um com sua rede neural).
- Criar uma quantidade inicial de **lobos** (cada um com sua rede neural).

### 3. Simulação (Loop Principal de Uma Rodada)
- Para cada frame:
  - **Coelhos**:
    - Sentem o ambiente (inputs = posição dos lobos, obstáculos próximos, bordas...).
    - Através da rede neural, escolhem como se mover (direções).
    - Movem-se se a posição for válida (não atravessam obstáculos).
  - **Lobos**:
    - Sentem o ambiente (inputs = posição dos coelhos, obstáculos próximos).
    - Através da rede neural, escolhem como se mover para caçar.
    - Movem-se se a posição for válida.
  - Atualizar tela (desenhar ambiente, coelhos, lobos).
  - Verificar:
    - Se lobo capturou coelho → lobo ganha pontos, coelho perde pontos.
    - Se coelho escapou tempo suficiente → coelho ganha pontos.

### 4. Avaliar Fitness
- Cada coelho e lobo tem um `fitness` baseado em:
  - Coelhos:
    - + sobrevivência por tempo.
    - - ser pego por lobo.
  - Lobos:
    - + caçar coelhos rápido.
    - - ficar muito tempo sem pegar nada.

### 5. Evoluir População (Fim da Rodada)
- NEAT seleciona os melhores coelhos/lobos para cruzar e mutar.
- Cria a nova geração.
- Recomeça a simulação.

### 6. Repetir
- Executar o processo de simulação/avaliação/evolução para várias gerações.

---

# 🗺️ Estrutura de Arquivos no Projeto

```text
/ecosystem-sim/
├── assets/
│   ├── ambiente.png
│   ├── mask_ambiente.png
│   ├── cueio.png
│   ├── lobo.png
├── main.py            # onde tudo começa
├── ambiente.py        # cuida do ambiente e das colisões
├── coelho.py          # define o comportamento do coelho
├── lobo.py            # define o comportamento do lobo
├── simulador.py       # roda a simulação de uma geração
├── neat-config-coelho.txt  # configuração NEAT para coelhos
├── neat-config-lobo.txt    # configuração NEAT para lobos
└── utils.py           # funções utilitárias (ex: calcular distância)
```

---

# 🔥 Pequenos detalhes técnicos importantes

- **NEAT separado para coelho e lobo**:  
  Se quiser, você pode evoluir coelhos e lobos **independentemente** para ter especialização real.  
  Ou usar um único NEAT para ambos (mais difícil).

- **Inputs para as redes neurais**:
  - Para coelhos:
    - Distância para o lobo mais próximo.
    - Se tem obstáculo nas direções ao redor.
    - Distância até borda do mapa.
  - Para lobos:
    - Distância para o coelho mais próximo.
    - Obstáculos ao redor.
    - Distância até borda.

- **Saídas da rede neural**:
  - [Movimento_X, Movimento_Y] (ex: ir para cima, baixo, esquerda, direita).

- **Fitness**:
  - Coelho: tempo vivo + distância de lobos.
  - Lobo: número de coelhos caçados.

---

# 🎬 Exemplo visual de como seria a execução:

```text
1. Carrega o mapa e a máscara.
2. Cria população de 20 coelhos e 5 lobos (cada um com sua NEAT).
3. Para cada passo:
    - Coelhos fogem, lobos perseguem.
    - Coelhos e lobos desviam de obstáculos.
    - A tela atualiza mostrando a simulação.
4. Depois de 30 segundos ou se todos coelhos forem mortos:
    - Avalia fitness.
    - NEAT gera nova geração.
5. Gerações se repetem.
6. Visualmente, vê-se coelhos e lobos ficando cada vez mais espertos!
```

---

# 🚀 Resumão
| Parte | O que faz? |
|:-----|:------------|
| **Ambiente** | Impede atravessar pedras, define limites |
| **Coelho.py** | Controla como o coelho age |
| **Lobo.py** | Controla como o lobo age |
| **Simulador** | Executa a simulação de uma geração |
| **NEAT** | Faz a evolução automática de cérebros dos agentes |

---

# ✨ Próximo passo: quer que eu já comece a montar o esqueleto real para isso?

- Um `main.py` para iniciar tudo.
- Um `ambiente.py` que lê a máscara de colisão.
- Um `coelho.py` e `lobo.py` para definir o comportamento.
- Um `simulador.py` para rodar a partida.
- As configs de NEAT separadas para cada espécie.

Posso montar e te explicar cada parte também se quiser, de uma forma bem organizada 🚀

**Quer?** 🎯🎮
(Se quiser, me diz também se prefere que eu já adicione inputs de obstáculos no coelho e no lobo!)
# Projeto Caça-Predador

## Modelagem

### Coelho 🐇

#### Fitness

**Como é definido o coelho mais apto?**

- +0.5/tick indicando uma fuga bem sucedida
- +1 por se afastar do lobo
- -1 por se aproximar do lobo
- +100 por comer cenoura
- -100 por morrer (tanto por fome quanto pelo lobo)

#### Inputs

**O que o coelho vê? ou precisa ver?**

- Distância até **a cenoura mais próxima**
- Direção da cenoura mais próxima
- Distância até **o lobo mais próximo**
- Direção do lobo mais próximo
- Distância até **o obstáculo mais próximo**
- Direção do obstáculo mais próximo
- Colisão com os obstáculos (Norte, Sul, Leste, Oeste)

#### Outputs

**O que o coelho faz?**

- Se movimenta usando as direções (Norte, Sul, Leste, Oeste)

### Lobo 🦊

#### Fitness

**Como é definido o lobo mais apto?**

- -1/tick indicando uma caça mal sucedida
- +1 por se aproximar do coelho
- -1 por se afastar do coelho
- +100 por comer coelho
- -100 por morrer (por fome)

#### Inputs

**O que o lobo vê? ou precisa ver?**

- Distância até **o coelho mais próximo**
- Direção do coelho mais próximo
- Distância até **o obstáculo mais próximo**
- Direção do obstáculo mais próximo
- Colisão com os obstáculos (Norte, Sul, Leste, Oeste)

#### Outputs

**O que o lobo faz?**

- Se movimenta usando as direções (Norte, Sul, Leste, Oeste)

### Ambiente 🌳

Onde o agente vive e que define regras e colisões

### Simulador 🌎


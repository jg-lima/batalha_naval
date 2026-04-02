# Batalha Naval

Um jogo de Batalha Naval implementado em Python com Pygame-ce

---

## Visão Geral

O jogo simula a batalha naval tradicional onde dois jogadores, alternadamente, tentam destruir os navios do adversário. Cada jogador tem 7 navios de 3 células em um tabuleiro 10x10. O objetivo é destruir todos os navios do oponente antes que seus próprios navios sejam destruídos.

---

## Estrutura do Projeto

```
batalha_naval/
├── batalha_naval.py          # Arquivo principal - Fluxo e loop do jogo
├── logica_jogo.py            # Lógica de jogo - Funções do tabuleiro e mecânicas
├── interface_jogo.py         # Interface gráfica - Desenho, sons e imagem
├── README.md                 # Este arquivo
├── imagens/                  # Sprites dos navios
├── sons/                     # Efeitos sonoros
```

---

## Módulos

### 1. **logica_jogo.py** - Lógica Core do Jogo

Define todas as operações matemáticas e lógicas relacionadas ao tabuleiro.

#### `novo_tabuleiro()`
Cria um tabuleiro zerado uma matriz 10x10 onde `0` significa água e os números `1` a `7` identificam cada navio.

- **Retorna:** Matriz 10x10 preenchida com zeros
- **Função:** Cria um tabuleiro vazio
- **Representação:** 
  - `0` = água (sem navio)
  - `1-7` = ID do navio

```python
tabuleiro = [[0, 0, 0, ..., 0],
             [0, 0, 0, ..., 0],
             ...
             [0, 0, 0, ..., 0]]
```

#### `celula_do_mouse(mouse_x, mouse_y)`
Transforma a posição do cursor (em pixels) numa célula do tabuleiro (coluna, linha). O tabuleiro começa no pixel (40, 40) e cada célula tem 52×52 px, retorna a coordenada`(coluna, linha)` ou `None` se o mouse estiver fora do tabuleiro.


- **Parâmetros:** Coordenadas x, y do mouse (pixels)
- **Retorna:** Tupla (coluna, linha) ou None
- **Função:** Converte coordenadas de pixel em índices do tabuleiro
- **Cálculo:**
  - Tabuleiro começa em pixel (40, 40)
  - Cada célula tem 52x52 pixels
  - Fórmula: `(coordenada - 40) // 52`
  - Valida se está dentro dos limites [0-9]

#### `pode_colocar(tabuleiro, coluna, linha)`
Antes de confirmar a posição de um navio, esta função verifica duas coisas: se o navio de 3 células cabe horizontalmente a partir daquela coluna, e se todas as células estão livres. Retorna `True` ou `False`.

- **Parâmetros:** Tabuleiro, coluna, linha de início
- **Retorna:** Boolean `True` se posição é válida, `False` caso contrário
- **Verificações:**
  1. Navio ocupa 3 células horizontalmente → `coluna + 3 ≤ 10`
  2. Todas as 3 células devem estar vazias (valor 0)

#### `coloca_navio(tabuleiro, coluna, linha, id_navio)`
Coloca o navio no tabuleiro preenchendo 3 células consecutivas com o ID do navio (de `1` a `7`, na ordem em que foram posicionados).

- **Parâmtros:** Tabuleiro, posição, ID do navio (1-7)
- **Retorna:** Preenche 3 células consecutivas com o ID do navio
- **Direção:** Horizontal (mesmo linha, colunas consecutivas)

```python
# Exemplo: Colocar navio ID 1 na coluna 2, linha 3
# Antes:  [0, 0, 0, 0, 0, ...]
# Depois: [0, 0, 1, 1, 1, ...]
```

#### `aplicar_tiro(tabuleiro, tiros_jogador, coluna, linha)`
Executa um tiro. Se a célula for água (`0`), registra o tiro e retorna `False`. Se for navio, **destrói o navio inteiro imediatamente** (registra as 3 células como atingidas) e retorna `True`.

- **Parâmetros:** Tabuleiro adversário, lista de tiros, coordenadas do tiro
- **Retorna:** Boolean (True = destruiu navio, False = errou)
- **Lógica:**
  1. Se célula = 0 (água): registra tiro, retorna False
  2. Se célula ≠ 0 (navio):
     - Identifica o ID do navio atingido
     - Localiza TODAS as 3 células daquele navio no tabuleiro
     - Adiciona as 3 coordenadas à lista `tiros_jogador`
     - Retorna True imediatamente (navio destruído instantaneamente)

#### `todos_destruidos(tabuleiro, tiros_jogador)`
Percorre o tabuleiro inteiro procurando alguma célula de navio que ainda não foi atingida. Se não encontrar nenhuma, retorna `True` um fim de jogo.

- **Parâmetros:** Tabuleiro, lista de tiros
- **Retorna:** Boolean `True` se TODOS os navios foram destruídos (todos atingidos)
- **Lógica:** Percorre todo o tabuleiro procurando por um navio não atingido

#### `contar_destruidos(tabuleiro, tiros_jogador)`
Conta quantos navios foram atingidos. Usa um `set` para evitar contagem duplicada. Retorna um número de `0` a `7`.

- **Parâmetros:** Tabuleiro, lista de tiros
- **Retorna:** Inteiro (número de navios atingidos/destruídos 0-7)
- **Lógica:**
  - Usa um conjunto (`set`) para armazenar IDs únicos de navios atingidos
  - Percorre todo o tabuleiro procurando células de navio que estão na lista de tiros
  - Cada ID de navio é adicionado ao conjunto apenas uma vez, independente de quantas células foram atingidas
  - Retorna o tamanho do conjunto (número de navios únicos atingidos)

---

### 2. **interface_jogo.py** - Interface Gráfica

Gerencia toda a renderização visual(formas e imagens) e áudio.

#### `criar_janela()`
- **Função:** Inicializa Pygame e cria a janela do jogo
- **Dimensões:** 600x680 pixels
  - 600x600: Tabuleiro (10x10 células de 52px)
  - 600x80: Área de informações na parte inferior
- **Retorna:** Tupla com (tela, relógio, fontes, sons)

#### `carregar_sons()`
- **Função:** Carrega arquivos de áudio
- **Sons:**
  - `acertou.mp3`: Som quando o tiro acerta um navio
  - `agua.mp3`: Som quando o tiro erra (acerta água)
- **Retorna:** Dicionário com sons carregados

#### `tocar_som(sons_jogo, chave_som)`
- **Função:** Reproduz som específico
- **Parâmetros:** Sons carregados(dicionário contendo o caminho dos sons), Chave do som ("acerto" ou "erro")

#### `obter_parte_navio(tabuleiro, coluna, linha)`
- **Função:** Determina qual das 3 partes do navio está naquela célula para desenhar a imagem correta
- **Parâmetros:** Tabuleiro, coluna e linha da célula
- **Retorno:** Número da parte (1, 2 ou 3) ou 0 se não houver navio
- **Lógica:**
  1. Identifica o ID do navio naquela célula
  2. Encontra a primeira coluna do navio movendo-se para esquerda até detectar mudança de ID
  3. Calcula a posição relativa: `coluna_atual - primeira_coluna + 1`
- **Exemplo:** 
  - Navio nas colunas [3, 4, 5] com ID 1
  - Primeira coluna 3
  - Na coluna 3 (3 - 3 + 1) = retorna 1 (primeira parte)
  - Na coluna 4 (4 - 3 + 1) = retorna 2 (segunda parte)
  - Na coluna 5 (5 - 3 + 1) = retorna 3 (terceira parte)

#### `desenhar_grade(tela_jogo, fonte, tabuleiro, tiros_jogador, esconder, celula_ativa)`
- **Função:** Desenha o tabuleiro 10x10 na tela
- **Parâmetros:**
  - `esconder`: Se True, não mostra os navios (modo de ataque)
  - `celula_ativa`: Célula onde o mouse está (mostra preview)
- **Cores:**
  - Azul: Água não atingida
  - Verde: Navio não atingido
  - Vermelho: Acerto (navio atingido)
  - Cinza: Erro (água atingida)
- **Imagens:** Sprites dos navios em diferentes estados

#### `desenhar_info(tela_jogo, fonte, texto_info)`
- **Função:** Exibe mensagem na área inferior da tela

#### `botao(tela_jogo, fonte, texto, pos_x, pos_y, largura, altura)`
- **Função:** Desenha botão interativo

#### `mensagem(tela_jogo, fonte_media, fonte_grande, titulo, subtitulo, texto_botao)`
- **Função:** Exibe tela de mensagem com transições

#### `tela_vitoria(tela_jogo, fonte_media, fonte_grande, jogador_vencedor)`
- **Função:** Exibe tela final com jogador vencedor

---

### 3. **batalha_naval.py** - Fluxo Principal

Implementa o loop principal e máquina de estados do jogo.

#### Variáveis Principais

```python
estado_jogo              # Estado atual da máquina de estados
tabuleiro_player1        # Matriz 10x10 do jogador 1
tabuleiro_player2        # Matriz 10x10 do jogador 2
tiros_player1            # Lista de tiros do jogador 1: [(col, lin), ...]
tiros_player2            # Lista de tiros do jogador 2: [(col, lin), ...]
navios_colocados_player1 # Contador: 0-7
navios_colocados_player2 # Contador: 0-7
jogador_vencedor         # Jogador que venceu (1 ou 2)
```
---

### Estados Detalhados

#### **SETUP1** - Jogador 1 coloca navios
- Jogador 1 clica nas células para posicionar seus 7 navios
- Cada navio recebe um ID: 1, 2, 3, 4, 5, 6, 7
- Validação: máximo 7 navios, sem sobreposição
- Transição: Quando contador = 7 → TRANS_P2

#### **TRANS_P2** - Transição para Jogador 2
- Mensagem: "Jogador 1 está pronto. Passe o computador para Jogador 2"
- Aguarda clique para continuar

#### **SETUP2** - Jogador 2 coloca navios
- Mesmo processo que SETUP1 para o jogador 2
- Transição: Quando contador = 7 → TRANS_BATALHA

#### **TRANS_BATALHA** - Início da batalha
- Mensagem: "Batalha vai começar! Jogador 1 ataca primeiro"
- Aguarda clique para iniciar ataques

#### **BATALHA1** - Jogador 1 ataca
- Jogador 1 clica no tabuleiro adversário (Player 2)
  - Tabuleiro de Player 2 é mostrado com `esconder=True` (sem revelar navios não atingidos)
- Aplicação do tiro via `aplicar_tiro(tabuleiro_player2, tiros_player1, col, lin)`
  - Se retorna **True** (acertou):
    - Toca som de "acerto"
    - Verifica com `todos_destruidos()` se Player 2 perdeu
    - Se perdeu → VITORIA (jogador_vencedor = 1)
    - Se não perdeu → volta para BATALHA1 (Jogador 1 ataca novamente)
  - Se retorna **False** (errou):
    - Toca som de "erro"
    - Transição → TRANS_2

#### **TRANS_2** - Transição para Jogador 2
- Mensagem: "Água! Vez do Jogador 2"
- Aguarda clique para continuar

#### **BATALHA2** - Jogador 2 ataca
- Similar a BATALHA1, mas Player 2 ataca Player 1
- Lógica idêntica mas com tabuleiros invertidos

#### **TRANS_1** - Transição para Jogador 1
- Mensagem: "Água! Vez do Jogador 1"

#### **VITORIA** - Tela de vitória
- Exibe qual jogador venceu
- Botão "Jogar Novamente" reinicia o jogo → SETUP1

---

## Estrutura de Dados

### Tabuleiro
```python
tabuleiro = [
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],  # Linha 0
    [0, 0, 0, 0, 0, 0, 2, 2, 2, 0],  # Linha 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Linha 2
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0],  # Linha 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Linha 4
    ...
]
# 0 = água, 1-7 = ID dos navios
```

### Lista de Tiros
```python
tiros = [
    (2, 0),  # Coluna 2, Linha 0 (acertou navio 1)
    (5, 1),  # Coluna 5, Linha 1 (acertou água)
    (3, 2),  # Coluna 3, Linha 2 (acertou água)
    ...
]
```

### Como verificar se um navio foi destruído
```python
# Navio 1 tem células em (2,0), (3,0), (4,0)
# Se tiros = [(2,0), (3,0), (4,0)], o navio 1 foi destruído

# Função aplicar_tiro retorna True quando TODAS as 
# células do navio atingido foram acertadas
```

---

## Fluxo de Interação do Usuário

### Fase de Setup
1. **Clique do mouse** → Detecta posição via `celula_do_mouse()`
2. **Validação** → `pode_colocar()` verifica se é válido
3. **Colocação** → `coloca_navio()` registra navio no tabuleiro
4. **Incremento** → `navios_colocados` aumenta
5. **Transição** → Quando = 7, muda estado

### Fase de Batalha
1. **Clique do mouse** → Detecta célula alvo
2. **Verificação** → Confirma se já atirou nessa célula
3. **Aplicação** → `aplicar_tiro()` executa a lógica
4. **Dano** → Se tiro atinge navio, registra acerto
5. **Verificação de Vitória** → `todos_destruidos()` ou `contar_destruidos()`
6. **Próximo Turno** → Muda para outro jogador

---

## Mecânicas Importantes

### Detecção de Célula do Mouse
- Coordenada pixel → Índice tabuleiro
- Margem esquerda: 40px, Margem superior: 40px
- Tamanho célula: 52x52px
- Fórmula: `indice = (coordenada - 40) // 52`

### Navios no Tabuleiro
- Tamanho fixo: 3 células
- Orientação: Horizontal
- ID único: 1-7 (baseado na ordem de colocação)
- Não podem se sobrepor

### Verificação de Destruição de Navio
- Um navio é destruído quando TODAS as suas 3 células são atingidas
- `aplicar_tiro()` percorre todo o tabuleiro procurando células não atingidas
- Retorna True apenas se não encontrar nenhuma célula não atingida

### Fim do Jogo
- O jogo termina quando `todos_destruidos()` retorna True
- TODOS os 7 navios do perdedor devem ser destruídos

---

## Recursos Visuais

### Dimensões e Cores
- **Tabuleiro:** 10x10 células de 52x52 pixels = 520x520
- **Área total:** 600x680 pixels
- **Área info:** 600x80 pixels na base
- **Área jogo** 600x600 pixels
- **Cores:**
  - Azul: Água não atingida
  - Verde: Navio não destruído
  - Vermelho: Acerto (navio destruído)
  - Cinza: Erro (água atingida)

### Imagens
- `barco_1.png`, `barco_2.png`, `barco_3.png`: Navios inteiros
- `barco_destruido_1.png`, `barco_destruido_2.png`, `barco_destruido_3.png`: Navios destruídos

### Sons
- `acertou.mp3`: Feedback positivo
- `agua.mp3`: Feedback negativo

---

## Resumo da Lógica

| Componente | Função | Entrada | Saída |
|-----------|--------|---------|-------|
| `novo_tabuleiro()` | Cria tabuleiro vazio | - | Matriz 10x10 |
| `celula_do_mouse()` | Converte pixel → índice | (x, y) | (col, lin) ou None |
| `pode_colocar()` | Valida posição navio | (tab, col, lin) | Boolean |
| `coloca_navio()` | Registra navio | (tab, col, lin, id) | Modifica tabuleiro |
| `aplicar_tiro()` | Processa tiro | (tab, tiros, col, lin) | Boolean |
| `todos_destruidos()` | Verifica derrota | (tab, tiros) | Boolean |
| `contar_destruidos()` | Conta navios perdidos | (tab, tiros) | Inteiro 0-7 |

---

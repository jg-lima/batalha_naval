import pygame


def criar_janela():
    pygame.init()
    tela_jogo = pygame.display.set_mode((600, 680)) # 600x600 area de jogo + 80 pixels para a área de informações na parte inferior da tela
    pygame.display.set_caption("Batalha Naval")
    relogio_jogo = pygame.time.Clock()
    fonte_pequena = pygame.font.SysFont(None, 20)
    fonte_media = pygame.font.SysFont(None, 28)
    fonte_grande = pygame.font.SysFont(None, 52)
    sons_jogo = carregar_sons()
    return tela_jogo, relogio_jogo, fonte_pequena, fonte_media, fonte_grande, sons_jogo


def carregar_sons():
    sons_jogo = {"acerto": None, "erro": None} # cria um dicionário para armazenar os sons do jogo, onde as chaves são "acerto" e "erro". Inicialmente, os valores são definidos como None, indicando que os sons ainda não foram carregados. O dicionário é usado para organizar e acessar facilmente os sons do jogo com base em suas chaves correspondentes.

    pygame.mixer.init()
    sons_jogo["acerto"] = pygame.mixer.Sound("./sons/acertou.mp3")
    sons_jogo["erro"] = pygame.mixer.Sound("./sons/agua.mp3")
    # inicializa o mixer de áudio do Pygame e carrega os arquivos de som "acertou.mp3" e "agua.mp3" para as chaves "acerto" e "erro" do dicionário sons_jogo, respectivamente.
    return sons_jogo


def tocar_som(sons_jogo, chave_som):
    sons_jogo[chave_som].play() # acessa o som correspondente à chave fornecida (chave_som) no dicionário sons_jogo e reproduz o som usando o método play().


def obter_parte_navio(tabuleiro, coluna, linha):
    id_navio = tabuleiro[linha][coluna]
    if id_navio == 0:
        return 0
    
    # Encontra a primeira coluna do navio
    primeira_coluna = coluna
    while primeira_coluna > 0 and tabuleiro[linha][primeira_coluna - 1] == id_navio:
        primeira_coluna -= 1
    
    # Retorna qual parte é (1, 2 ou 3)
    return coluna - primeira_coluna + 1


def desenhar_grade(tela_jogo, fonte_pequena, tabuleiro, tiros_jogador, esconder=False, celula_ativa=None):
    cor_agua = "blue"
    cor_navio = "green"
    cor_acerto = "red"
    cor_erro = "gray"
    cor_borda = "black"
    cor_texto = "white"
    imagem_barco = {1: pygame.image.load("./imagens/barco_1.png").convert_alpha(), 2: pygame.image.load("./imagens/barco_2.png").convert_alpha(), 3: pygame.image.load("./imagens/barco_3.png").convert_alpha()}
    imagem_barco_destruido = {1: pygame.image.load("./imagens/barco_destruido_1.png").convert_alpha(), 2: pygame.image.load("./imagens/barco_destruido_2.png").convert_alpha(), 3: pygame.image.load("./imagens/barco_destruido_3.png").convert_alpha()}

    for linha in range(10):
        for coluna in range(10):
            pos_x = 40 + coluna * 52
            pos_y = 40 + linha * 52 # calcula as coordenadas x e y para desenhar a célula da grade com base na posição da coluna e linha, multiplicando o índice da coluna por 52 (tamanho da célula) e adicionando 40 (margem inicial), e fazendo o mesmo para a linha.
            quadrado = pygame.Rect(pos_x, pos_y, 52, 52) # cria um retangulo, com as coordenadas x e y calculadas, e com largura e altura de 52 pixels, representando a célula da grade a ser desenhada.
            celula_tem_navio = tabuleiro[linha][coluna] != 0 # recebe true se a célula atual do tabuleiro contiver um navio (valor diferente de 0) e False caso contrário. Isso é usado para determinar se a célula deve ser desenhada como água ou como um navio, dependendo do valor presente no tabuleiro para aquela posição específica.
            celula_foi_atirada = (coluna, linha) in tiros_jogador # recebe true se a célula atual (representada pelas coordenadas coluna e linha) tiver sido alvo de um tiro do jogador, ou seja, se as coordenadas estiverem presentes na lista tiros_jogador. Caso contrário, recebe False. Isso é usado para determinar se a célula deve ser desenhada como um acerto ou um erro, dependendo se o jogador atirou naquela posição específica.

            if celula_foi_atirada and celula_tem_navio:
                pygame.draw.rect(tela_jogo, cor_acerto, quadrado)
                parte_navio = obter_parte_navio(tabuleiro, coluna, linha)
                tela_jogo.blit(imagem_barco_destruido[parte_navio], quadrado)
            elif celula_foi_atirada:
                pygame.draw.rect(tela_jogo, cor_erro, quadrado)
            elif celula_tem_navio and not esconder:
                pygame.draw.rect(tela_jogo, cor_navio, quadrado)
                parte_navio = obter_parte_navio(tabuleiro, coluna, linha)
                tela_jogo.blit(imagem_barco[parte_navio], quadrado)
            else:
                pygame.draw.rect(tela_jogo, cor_agua, quadrado)

            pygame.draw.rect(tela_jogo, cor_borda, quadrado, 1)

    if celula_ativa and not esconder:
        coluna_ativa, linha_ativa = celula_ativa
        # Desenha as 3 partes do navio
        for parte in range(1, 4):
            coluna = coluna_ativa + parte - 1
            if coluna < 10:
                pos_x = 40 + coluna * 52
                pos_y = 40 + linha_ativa * 52
                tela_jogo.blit(imagem_barco[parte], (pos_x, pos_y))
                pygame.draw.rect(tela_jogo, cor_texto, (pos_x, pos_y, 52, 52), 2)

    letras = "ABCDEFGHIJ"
    for indice in range(10):
        texto_letra = fonte_pequena.render(letras[indice], True, "black")
        tela_jogo.blit(texto_letra, (40 + indice * 52 + (52 - texto_letra.get_width()) // 2, 20)) 
        texto_numero = fonte_pequena.render(str(indice + 1), True, "black")
        tela_jogo.blit(texto_numero, (20, 40 + indice * 52 + (52 - texto_numero.get_height()) // 2)) 


def desenhar_info(tela_jogo, fonte_media, texto_info):
    cor_fundo = "black"
    cor_texto = "white"
    pygame.draw.rect(tela_jogo, cor_fundo, (0, 600, 600, 80)) # 0 e 600 são as coordenadas x e y do canto superior esquerdo do retângulo, 600 é a largura do retângulo e 80 é a altura do retângulo. Isso cria uma área de fundo para a mensagem de informação na parte inferior da tela.
    texto_renderizado = fonte_media.render(texto_info, True, cor_texto)
    tela_jogo.blit(texto_renderizado, (40, 600 + (80 - texto_renderizado.get_height()) // 2))


def botao(tela_jogo, fonte_media, texto_botao, pos_x, pos_y, largura=260, altura=52):
    retangulo_botao = pygame.Rect(pos_x, pos_y, largura, altura)
    pygame.draw.rect(tela_jogo, "black", retangulo_botao)
    pygame.draw.rect(tela_jogo, "white", retangulo_botao, 2)
    texto_renderizado = fonte_media.render(texto_botao, True, "white")
    tela_jogo.blit(texto_renderizado, (pos_x + (largura - texto_renderizado.get_width()) // 2, pos_y + (altura - texto_renderizado.get_height()) // 2))


def mensagem(tela_jogo, fonte_media, fonte_grande, titulo, subtitulo, texto_botao):
    tela_jogo.fill("black")
    texto_titulo = fonte_grande.render(titulo, True, "white")
    texto_subtitulo = fonte_media.render(subtitulo, True, "white")
    tela_jogo.blit(texto_titulo, (300 - texto_titulo.get_width() // 2, 260))
    tela_jogo.blit(texto_subtitulo, (300 - texto_subtitulo.get_width() // 2, 320))
    botao(tela_jogo, fonte_media, texto_botao, 170, 380)


def tela_vitoria(tela_jogo, fonte_media, fonte_grande, jogador_vencedor):
    tela_jogo.fill("black")
    texto_titulo = fonte_grande.render(f"Jogador {jogador_vencedor} venceu!", True, "white")
    texto_subtitulo = fonte_media.render("Todos os navios do adversario foram destruidos!", True, "white")
    tela_jogo.blit(texto_titulo, (300 - texto_titulo.get_width() // 2, 250))
    tela_jogo.blit(texto_subtitulo, (300 - texto_subtitulo.get_width() // 2, 320))
    botao(tela_jogo, fonte_media, "Jogar Novamente", 170, 390)

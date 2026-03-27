import pygame


def criar_janela():
    pygame.init()
    tela_jogo = pygame.display.set_mode((600, 680))
    pygame.display.set_caption("Batalha Naval")
    relogio_jogo = pygame.time.Clock()
    fonte_pequena = pygame.font.SysFont(None, 20)
    fonte_media = pygame.font.SysFont(None, 28)
    fonte_grande = pygame.font.SysFont(None, 52)
    sons_jogo = carregar_sons()
    return tela_jogo, relogio_jogo, fonte_pequena, fonte_media, fonte_grande, sons_jogo


def carregar_sons():
    sons_jogo = {"acerto": None, "agua": None}

    pygame.mixer.init()
    sons_jogo["acerto"] = pygame.mixer.Sound("./sons/acertou.mp3")
    sons_jogo["agua"] = pygame.mixer.Sound("./sons/agua.mp3")

    return sons_jogo


def tocar_som(sons_jogo, chave_som):
    sons_jogo[chave_som].play()


def desenhar_grade(tela_jogo, fonte_pequena, tabuleiro, tiros_jogador, esconder=False, celula_hover=None):
    cor_agua = ('blue')
    cor_navio = ('green')
    cor_acerto = ('red')
    cor_erro = ('gray')
    cor_borda = ('black')
    cor_texto = ('white')

    for linha in range(10):
        for coluna in range(10):
            pos_x = 40 + coluna * 52
            pos_y = 40 + linha * 52
            retangulo = pygame.Rect(pos_x, pos_y, 52, 52)
            celula_tem_navio = tabuleiro[linha][coluna] != 0
            celula_foi_atirada = (coluna, linha) in tiros_jogador

            if celula_foi_atirada and celula_tem_navio:
                pygame.draw.rect(tela_jogo, cor_acerto, retangulo)
            elif celula_foi_atirada:
                pygame.draw.rect(tela_jogo, cor_erro, retangulo)
            elif celula_tem_navio and not esconder:
                pygame.draw.rect(tela_jogo, cor_navio, retangulo)
            else:
                pygame.draw.rect(tela_jogo, cor_agua, retangulo)

            pygame.draw.rect(tela_jogo, cor_borda, retangulo, 1)

    if celula_hover and not esconder:
        coluna_hover, linha_hover = celula_hover
        for coluna in range(coluna_hover, min(coluna_hover + 3, 10)):
            pygame.draw.rect(tela_jogo, (cor_texto), (40 + coluna * 52, 40 + linha_hover * 52, 52, 52), 2)

    letras = "ABCDEFGHIJ"
    for indice in range(10):
        texto_letra = fonte_pequena.render(letras[indice], True, cor_texto)
        tela_jogo.blit(texto_letra, (40 + indice * 52 + (52 - texto_letra.get_width()) // 2, 18))
        texto_numero = fonte_pequena.render(str(indice + 1), True, cor_texto)
        tela_jogo.blit(texto_numero, (15, 40 + indice * 52 + (52 - texto_numero.get_height()) // 2))


def desenhar_info(tela_jogo, fonte_media, texto_info):
    pygame.draw.rect(tela_jogo, ('black'), (0, 600, 600, 80))
    texto_renderizado = fonte_media.render(texto_info, True, ('white'))
    tela_jogo.blit(texto_renderizado, (40, 600 + (80 - texto_renderizado.get_height()) // 2))


def botao(tela_jogo, fonte_media, texto_botao, pos_x, pos_y, largura=260, altura=52):
    retangulo_botao = pygame.Rect(pos_x, pos_y, largura, altura)
    pygame.draw.rect(tela_jogo, ('black'), retangulo_botao)
    pygame.draw.rect(tela_jogo, ('white'), retangulo_botao, 2)
    texto_renderizado = fonte_media.render(texto_botao, True, ('white'))
    tela_jogo.blit(texto_renderizado, (pos_x + (largura - texto_renderizado.get_width()) // 2, pos_y + (altura - texto_renderizado.get_height()) // 2))


def mensagem(tela_jogo, fonte_media, fonte_grande, titulo, subtitulo, texto_botao):
    tela_jogo.fill(('black'))
    texto_titulo = fonte_grande.render(titulo, True, ('white'))
    texto_subtitulo = fonte_media.render(subtitulo, True, ('white'))
    tela_jogo.blit(texto_titulo, (300 - texto_titulo.get_width() // 2, 260))
    tela_jogo.blit(texto_subtitulo, (300 - texto_subtitulo.get_width() // 2, 320))
    botao(tela_jogo, fonte_media, texto_botao, 170, 380)


def tela_vitoria(tela_jogo, fonte_media, fonte_grande, jogador_vencedor):
    tela_jogo.fill(('black'))
    texto_titulo = fonte_grande.render(f"Jogador {jogador_vencedor} venceu!", True, ('white'))
    texto_subtitulo = fonte_media.render("Todos os navios do adversario foram destruidos!", True, ('white'))
    tela_jogo.blit(texto_titulo, (300 - texto_titulo.get_width() // 2, 250))
    tela_jogo.blit(texto_subtitulo, (300 - texto_subtitulo.get_width() // 2, 320))
    botao(tela_jogo, fonte_media, "Jogar Novamente", 170, 390)

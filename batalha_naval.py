import pygame
import sys
from logica_jogo import *
from interface_jogo import *

def main():
    tela_jogo, relogio_jogo, fonte_pequena, fonte_media, fonte_grande, sons_jogo = criar_janela()

    estado_jogo = "setup1"
    tabuleiros = [novo_tabuleiro(), novo_tabuleiro()]
    tiros_jogadores = [[], []]
    navios_colocados = [0, 0]
    jogador_vencedor = 0

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if estado_jogo == "setup1":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and navios_colocados[0] < 7:
                        coluna, linha = celula
                        if pode_colocar(tabuleiros[0], coluna, linha):
                            navios_colocados[0] += 1
                            coloca_navio(tabuleiros[0], coluna, linha, navios_colocados[0])
                            if navios_colocados[0] == 7:
                                estado_jogo = "trans_p2"

                elif estado_jogo == "trans_p2":
                    estado_jogo = "setup2"

                elif estado_jogo == "setup2":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and navios_colocados[1] < 7:
                        coluna, linha = celula
                        if pode_colocar(tabuleiros[1], coluna, linha):
                            navios_colocados[1] += 1
                            coloca_navio(tabuleiros[1], coluna, linha, navios_colocados[1])
                            if navios_colocados[1] == 7:
                                estado_jogo = "trans_batalha"

                elif estado_jogo == "trans_batalha":
                    estado_jogo = "batalha1"

                elif estado_jogo == "batalha1":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and celula not in tiros_jogadores[0]:
                        coluna, linha = celula
                        acertou = aplicar_tiro(tabuleiros[1], tiros_jogadores[0], coluna, linha)
                        if acertou:
                            tocar_som(sons_jogo, "acerto")
                            if todos_destruidos(tabuleiros[1], tiros_jogadores[0]):
                                jogador_vencedor = 1
                                estado_jogo = "vitoria"
                        else:
                            tocar_som(sons_jogo, "agua")
                            estado_jogo = "trans_2"

                elif estado_jogo == "trans_2":
                    estado_jogo = "batalha2"

                elif estado_jogo == "batalha2":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and celula not in tiros_jogadores[1]:
                        coluna, linha = celula
                        acertou = aplicar_tiro(tabuleiros[0], tiros_jogadores[1], coluna, linha)
                        if acertou:
                            tocar_som(sons_jogo, "acerto")
                            if todos_destruidos(tabuleiros[0], tiros_jogadores[1]):
                                jogador_vencedor = 2
                                estado_jogo = "vitoria"
                        else:
                            tocar_som(sons_jogo, "agua")
                            estado_jogo = "trans_1"

                elif estado_jogo == "trans_1":
                    estado_jogo = "batalha1"

                elif estado_jogo == "vitoria":
                    estado_jogo = "setup1"
                    tabuleiros = [novo_tabuleiro(), novo_tabuleiro()]
                    tiros_jogadores = [[], []]
                    navios_colocados = [0, 0]
                    jogador_vencedor = 0

        tela_jogo.fill(('darkgray'))

        if estado_jogo == "setup1":
            celula = celula_do_mouse(mouse_x, mouse_y)
            posicao_valida = pode_colocar(tabuleiros[0], *celula) if celula else False
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiros[0], [], False, celula)
            mensagem_info = f"Jogador 1: navio {navios_colocados[0] + 1}/7"
            if celula:
                mensagem_info += " (valido)" if posicao_valida else " (invalido)"
            desenhar_info(tela_jogo, fonte_media, mensagem_info)

        elif estado_jogo == "trans_p2":
            mensagem(tela_jogo, fonte_media, fonte_grande, "Jogador 1 esta pronto!", "Passe o computador ao Jogador 2", "Continuar")

        elif estado_jogo == "setup2":
            celula = celula_do_mouse(mouse_x, mouse_y)
            posicao_valida = pode_colocar(tabuleiros[1], *celula) if celula else False
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiros[1], [], False, celula)
            mensagem_info = f"Jogador 2: navio {navios_colocados[1] + 1}/7"
            if celula:
                mensagem_info += " (valido)" if posicao_valida else " (invalido)"
            desenhar_info(tela_jogo, fonte_media, mensagem_info)

        elif estado_jogo == "trans_batalha":
            mensagem(tela_jogo, fonte_media, fonte_grande, "Batalha vai comecar!", "Jogador 1 ataca primeiro", "Iniciar")

        elif estado_jogo == "batalha1":
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiros[1], tiros_jogadores[0], True)
            navios_destruidos = contar_destruidos(tabuleiros[1], tiros_jogadores[0])
            desenhar_info(tela_jogo, fonte_media, f"Jogador 1 ataca! Navios destruidos: {navios_destruidos}/7")

        elif estado_jogo == "trans_2":
            mensagem(tela_jogo, fonte_media, fonte_grande, "Agua!", "Vez do Jogador 2", "Continuar")

        elif estado_jogo == "batalha2":
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiros[0], tiros_jogadores[1], True)
            navios_destruidos = contar_destruidos(tabuleiros[0], tiros_jogadores[1])
            desenhar_info(tela_jogo, fonte_media, f"Jogador 2 ataca! Navios destruidos: {navios_destruidos}/7")

        elif estado_jogo == "trans_1":
            mensagem(tela_jogo, fonte_media, fonte_grande, "Agua!", "Vez do Jogador 1", "Continuar")

        elif estado_jogo == "vitoria":
            tela_vitoria(tela_jogo, fonte_media, fonte_grande, jogador_vencedor)

        pygame.display.flip()
        relogio_jogo.tick(60)


if __name__ == "__main__":
    main()

import pygame
import sys
from logica_jogo import *
from interface_jogo import *

def main():
    tela_jogo, relogio_jogo, fonte_pequena, fonte_media, fonte_grande, sons_jogo = criar_janela() # Configura a janela do jogo e os recursos necessários

    estado_jogo = "setup1"
    tabuleiros = [novo_tabuleiro(), novo_tabuleiro()]
    tiros_jogadores = [[], []]
    navios_colocados = [0, 0]
    jogador_vencedor = 0
    # inicializacao das variaveis para estado inicial do jogo

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos() # Captura a posição do mouse 

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # Encerra o jogo quando a janela é fechada

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: # Verifica se o botão esquerdo do mouse foi clicado 
                if estado_jogo == "setup1":
                    celula = celula_do_mouse(mouse_x, mouse_y) # Converte a posição do mouse para coordenadas da grade do jogo
                    if celula and navios_colocados[0] < 7: # Verifica se a célula é válida e se o jogador ainda pode colocar navios
                        coluna, linha = celula # separa as coordenadas para coluna e linha
                        if pode_colocar(tabuleiros[0], coluna, linha): # Verifica se é possível colocar um navio usando o tabuleiro do jogador 1, a coluna e linha selecionadas
                            navios_colocados[0] += 1 # aumenta o numero de navios colocados para o jogador 1
                            coloca_navio(tabuleiros[0], coluna, linha, navios_colocados[0]) # registra o navio no tabuleiro do jogador 1, passando o tabuleiro, coluna, linha e o navio colocado no momento
                            if navios_colocados[0] == 7:
                                estado_jogo = "trans_p2" # Se o jogador 1 tiver colocado os 7 navios, muda o estado do jogo para a transição para o jogador 2

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
                                estado_jogo = "trans_batalha" # mesma coisa para o jogador 2, quando ele colocar os 7 navios, muda o estado do jogo para a transição para a batalha

                elif estado_jogo == "trans_batalha":
                    estado_jogo = "batalha1"

                elif estado_jogo == "batalha1":
                    celula = celula_do_mouse(mouse_x, mouse_y)
                    if celula and celula not in tiros_jogadores[0]: # Verifica se a célula é válida e se o jogador 1 ainda não atirou nessa célula
                        coluna, linha = celula
                        acertou = aplicar_tiro(tabuleiros[1], tiros_jogadores[0], coluna, linha) # Aplica o tiro do jogador 1 no tabuleiro do jogador 2, registrando o tiro na lista de tiros do jogador 1 e verificando se acertou um navio
                        if acertou: 
                            tocar_som(sons_jogo, "acerto")
                            if todos_destruidos(tabuleiros[1], tiros_jogadores[0]):
                                jogador_vencedor = 1
                                estado_jogo = "vitoria" # Se o jogador 1 acertar um navio, toca o som de acerto e verifica se todos os navios do jogador 2 foram destruídos. Se sim, define o jogador 1 como vencedor e muda o estado do jogo para a tela de vitória
                        else:
                            tocar_som(sons_jogo, "agua")
                            estado_jogo = "trans_2" # Se o jogador 1 errar, muda o estado do jogo para a transição para o jogador 2 atacar

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
                            estado_jogo = "trans_1" # Mesma coisa para o jogador 2, se ele acertar um navio, toca o som de acerto e verifica se todos os navios do jogador 1 foram destruídos. Se sim, define o jogador 2 como vencedor e muda o estado do jogo para a tela de vitória. Se errar, muda o estado do jogo para a transição para o jogador 1 atacar

                elif estado_jogo == "trans_1":
                    estado_jogo = "batalha1"

                elif estado_jogo == "vitoria":
                    estado_jogo = "setup1"
                    tabuleiros = [novo_tabuleiro(), novo_tabuleiro()]
                    tiros_jogadores = [[], []]
                    navios_colocados = [0, 0]
                    jogador_vencedor = 0 # Se o jogo estiver na tela de vitória e o jogador clicar, reinicia o jogo para o estado inicial

        tela_jogo.fill('darkgray') # Limpa a tela do jogo com uma cor de fundo

        if estado_jogo == "setup1":
            celula = celula_do_mouse(mouse_x, mouse_y)
            if celula:
                coluna, linha = celula
                posicao_valida = pode_colocar(tabuleiros[0], coluna, linha) # Verifica se a linha/coluna é válida e se o jogador 1 pode colocar um navio nessa posição
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiros[0], tiros_jogadores[0], False, celula) # Desenha a grade do jogo para o jogador 1, passando o tabuleiro do jogador 1, os tiros do jogador 1, e a célula do mouse para destacar a posição onde o navio pode ser colocado
            mensagem_info = f"Jogador 1: navio {navios_colocados[0] + 1}/7"
            if celula:
                if posicao_valida:
                    mensagem_info += " (valido)"
                else:
                    mensagem_info += " (invalido)"
            desenhar_info(tela_jogo, fonte_media, mensagem_info) # Desenha a mensagem de informação para o jogador 1, mostrando quantos navios foram colocados e se a posição atual do mouse é válida para colocar um navio ou não

        elif estado_jogo == "trans_p2":
            mensagem(tela_jogo, fonte_media, fonte_grande, "Jogador 1 esta pronto!", "Passe o computador ao Jogador 2", "Continuar") # Exibe uma mensagem de transição para o jogador 2, indicando que o jogador 1 está pronto e que o computador deve ser passado para o jogador 2

        elif estado_jogo == "setup2":
            celula = celula_do_mouse(mouse_x, mouse_y)
            if celula:
                coluna, linha = celula
                posicao_valida = pode_colocar(tabuleiros[1], coluna, linha)
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiros[1], tiros_jogadores[1], False, celula)
            mensagem_info = f"Jogador 2: navio {navios_colocados[1] + 1}/7"
            if celula:
                if posicao_valida:
                    mensagem_info += " (valido)"
                else:
                    mensagem_info += " (invalido)" 
            desenhar_info(tela_jogo, fonte_media, mensagem_info) # Mesma coisa para o jogador 2, desenha a grade do jogo para o jogador 2 e exibe a mensagem de informação mostrando quantos navios foram colocados e se a posição atual do mouse é válida para colocar um navio ou não

        elif estado_jogo == "trans_batalha":
            mensagem(tela_jogo, fonte_media, fonte_grande, "Batalha vai comecar!", "Jogador 1 ataca primeiro", "Iniciar") # Exibe uma mensagem de transição para a batalha

        elif estado_jogo == "batalha1":
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiros[1], tiros_jogadores[0], True) # Desenha a grade do jogo para o jogador 1, mostrando os tiros do jogador 1 no tabuleiro do jogador 2, e destacando as células onde o jogador 1 pode atirar
            navios_destruidos = contar_destruidos(tabuleiros[1], tiros_jogadores[0]) # Conta quantos navios do jogador 2 foram destruídos pelos tiros do jogador 1, usando a função contar_destruidos que verifica o tabuleiro do jogador 2 e os tiros do jogador 1 para calcular o número de navios destruídos
            desenhar_info(tela_jogo, fonte_media, f"Jogador 1 ataca! Navios destruidos: {navios_destruidos}/7") # Desenha a mensagem de informação para o jogador 1, mostrando quantos navios do jogador 2 foram destruídos pelos tiros do jogador 1, e quantos navios ainda restam para serem destruídos

        elif estado_jogo == "trans_2":
            mensagem(tela_jogo, fonte_media, fonte_grande, "Agua!", "Vez do Jogador 2", "Continuar") # Exibe uma mensagem de transição para o jogador 2, indicando que o jogador 1 errou e que é a vez do jogador 2 atacar

        elif estado_jogo == "batalha2":
            desenhar_grade(tela_jogo, fonte_pequena, tabuleiros[0], tiros_jogadores[1], True)
            navios_destruidos = contar_destruidos(tabuleiros[0], tiros_jogadores[1])
            desenhar_info(tela_jogo, fonte_media, f"Jogador 2 ataca! Navios destruidos: {navios_destruidos}/7") # Mesma coisa para o jogador 2, desenha a grade do jogo para o jogador 2, mostrando os tiros do jogador 2 no tabuleiro do jogador 1, e destacando as células onde o jogador 2 pode atirar. Também exibe a mensagem de informação para o jogador 2, mostrando quantos navios do jogador 1 foram destruídos pelos tiros do jogador 2, e quantos navios ainda restam para serem destruídos

        elif estado_jogo == "trans_1":
            mensagem(tela_jogo, fonte_media, fonte_grande, "Agua!", "Vez do Jogador 1", "Continuar") # Exibe uma mensagem de transição para o jogador 1, indicando que o jogador 2 errou e que é a vez do jogador 1 atacar

        elif estado_jogo == "vitoria":
            tela_vitoria(tela_jogo, fonte_media, fonte_grande, jogador_vencedor) # Exibe a tela de vitória, indicando qual jogador venceu o jogo

        pygame.display.flip() # Atualiza a tela do jogo para refletir as mudanças feitas durante o loop de eventos e desenho
        relogio_jogo.tick(60) # Controla a taxa de atualização do jogo, limitando a 60 quadros por segundo para garantir uma jogabilidade suave e consistente


if __name__ == "__main__":
    main()

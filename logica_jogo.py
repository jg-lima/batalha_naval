def novo_tabuleiro():
    return [[0] * 10 for _ in range(10)] # cria uma matriz 10x10 preenchida com zeros que representa agua, ou seja, sem navios. Cada célula pode conter um número inteiro que representa o ID do navio presente naquela posição. Se a célula for 0, significa que não há navio naquela posição.


def celula_do_mouse(mouse_x, mouse_y): 
    coluna = (mouse_x - 40) // 52 # -40 para ajustar a posição em relação ao início do tabuleiro e //52 para obter o índice correspondente da coluna. O tabuleiro começa a ser desenhado a partir da coordenada (40, 40) e cada célula tem um tamanho de 52 pixels
    linha = (mouse_y - 40) // 52
    if 0 <= coluna < 10 and 0 <= linha < 10:
        return coluna, linha # converte as coordenadas do mouse em índices de coluna e linha para acessar a matriz do tabuleiro. A função retorna uma tupla (coluna, linha) se as coordenadas estiverem dentro dos limites do tabuleiro, caso contrário, retorna None.


def pode_colocar(tabuleiro, coluna, linha):
    if coluna + 3 > 10:
        return False # verifica se a posição inicial mais o comprimento do navio (3 células) ultrapassa os limites do tabuleiro. Se ultrapassar, não é possível colocar o navio nessa posição.
    for deslocamento in range(3):
        if tabuleiro[linha][coluna + deslocamento] != 0:
            return False # verifica se as células onde o navio seria colocado já estão ocupadas por outro navio. Se alguma das células estiver ocupada (diferente de 0), não é possível colocar o navio nessa posição.
    return True # se as verificações anteriores forem passadas, significa que é possível colocar o navio na posição especificada, e a função retorna True.


def coloca_navio(tabuleiro, coluna, linha, id_navio):
    for deslocamento in range(3):
        tabuleiro[linha][coluna + deslocamento] = id_navio # preenche as células correspondentes ao navio com o ID do navio. O navio é colocado horizontalmente, ocupando três células consecutivas na mesma linha, começando na coluna especificada.


def aplicar_tiro(tabuleiro, tiros_jogador, coluna, linha):
    id_navio = tabuleiro[linha][coluna]
    
    if id_navio == 0:
        tiros_jogador.append((coluna, linha))
        return False
    
    # Destruir TODAS as células do navio
    for indice_linha in range(10):
        for indice_coluna in range(10):
            if tabuleiro[indice_linha][indice_coluna] == id_navio:
                tiros_jogador.append((indice_coluna, indice_linha))
    
    return True # se a função percorreu todas as células do tabuleiro e não encontrou nenhuma célula do navio que não tenha sido atingida, isso significa que o navio foi completamente destruído, e a função retorna True.


def todos_destruidos(tabuleiro, tiros_jogador):
    for linha in range(10):
        for coluna in range(10):
            if tabuleiro[linha][coluna] != 0 and (coluna, linha) not in tiros_jogador: 
                return False # verifica se há alguma célula do tabuleiro que contém um navio (diferente de 0) e que ainda não foi atingida (ou seja, cujas coordenadas não estão na lista de tiros do jogador). Se encontrar uma célula do navio que ainda não foi atingida, a função retorna False, indicando que nem todos os navios foram destruídos.
    return True # se a função percorreu todas as células do tabuleiro e não encontrou nenhuma célula de navio que não tenha sido atingida, isso significa que todos os navios foram destruídos, e a função retorna True.


def contar_destruidos(tabuleiro, tiros_jogador):
    ids_destruidos = set() # cria um conjunto para armazenar os IDs dos navios que foram completamente destruídos. O uso de um conjunto garante que cada ID de navio seja contado apenas uma vez, mesmo que o jogador tenha atingido várias partes do mesmo navio.
    for linha in range(10):
        for coluna in range(10):
            id_navio = tabuleiro[linha][coluna] # obtém o ID do navio presente na célula atual do tabuleiro. Se a célula estiver vazia (0), significa que não há navio nessa posição. Caso contrário, o ID do navio é usado para verificar se ele foi completamente destruído.
            if id_navio != 0 and (coluna, linha) in tiros_jogador:
                ids_destruidos.add(id_navio) # verifica se a célula contém um navio (ID diferente de 0) e se as coordenadas dessa célula estão na lista de tiros do jogador. Se ambas as condições forem verdadeiras, isso significa que o jogador atingiu essa parte do navio, e o ID do navio é adicionado ao conjunto de IDs destruídos. O uso de um conjunto garante que cada ID de navio seja contado apenas uma vez, mesmo que o jogador tenha atingido várias partes do mesmo navio.
    return len(ids_destruidos) # retorna o número de navios completamente destruídos, que é igual ao tamanho do conjunto de IDs destruídos. Cada ID no conjunto representa um navio que foi completamente destruído, e o número total de navios destruídos é dado pelo número de elementos únicos nesse conjunto.

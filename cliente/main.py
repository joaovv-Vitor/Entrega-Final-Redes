import pygame
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 300, 320  # Aumentamos a altura para incluir o cabeçalho
CELL_SIZE = 20  # Tamanho de cada célula do tabuleiro
ROWS, COLS = (HEIGHT - 20) // CELL_SIZE, WIDTH // CELL_SIZE  # Ajuste para o cabeçalho

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Cria a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caça-Palavras em Português")

# Fonte para exibir as letras e o cabeçalho
font = pygame.font.SysFont(None, 25)
header_font = pygame.font.SysFont(None, 35)

# Lista de palavras em português para o jogo
#WORDS = ["PYTHON", "JOGO", "PROGRAMA", "DIVERSÃO", "TECLADO", "MOUSE", "TELA", "CÓDIGO"]

WORDS = [
    "AMOR", "CASA", "FELIZ", "JOGO", "LIVRO", "MUNDO", "TEMPO", "VIDA",
    "SOL", "LUZ", "MAR", "RIO", "FLOR", "ÁRVORE", "PRAIA", "CAMPO",
    "FUTURO", "PASSADO", "PRESENTE", "FAMÍLIA", "AMIGO", "ESCOLA", "TRABALHO"
]

# Letras mais comuns no português (para gerar o tabuleiro)
LETRAS_PT = [
    'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A',  # Letra A é muito comum
    'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',  # Letra E é muito comum
    'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O',  # Letra O é muito comum
    'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S',            # Letra S é comum
    'R', 'R', 'R', 'R', 'R', 'R',                      # Letra R é comum
    'I', 'I', 'I', 'I', 'I',                           # Letra I é comum
    'D', 'D', 'D', 'D',                                # Letra D é comum
    'M', 'M', 'M',                                     # Letra M é comum
    'N', 'N', 'N',                                     # Letra N é comum
    'C', 'C', 'C',                                     # Letra C é comum
    'P', 'P', 'P',                                     # Letra P é comum
    'T', 'T', 'T',                                     # Letra T é comum
    'B', 'B',                                          # Letra B é menos comum
    'L', 'L',                                          # Letra L é menos comum
    'U', 'U',                                          # Letra U é menos comum
    'G', 'G',                                          # Letra G é menos comum
    'V', 'V',                                          # Letra V é menos comum
    'F', 'F',                                          # Letra F é menos comum
    'H', 'H',                                          # Letra H é menos comum
    'J', 'J',                                          # Letra J é menos comum
    'Q', 'Q',                                          # Letra Q é menos comum
    'X', 'X',                                          # Letra X é menos comum
    'Z', 'Z',                                          # Letra Z é menos comum
]

# Função para gerar o tabuleiro com palavras inseridas
def generate_board(rows, cols):
    board = [[random.choice(LETRAS_PT) for _ in range(cols)] for _ in range(rows)]
    
    # Insere as palavras no tabuleiro
    for word in WORDS:
        direction = random.choice(["horizontal", "vertical"])
        if direction == "horizontal":
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - len(word))
            for i, letter in enumerate(word):
                board[row][col + i] = letter
        elif direction == "vertical":
            row = random.randint(0, rows - len(word))
            col = random.randint(0, cols - 1)
            for i, letter in enumerate(word):
                board[row + i][col] = letter
    
    return board

# Função para desenhar o tabuleiro
def draw_board(board, selected_cells):
    for row in range(ROWS):
        for col in range(COLS):
            letter = board[row][col]
            color = GREEN if (row, col) in selected_cells else BLACK
            text = font.render(letter, True, color)
            screen.blit(text, (col * CELL_SIZE + 5, row * CELL_SIZE + 45))  # Ajuste para o cabeçalho
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE), 1)

# Função para desenhar o cabeçalho
def draw_header(found_words):
    header_text = f"Encontradas: {found_words}/{len(WORDS)}"
    text = header_font.render(header_text, True, BLACK)
    screen.blit(text, (10, 10))

# Função para verificar se a seleção forma uma palavra válida
def check_word(board, selected_cells):
    word = "".join([board[row][col] for row, col in selected_cells])
    return word in WORDS

# Função principal do jogo
def main():
    board = generate_board(ROWS, COLS)
    selected_cells = []  # Células selecionadas pelo jogador
    found_words = 0  # Contador de palavras encontradas
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = (y - 40) // CELL_SIZE  # Ajuste para o cabeçalho
                if 0 <= row < ROWS and 0 <= col < COLS:  # Verifica se o clique está dentro do tabuleiro
                    if (row, col) not in selected_cells:
                        selected_cells.append((row, col))
                    else:
                        selected_cells.remove((row, col))
                    
                    # Verifica se a seleção forma uma palavra válida
                    if check_word(board, selected_cells):
                        found_words += 1
                        print(f"Parabéns! Você encontrou a palavra: {''.join([board[row][col] for row, col in selected_cells])}")
                        selected_cells = []  # Limpa a seleção após encontrar uma palavra

        screen.fill(WHITE)
        draw_header(found_words)  # Desenha o cabeçalho
        draw_board(board, selected_cells)  # Desenha o tabuleiro
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
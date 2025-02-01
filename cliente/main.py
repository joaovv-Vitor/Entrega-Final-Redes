import socket
import pygame

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 5000         # Porta do servidor

# Configurações da tela
WIDTH, HEIGHT = 600, 640
CELL_SIZE = 40
ROWS, COLS = 10, 10

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caça-Palavras (Cliente)")

# Fonte para exibir as letras e o cabeçalho
font = pygame.font.SysFont(None, 25)
header_font = pygame.font.SysFont(None, 35)

# Função para desenhar o tabuleiro
def draw_board(board, selected_cells):
    for row in range(ROWS):
        for col in range(COLS):
            letter = board[row][col]
            color = GREEN if (row, col) in selected_cells else BLACK
            text = font.render(letter, True, color)
            screen.blit(text, (col * CELL_SIZE + 5, row * CELL_SIZE + 85))  # Ajuste para o cabeçalho
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE + 80, CELL_SIZE, CELL_SIZE), 1)

# Função para desenhar o cabeçalho
def draw_header(score, found_words):
    header_text = f"Pontuação: {score}"
    text = header_font.render(header_text, True, BLACK)
    screen.blit(text, (10, 10))

# Função principal do cliente
def main():
    # Conecta ao servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"Conectado ao servidor {HOST}:{PORT}")

        # Recebe o tabuleiro do servidor
        board_data = client_socket.recv(4096).decode()
        board = eval(board_data)  # Converte a string de volta para lista
        print("Tabuleiro recebido:", board)

        selected_cells = []  # Células selecionadas pelo jogador
        found_words = []     # Lista de palavras encontradas pelo jogador
        score = 0            # Pontuação do jogador
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // CELL_SIZE
                    row = (y - 80) // CELL_SIZE  # Ajuste para o cabeçalho
                    if 0 <= row < ROWS and 0 <= col < COLS:  # Verifica se o clique está dentro do tabuleiro
                        if (row, col) not in selected_cells:
                            selected_cells.append((row, col))
                        else:
                            selected_cells.remove((row, col))

                        # Envia as células selecionadas para o servidor
                        client_socket.sendall(str(selected_cells).encode())

                        # Recebe a resposta do servidor
                        response = client_socket.recv(1024).decode()
                        print("Resposta do servidor:", response)

                        # Recebe a pontuação e a lista de palavras encontradas
                        progress_data = client_socket.recv(1024).decode()
                        progress = eval(progress_data)
                        score = progress["score"]
                        found_words = progress["found_words"]
                        print(f"Pontuação: {score} | Palavras encontradas: {found_words}")

            screen.fill(WHITE)
            draw_header(score, found_words)  # Desenha o cabeçalho
            draw_board(board, selected_cells)  # Desenha o tabuleiro
            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
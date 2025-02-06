import socket
import pygame
import ast

BROADCAST_PORT = 5001
TCP_PORT = 5000
BROADCAST_MSG = "DISCOVERY_REQUEST"
BUFFER_SIZE = 4096

WIDTH, HEIGHT = 600, 640
CELL_SIZE = 40
ROWS, COLS = 10, 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (200, 50, 50)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caça-Palavras (Cliente)")

font = pygame.font.SysFont(None, 25)
header_font = pygame.font.SysFont(None, 35)

def discover_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_socket.settimeout(3)

        print("Procurando servidor...")
        udp_socket.sendto(BROADCAST_MSG.encode(), ('<broadcast>', BROADCAST_PORT))
        
        try:
            data, addr = udp_socket.recvfrom(1024)
            if data.decode() == "DISCOVERY_RESPONSE":
                print(f"Servidor encontrado em {addr[0]}")
                return addr[0]
        except socket.timeout:
            print("Nenhuma resposta do servidor encontrada.")
            return None

def draw_board(board, selected_cells):
    for row in range(ROWS):
        for col in range(COLS):
            letter = board[row][col]
            color = GREEN if (row, col) in selected_cells else BLACK
            text = font.render(letter, True, color)
            screen.blit(text, (col * CELL_SIZE + 5, row * CELL_SIZE + 85))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE + 80, CELL_SIZE, CELL_SIZE), 1)

def draw_header(score, found_words):
    header_text = f"Pontuação: {score}"
    text = header_font.render(header_text, True, BLACK)
    screen.blit(text, (10, 10))

def draw_ranking(rankings):
    y_offset = 80  
    x_offset = 420

    for i, (name, score) in enumerate(rankings, start=1):
        ranking_text = f"{i}. {name}: {score} pontos"
        text = font.render(ranking_text, True, BLACK)
        screen.blit(text, (x_offset, y_offset))
        y_offset += 20

def get_nickname():
    input_box = pygame.Rect(150, 200, 300, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    nickname = None

    while nickname is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        nickname = text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        instruction = font.render("Digite seu nickname e pressione ENTER:", True, BLACK)
        screen.blit(instruction, (input_box.x, input_box.y - 30))

        pygame.display.flip()

    return nickname

def draw_ranking_final(rankings):
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 50)

    screen.fill(WHITE)

    # Título
    title_text = title_font.render("Ranking Final", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))

    # Desenha os rankings
    for i, (name, score) in enumerate(rankings, start=1):
        text = font.render(f"{i}. {name} - {score} pontos", True, RED if name == "Você" else BLACK)
        screen.blit(text, (WIDTH // 4, 100 + i * 40))

    #Desenha o botão de reiniciar
    restart_button_rect = pygame.Rect(WIDTH // 2 - 175, HEIGHT - 80, 150, 50)
    pygame.draw.rect(screen, GRAY, restart_button_rect)
    restart_button_text = font.render("Reiniciar", True, BLACK)
    screen.blit(restart_button_text, (WIDTH // 2 - 175 + (150 - restart_button_text.get_width()) // 2, HEIGHT - 65))

    # Desenha o botão de atualizar ranking
    update_button_rect = pygame.Rect(WIDTH // 2 + 25, HEIGHT - 80, 150, 50)
    pygame.draw.rect(screen, GRAY, update_button_rect)
    update_button_text = font.render("Atualizar", True, BLACK)
    screen.blit(update_button_text, (WIDTH // 2 + 25 + (150 - update_button_text.get_width()) // 2, HEIGHT - 65))

    pygame.display.flip()

    return update_button_rect ,restart_button_rect

def main():
    server_ip = discover_server()
    if not server_ip:
        print("Não foi possível encontrar o servidor. Verifique se o servidor está ativo e na mesma rede.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Conectando ao servidor em {server_ip}:{TCP_PORT}...")
            client_socket.connect((server_ip, TCP_PORT))
            print("Conexão estabelecida com o servidor.")

            nickname = get_nickname()
            if nickname is None:
                return
            client_socket.recv(4096).decode()
            client_socket.sendall(nickname.encode())

            board_data = client_socket.recv(4096).decode()
            board = ast.literal_eval(board_data)
            print("Tabuleiro recebido:", board)

            selected_cells = []
            found_words = []
            score = 0
            rankings = []
            running = True
            game_over = False

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                        x, y = pygame.mouse.get_pos()
                        col = x // CELL_SIZE
                        row = (y - 80) // CELL_SIZE
                        if 0 <= row < ROWS and 0 <= col < COLS:
                            if (row, col) not in selected_cells:
                                selected_cells.append((row, col))
                            else:
                                selected_cells.remove((row, col))

                            client_socket.sendall(str(selected_cells).encode())

                            response = client_socket.recv(1024).decode()
                            print("Resposta do servidor:", response)

                            progress_data = client_socket.recv(1024).decode()
                            progress = ast.literal_eval(progress_data)
                            score = progress["score"]
                            found_words = progress["found_words"]
                            rankings = progress["rankings"]
                            print(f"Pontuação: {score} | Palavras encontradas: {found_words}")
                            print("Ranking:", rankings)
                            if "Palavra encontrada" in response:
                                selected_cells = []

                            if score == 5:
                                game_over = True

                    elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                        # if restart_button_rect.collidepoint(event.pos):
                        #     print("Reiniciando tela...")
                        #     rankings = [("Você", 0)]
                        #     game_over = False
                        #     selected_cells = []
                        #     found_words = []
                        #     score = 0
                        if update_button_rect.collidepoint(event.pos):
                            print("Atualizando ranking...")
                            client_socket.sendall("update_ranking".encode())
                            updated_rankings_data = client_socket.recv(1024).decode()
                            rankings = ast.literal_eval(updated_rankings_data)
                            print("Ranking atualizado:", rankings)

                screen.fill(WHITE)
                draw_header(score, found_words)
                draw_board(board, selected_cells)
                draw_ranking(rankings)

                if game_over:
                    restart_button_rect, update_button_rect = draw_ranking_final(rankings)

                pygame.display.flip()

                if game_over:
                    try:
                        client_socket.setblocking(False)
                        progress_data = client_socket.recv(1024).decode()
                        if progress_data:
                            progress = ast.literal_eval(progress_data)
                            rankings = progress["rankings"]
                            print("Ranking atualizado:", rankings)
                    except BlockingIOError:
                        pass
                    except Exception as e:
                        print(f"Erro ao receber dados do servidor: {e}")

    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor. Verifique se o servidor está ativo.")
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
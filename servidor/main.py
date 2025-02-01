import socket
import random
import string
from threading import Thread

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 5000         # Porta do servidor

# Configurações do tabuleiro
ROWS, COLS = 10, 10
WORDS = ["PYTHON", "JOGO", "PROGRAMA", "DIVERSÃO"]

# Função para gerar o tabuleiro
def generate_board():
    board = [[random.choice(string.ascii_uppercase) for _ in range(COLS)] for _ in range(ROWS)]
    for word in WORDS:
        direction = random.choice(["horizontal", "vertical"])
        if direction == "horizontal":
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - len(word))
            for i, letter in enumerate(word):
                board[row][col + i] = letter
        elif direction == "vertical":
            row = random.randint(0, ROWS - len(word))
            col = random.randint(0, COLS - 1)
            for i, letter in enumerate(word):
                board[row + i][col] = letter
    return board

# Função para verificar se a seleção forma uma palavra válida
def check_word(board, selected_cells):
    word = "".join([board[row][col] for row, col in selected_cells])
    return word in WORDS

# Classe para gerenciar cada cliente
class ClientHandler(Thread):
    def __init__(self, conn, addr, board):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.board = board
        self.found_words = []  # Lista de palavras encontradas pelo jogador
        self.score = 0         # Pontuação do jogador (palavras acertadas)

    def run(self):
        print(f"Novo cliente conectado: {self.addr}")

        # Envia o tabuleiro para o cliente
        self.conn.sendall(str(self.board).encode())

        while True:
            try:
                # Recebe as células selecionadas pelo cliente
                data = self.conn.recv(1024).decode()
                if not data:
                    break

                selected_cells = eval(data)  # Converte a string de volta para lista
                print(f"Cliente {self.addr} selecionou: {selected_cells}")

                # Verifica se a seleção forma uma palavra válida
                word = "".join([self.board[row][col] for row, col in selected_cells])
                if word in WORDS and word not in self.found_words:
                    self.found_words.append(word)
                    self.score += 1  # Incrementa a pontuação
                    self.conn.sendall(f"Palavra encontrada: {word}".encode())
                else:
                    self.conn.sendall("Palavra não encontrada.".encode())

                # Envia a pontuação e a lista de palavras encontradas para o cliente
                response = {
                    "score": self.score,
                    "found_words": self.found_words
                }
                self.conn.sendall(str(response).encode())
            except Exception as e:
                print(f"Erro com o cliente {self.addr}: {e}")
                break

        print(f"Cliente {self.addr} desconectado.")
        self.conn.close()

# Inicia o servidor
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor iniciado em {HOST}:{PORT}. Aguardando conexões...")

        # Gera o tabuleiro (compartilhado entre todos os clientes)
        board = generate_board()
        print("Tabuleiro gerado:", board)

        while True:
            conn, addr = server_socket.accept()
            client_handler = ClientHandler(conn, addr, board)
            client_handler.start()

if __name__ == "__main__":
    start_server()
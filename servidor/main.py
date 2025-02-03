import socket
import random
import string
from threading import Thread

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 5000         # Porta do servidor

# Configurações do tabuleiro
ROWS, COLS = 10, 10


#sortear palavras
bancoPalavras = [
    "AMOR", "CASA", "FELIZ", "JOGO", "LIVRO", "MUNDO", "TEMPO", "VIDA",
    "SOL", "LUZ", "MAR", "RIO", "FLOR", "ÁRVORE", "PRAIA", "CAMPO",
    "FUTURO", "PASSADO", "PRESENTE", "FAMÍLIA", "AMIGO", "ESCOLA", "TRABALHO"
]

WORDS = random.sample(bancoPalavras, 5)


# Lista para armazenar os rankings (nickname, score)
rankings = []

# Função para gerar o tabuleiro
def generate_board():
    # Inicializa o tabuleiro com espaços vazios
    board = [[' ' for _ in range(COLS)] for _ in range(ROWS)]
    
    # Função para verificar se uma palavra pode ser colocada em uma determinada posição
    def can_place_word(word, row, col, direction):
        if direction == "horizontal":
            if col + len(word) > COLS:
                return False
            for i in range(len(word)):
                if board[row][col + i] != ' ' and board[row][col + i] != word[i]:
                    return False
        elif direction == "vertical":
            if row + len(word) > ROWS:
                return False
            for i in range(len(word)):
                if board[row + i][col] != ' ' and board[row + i][col] != word[i]:
                    return False
        return True
    
    # Função para colocar uma palavra no tabuleiro
    def place_word(word, row, col, direction):
        if direction == "horizontal":
            for i in range(len(word)):
                board[row][col + i] = word[i]
        elif direction == "vertical":
            for i in range(len(word)):
                board[row + i][col] = word[i]
    
    # Coloca as palavras no tabuleiro
    for word in WORDS:
        placed = False
        attempts = 0
        while not placed and attempts < 1000:
            direction = random.choice(["horizontal", "vertical"])
            if direction == "horizontal":
                row = random.randint(0, ROWS - 1)
                col = random.randint(0, COLS - len(word))
            elif direction == "vertical":
                row = random.randint(0, ROWS - len(word))
                col = random.randint(0, COLS - 1)
            
            if can_place_word(word, row, col, direction):
                place_word(word, row, col, direction)
                placed = True
            attempts += 1
        
        if not placed:
            raise ValueError(f"Não foi possível colocar a palavra: {word}")
    
    # Preenche os espaços vazios com letras aleatórias
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == ' ':
                board[row][col] = random.choice(string.ascii_uppercase)
    
    return board

# Classe para gerenciar cada cliente
class ClientHandler(Thread):
    def __init__(self, conn, addr, board):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.board = board
        self.found_words = []  # Lista de palavras encontradas pelo jogador
        self.score = 0         # Pontuação do jogador (palavras acertadas)
        self.nickname = None   # Nickname do jogador

    def run(self):
        #print(WORDS)
        print(f"Novo cliente conectado: {self.addr}")

        # Solicita o nickname do cliente
        self.conn.sendall("Digite seu nickname: ".encode())
        self.nickname = self.conn.recv(1024).decode().strip()
        print(f"Cliente {self.addr} escolheu o nickname: {self.nickname}")

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

                    # Atualiza o ranking
                    updated = False
                    for i, (name, old_score) in enumerate(rankings):
                        if name == self.nickname:
                            rankings[i] = (self.nickname, self.score)  # Atualiza a pontuação
                            updated = True
                            break

                    if not updated:
                        rankings.append((self.nickname, self.score))  # Adiciona novo jogador ao ranking

                    rankings.sort(key=lambda x: x[1], reverse=True)  # Ordena por score
                else:
                    self.conn.sendall("Palavra não encontrada.".encode())

                # Envia a pontuação, a lista de palavras encontradas e o ranking para o cliente
                response = {
                    "score": self.score,
                    "found_words": self.found_words,
                    "rankings": rankings[:10]  # Envia apenas os top 10
                }
                self.conn.sendall(str(response).encode())
            except Exception as e:
                print(f"Erro com o cliente {self.addr}: {e}")
                break

        print(f"Cliente {self.addr} desconectado.")
        self.remove_from_ranking()
        self.conn.close()

    def remove_from_ranking(self):
        """Remove o nickname e o score do ranking quando o cliente se desconecta."""
        global rankings
        rankings = [(name, score) for name, score in rankings if name != self.nickname]
        print(f"Ranking atualizado após desconexão de {self.nickname}: {rankings}")

# Inicia o servidor
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor iniciado em {HOST}:{PORT}. Aguardando conexões...")

        # Gera o tabuleiro (compartilhado entre todos os clientes)
        board = generate_board()
        print("Tabuleiro gerado:")
        for row in board:
            print(' '.join(row))
        print(WORDS)

        while True:
            conn, addr = server_socket.accept()
            client_handler = ClientHandler(conn, addr, board)
            client_handler.start()

if __name__ == "__main__":
    start_server()
class Player():
    def __init__(self, conn, addr, name):
        self.conn = conn  # Conexão do jogador (socket)
        self.addr = addr  # Endereço do jogador
        self.name = name  # Nome do jogador
        self.score = 0  # Pontuação do jogador
        self.turn = False  # Define se é o turno do jogador


    def add_score(self, points):
        """Adiciona pontos ao jogador."""
        self.score += points

    def set_name(sef, name):
        """Setar nome do jogador."""
        sef.name = name



    
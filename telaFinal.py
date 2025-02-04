import pygame

# Inicializa o Pygame
pygame.init()

# Definições de tela
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fim de Jogo - Ranking")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)

# Fonte
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 50)

# Ranking fictício (nome, pontos)
ranking = [
    ("Alice", 120),
    ("Bob", 100),
    ("Carlos", 85),
    ("Você", 90)  # Simulando o jogador atual
]

# Função para desenhar a tela de ranking
def draw_ranking():
    screen.fill(WHITE)  # Fundo branco

    # Título
    title_text = title_font.render("Ranking Final", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 30))

    # Lista do ranking
    for i, (name, score) in enumerate(ranking):
        text = font.render(f"{i + 1}. {name} - {score} pontos", True, RED if name == "Você" else BLACK)
        screen.blit(text, (WIDTH // 4, 100 + i * 40))

    pygame.display.flip()

# Loop do jogo
running = True
while running:
    draw_ranking()  # Atualiza a tela
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

pygame.quit()

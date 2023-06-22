import pygame
import random
import time
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600
INITIAL_POSITION_X = WINDOWS_WIDTH / 2
INITIAL_POSITION_Y = WINDOWS_HEIGHT / 2
BLOCK = 10
KEY_DIRECTION = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

SCORE_AREA_WIDTH = WINDOWS_WIDTH
SCORE_AREA_HEIGHT = 50
SCORE_AREA_POSITION = (0, 0)

score = 0
speed = 10


pygame.init()
pygame.display.set_caption("Kobra Come - A Python Snake Game")


def collision(pos1, pos2):
    """Verifica se duas posições colidem.

    Args:
        pos1 (tuple): Primeira posição (x, y).
        pos2 (tuple): Segunda posição (x, y).

    Returns:
        bool: True se as posições colidirem, False caso contrário.
    """
    return pos1 == pos2


def game_over():
    """Exibe a mensagem de Game Over e encerra o jogo."""
    game_over_font = pygame.font.SysFont("arial", 60, True, True)
    game_over_text = "GAME OVER"
    text_over = game_over_font.render(game_over_text, True, (255, 255, 255))
    window.blit(text_over, (100, 300))
    pygame.display.update()
    time.sleep(5)
    pygame.quit()
    quit()


def check_margins(pos):
    """Verifica se a posição está dentro dos limites da janela.

    Args:
        pos (tuple): Posição (x, y) a ser verificada.

    Returns:
        bool: True se a posição estiver fora dos limites da janela, False caso contrário.
    """
    if 0 <= pos[0] < WINDOWS_WIDTH and SCORE_AREA_HEIGHT <= pos[1] < WINDOWS_HEIGHT:
        return False
    else:
        return True


def generate_random_position():
    """Gera uma posição aleatória dentro dos limites da janela, evitando
       colisões com obstáculos e a cobra.

    Returns:
        tuple: Posição aleatória gerada (x, y).
    """
    x = random.randint(0, WINDOWS_WIDTH - BLOCK) // BLOCK * BLOCK
    y = random.randint(SCORE_AREA_HEIGHT, WINDOWS_HEIGHT - BLOCK) // BLOCK * BLOCK

    if (x, y) in obstacle_position or (x, y) in kobra_position:
        return generate_random_position()

    return x, y


pygame.font.init()
font = pygame.font.SysFont("arial", 20, True, True)

window = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))

obstacle_position = []
obstacle_surface = pygame.Surface((BLOCK, BLOCK))
obstacle_surface.fill((0, 0, 0))

kobra_position = [
    (INITIAL_POSITION_X, INITIAL_POSITION_Y),
    (INITIAL_POSITION_X + BLOCK, INITIAL_POSITION_Y),
    (INITIAL_POSITION_X + 2 * BLOCK, INITIAL_POSITION_Y),
]
kobra_surface = pygame.Surface((BLOCK, BLOCK))
kobra_surface.fill((53, 59, 72))
direction = K_LEFT

apple_surface = pygame.Surface((BLOCK, BLOCK))
apple_surface.fill((255, 0, 0))
apple_position = generate_random_position()


while True:
    pygame.time.Clock().tick(speed)
    window.fill((68, 189, 50))

    message = f"Pontos: {score}"
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOWS_WIDTH // 2, SCORE_AREA_HEIGHT // 2))

    pygame.draw.rect(window, (0, 0, 0), (0, 0, SCORE_AREA_WIDTH, SCORE_AREA_HEIGHT))
    window.blit(text, text_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key in KEY_DIRECTION:
                if event.key == K_UP and direction == K_DOWN:
                    continue
                elif event.key == K_DOWN and direction == K_UP:
                    continue
                elif event.key == K_LEFT and direction == K_RIGHT:
                    continue
                elif event.key == K_RIGHT and direction == K_LEFT:
                    continue
                else:
                    direction = event.key

    window.blit(apple_surface, apple_position)

    if collision(kobra_position[0], apple_position):
        kobra_position.append((-10, -10))
        apple_position = generate_random_position()
        obstacle_position.append(generate_random_position())
        score += 1
        if score % 5 == 0:
            speed += 2

    for pos in obstacle_position:
        if collision(kobra_position[0], pos):
            game_over()
        window.blit(obstacle_surface, pos)

    for pos in kobra_position:
        window.blit(kobra_surface, pos)

    for item in range(len(kobra_position) - 1, 0, -1):
        if collision(kobra_position[0], kobra_position[item]):
            game_over()
        kobra_position[item] = kobra_position[item - 1]

    if check_margins(kobra_position[0]):
        game_over()

    if direction == K_RIGHT:
        # Movimenta para a direita
        kobra_position[0] = (
            kobra_position[0][0] + BLOCK,
            kobra_position[0][1],
        )

    elif direction == K_LEFT:
        # Movimenta para a esquerda
        kobra_position[0] = (
            kobra_position[0][0] - BLOCK,
            kobra_position[0][1],
        )

    elif direction == K_UP:
        # Movimenta para cima
        kobra_position[0] = (
            kobra_position[0][0],
            kobra_position[0][1] - BLOCK,
        )

    elif direction == K_DOWN:
        # Movimenta para baixo
        kobra_position[0] = (
            kobra_position[0][0],
            kobra_position[0][1] + BLOCK,
        )

    pygame.display.update()

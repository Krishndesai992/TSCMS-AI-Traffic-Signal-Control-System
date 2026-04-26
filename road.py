import pygame

WIDTH, HEIGHT = 800, 800
CENTER = WIDTH // 2

GRAY=(100,100,100)
BLACK=(0,0,0)

def draw_roads(screen):
    screen.fill(GRAY)
    pygame.draw.rect(screen, BLACK, (CENTER-100,0,200,HEIGHT))
    pygame.draw.rect(screen, BLACK, (0,CENTER-100,WIDTH,200))
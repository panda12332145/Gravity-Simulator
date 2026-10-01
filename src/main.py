"""Loop principal do Gravity-Simulator (Pygame).

Teclas:
  ESC  — sair
  ESPAÇO — pausar/continuar
  R    — reiniciar o sistema
"""
import pygame

from .planet import HEIGHT, WIDTH, Planet
from .system import GravitySystem


def build_system() -> GravitySystem:
    earth = Planet("Earth", 20, 10, (0, 100, 255), 200, 100, 0, 0.3)
    sun = Planet("Sun", 30, 1000, (255, 220, 0), 512, 350, 0, 0.0)
    moon = Planet("Moon", 10, 1, (200, 200, 200), 250, 100, 45, 0.5)
    return GravitySystem([earth, sun, moon])


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gravity Simulator")
    clock = pygame.time.Clock()

    system = build_system()
    system.attach_surface(screen)

    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    pygame.display.set_caption(
                        "Gravity Simulator — [PAUSADO]" if paused
                        else "Gravity Simulator")
                elif event.key == pygame.K_r:
                    system = build_system()
                    system.attach_surface(screen)
                    paused = False
                    pygame.display.set_caption("Gravity Simulator")

        if not paused:
            system.step(draw=True)
            pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

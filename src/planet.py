"""Corpo celeste: estado físico, integração de Euler e desenho."""
import math
from collections import deque

import pygame

WIDTH, HEIGHT = 1024, 700
G = 0.1          # constante gravitacional (unidades de tela)
TRAIL_MAX = 600  # tamanho máximo da trilha (evita vazamento de memória)


class Planet:
    def __init__(self, name: str, radius: int, mass: float, color: tuple,
                 x: float, y: float, angle: float, speed: float):
        self.name = name
        self.radius = radius
        self.mass = mass
        self.color = color
        self.pos_x = x
        self.pos_y = y
        # velocidade inicial em coordenadas polares (ângulo em graus)
        self.vel_x = speed * math.sin(math.radians(angle))
        self.vel_y = speed * math.cos(math.radians(angle))
        self.trail = deque([(x, y)], maxlen=TRAIL_MAX)

    def apply_acceleration(self, ax: float, ay: float) -> None:
        """Euler semi-implícito: atualiza velocidade, depois posição."""
        self.vel_x += ax
        self.vel_y += ay
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        self.trail.append((self.pos_x, self.pos_y))

    def draw(self, surface) -> None:
        for pos in self.trail:
            surface.fill((255, 255, 255),
                         (int(pos[0]), int(pos[1]), 1, 1))
        pygame.draw.circle(
            surface, self.color,
            (int(self.pos_x), int(self.pos_y)), self.radius)

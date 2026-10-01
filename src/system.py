"""Sistema N-corpos: força gravitacional mútua vetorial.

Correção de lógica em relação ao código original: as contribuições de
CADA corpo são SOMADAS (ax += ...), e não sobrescritas — antes, com 3+
corpos, apenas a última força era aplicada e o resultado estava errado.
"""
import math

from .planet import G, Planet


class GravitySystem:
    def __init__(self, planets: list):
        self.planets = planets
        self._surface = None

    def attach_surface(self, surface):
        self._surface = surface

    def net_acceleration(self, planet: Planet) -> tuple:
        """Aceleração resultante (ax, ay) sobre `planet` — soma vetorial
        de G·m_outro/r² em cada direção."""
        ax = ay = 0.0
        for other in self.planets:
            if other is planet:
                continue
            dx = other.pos_x - planet.pos_x
            dy = other.pos_y - planet.pos_y
            dist2 = dx * dx + dy * dy
            if dist2 < 100:          # raio de corte (dist < 10 px): evita
                continue             # força singular quando corpos colidem
            dist = math.sqrt(dist2)
            a = G * other.mass / dist2
            ax += a * dx / dist      # componente x do versor direção
            ay += a * dy / dist      # componente y do versor direção
        return ax, ay

    def step(self, draw: bool = True) -> None:
        """Avança um frame: calcula TODAS as acelerações antes de mover
        (integração símplecticamente conservadora) e depois desenha."""
        accelerations = [(p, *self.net_acceleration(p)) for p in self.planets]
        if draw and self._surface is not None:
            self._surface.fill((0, 0, 0))
        for planet, ax, ay in accelerations:
            planet.apply_acceleration(ax, ay)
            if draw and self._surface is not None:
                planet.draw(self._surface)

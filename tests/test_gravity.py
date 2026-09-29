"""Testes do Gravity-Simulator (matemática + smoke headless)."""
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")  # headless
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.planet import TRAIL_MAX, Planet
from src.system import GravitySystem, G


def _body(name, mass, x, y):
    return Planet(name, 5, mass, (255, 255, 255), x, y, 0, 0)


def test_two_body_symmetry():
    """A força de A em B deve ser igual e oposta à de B em A
    (ação = reação: m_A·a_A = -m_B·a_B)."""
    a = _body("A", 10, 0, 0)
    b = _body("B", 40, 100, 0)
    sys2 = GravitySystem([a, b])
    ax_a, ay_a = sys2.net_acceleration(a)
    ax_b, ay_b = sys2.net_acceleration(b)
    assert ax_a > 0 and ax_b < 0, "devem se atrair em x"
    assert abs(a.mass * ax_a + b.mass * ax_b) < 1e-9, "3ª lei de Newton violada"
    assert abs(ay_a) < 1e-12 and abs(ay_b) < 1e-12


def test_three_body_accumulates():
    """Regressão do bug original: com 3 corpos, as duas contribuições
    devem ser SOMADAS (antes, a última sobrescrevia a anterior)."""
    c = _body("C", 1, 0, 0)          # alvo
    left = _body("L", 1000, -200, 0) # puxa para -x
    right = _body("R", 1000, 200, 0) # puxa para +x
    sys3 = GravitySystem([c, left, right])
    ax, ay = sys3.net_acceleration(c)
    # simétricos: força líquida ~0 (massas iguais, distâncias iguais)
    assert abs(ax) < 1e-9, f"deveria cancelar, veio {ax}"
    # agora torna R mais massivo: resultado líquido deve virar +x
    right.mass = 4000
    ax2, _ = sys3.net_acceleration(c)
    assert ax2 > 0, "a contribuição do corpo mais massivo deve dominar"
    # e a soma é exatamente o valor de cada isolado somado
    right.mass = 1000
    GravitySystem([c, left]).net_acceleration(c)  # só L
    GravitySystem([c, right]).net_acceleration(c)  # só R
    ax_l, _ = GravitySystem([c, left]).net_acceleration(c)
    ax_r, _ = GravitySystem([c, right]).net_acceleration(c)
    GravitySystem([c, left, right])
    ax_total, _ = sys3.net_acceleration(c)
    assert abs((ax_l + ax_r) - ax_total) < 1e-9, "soma vetorial incorreta"


def test_trail_is_capped():
    """Trilha usa deque com maxlen (o legado crescia sem limite)."""
    a = _body("A", 1, 0, 0)
    b = _body("B", 100, 300, 0)
    sys2 = GravitySystem([a, b])
    for _ in range(TRAIL_MAX + 400):
        sys2.step(draw=False)
    assert len(a.trail) <= TRAIL_MAX
    assert len(a.trail) == TRAIL_MAX


def test_smoke_pygame_headless():
    """30 frames com driver dummy (sem display)."""
    import pygame
    from src.main import build_system
    from src.planet import WIDTH, HEIGHT

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    system = build_system()
    system.attach_surface(screen)
    for _ in range(30):
        system.step(draw=True)
        pygame.display.flip()
    pygame.quit()
    # corpos ainda na tela (não explodiram numericamente)
    for p in system.planets:
        assert abs(p.pos_x) < WIDTH * 10 and abs(p.pos_y) < HEIGHT * 10, \
            f"{p.name} divergiu numericamente"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"✅ {fn.__name__}")
    print(f"\n{len(fns)} testes passaram.")

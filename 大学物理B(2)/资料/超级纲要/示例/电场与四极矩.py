"""SI单位：用独立微元求和，核对第02章解析式与四极远场。"""
from math import cos, sin, pi, sqrt, isclose

K = 8.99e9


def rod_sum(half_length, height, density, pieces):
    dx = 2 * half_length / pieces
    ex = ey = 0.0
    for i in range(pieces):
        x = -half_length + (i + 0.5) * dx
        distance = sqrt(x*x + height*height)
        coefficient = K * density * dx / distance**3
        ex += coefficient * (-x)
        ey += coefficient * height
    return ex, ey


def ring_sum(radius, height, charge, pieces):
    ex = ey = ez = 0.0
    for i in range(pieces):
        angle = 2*pi*(i+0.5)/pieces
        # 从源点(radius*cos, radius*sin, 0)指向(0,0,height)。
        rx, ry, rz = -radius*cos(angle), -radius*sin(angle), height
        distance = sqrt(rx*rx + ry*ry + rz*rz)
        coefficient = K*(charge/pieces)/distance**3
        ex += coefficient*rx
        ey += coefficient*ry
        ez += coefficient*rz
    return ex, ey, ez


def main():
    length, height, density = 0.15, 0.20, 4e-9
    ex, ey = rod_sum(length, height, density, 4000)
    exact = 2*K*density*length/(height*sqrt(length**2+height**2))
    assert abs(ex) < 1e-8
    assert isclose(ey, exact, rel_tol=1e-7)
    print(f"细棒：微元求和Ey={ey:.6f} N/C；解析式={exact:.6f} N/C")

    radius, height, charge = 0.10, 0.10, 1e-9
    ex, ey, ez = ring_sum(radius, height, charge, 4000)
    exact = K*charge*height/(radius**2+height**2)**1.5
    assert abs(ex) < 1e-8 and abs(ey) < 1e-8
    assert isclose(ez, exact, rel_tol=1e-12)
    print(f"圆环：微元求和Ez={ez:.6f} N/C；解析式={exact:.6f} N/C")

    q, a, observation = 1e-9, 0.01, 0.10
    charges = [(q, 0., 0., a), (q, 0., 0., -a), (-2*q, 0., 0., 0.)]
    tensor = [[0.]*3 for _ in range(3)]
    for charge, *position in charges:
        distance_squared = sum(v*v for v in position)
        for alpha in range(3):
            for beta in range(3):
                delta = 1 if alpha == beta else 0
                tensor[alpha][beta] += charge*(3*position[alpha]*position[beta]-distance_squared*delta)
    assert isclose(tensor[2][2], 4*q*a*a)
    assert abs(sum(tensor[i][i] for i in range(3))) < 1e-25
    exact_potential = sum(K*charge/abs(observation-z) for charge, x, y, z in charges)
    approximate = K*tensor[2][2]/(2*observation**3)
    assert isclose(exact_potential, 1.8161616161616, rel_tol=1e-12)
    assert isclose(approximate, 1.798, rel_tol=1e-12)
    print(f"四极：点源精确电势={exact_potential:.6f} V；远场二次项={approximate:.6f} V")


if __name__ == '__main__':
    main()

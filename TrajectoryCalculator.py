import json
import math
import numpy
import scipy.integrate


def ballistics(t, x, cD_sphere, Area, Density, m, g):
    dfdt = [x[1], (1 / m) * (-1 * cD_sphere * Area * Density * (x[1] ** 2)), x[3], (1 / m) * (-1 * cD_sphere * Area * Density * (x[3] ** 2) * numpy.sign(x[3]) - (m * g))]
    return dfdt


def solve_initial_value_problem(initial_velocity, angle, barrel_offset, cD_sphere, area, density_of_air, m, g, tspan, timestep):
    x0 = 0
    x1 = initial_velocity * math.cos(math.radians(angle))
    y0 = barrel_offset
    y1 = initial_velocity * math.sin(math.radians(angle))
    p0 = [x0, x1, y0, y1]
    return scipy.integrate.solve_ivp(ballistics, tspan, p0, t_eval=timestep, args=(cD_sphere, area, density_of_air, m, g))


def solve_angle(initial_velocity, angle, barrel_offset, cD_sphere, area, density_of_air, m, g, tspan, timestep):
    results = solve_initial_value_problem(initial_velocity, angle, barrel_offset, cD_sphere, area, density_of_air, m, g, tspan, timestep)
    p = results.y
    target_val = 0
    while p[2][target_val] > 0:
        target_val = target_val + 1
    return p, target_val


def main():
    steps = 200000
    initial_velocity = 150  # m/s
    bb_diameter = 6e-3  # m
    density_of_air = 1.092  # kg/m^3
    cD_sphere = 0.5
    area = math.pi * 0.25 * (bb_diameter ** 2)  # m^2
    m = 0.2e-3  # kg
    gun_height = 1  # m
    g = 9.81  # m/s
    barrel_offset = 0.03 + gun_height
    tmax = 1000
    angletable = numpy.linspace(-45, 45, 10)
    tspan = [0, tmax]
    timestep = numpy.linspace(0, tmax, steps)
    firing_table = {}
    for angle in angletable:
        p, target_val = solve_angle(initial_velocity, angle, barrel_offset, cD_sphere, area, density_of_air, m, g, tspan, timestep)
        polynomial = numpy.polynomial.polynomial.Polynomial.fit(p[0][0:(target_val + 1)], p[2][0:(target_val + 1)], 5)
        firing_table[angle] = {}
        for coefficient in range(len(polynomial.convert().coef)):
            firing_table[angle][coefficient] = '{:.{prec}f}'.format(polynomial.convert().coef[coefficient], prec=2)
    with open('test.json', 'w') as file:
        json.dump(firing_table, file)


main()

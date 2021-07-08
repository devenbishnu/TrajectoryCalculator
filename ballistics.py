import numpy


def ballistics(t, x, cD_sphere, Area, Density, m, g):
    dfdt = [x[2], (1 / m) * (-1 * cD_sphere * Area * Density * (x[2] ** 2)), x(4), (1 / m) * (-1 * cD_sphere * Area *
            Density * (x[4] ** 2) * numpy.sign([4])) - (m * g)]
    return dfdt

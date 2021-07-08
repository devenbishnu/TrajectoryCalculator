import numpy


def ballistics(t, x, cD_sphere, Area, Density, m, g):
    dfdt = [x[1], (1 / m) * (-1 * cD_sphere * Area * Density * (x[1] ** 2)), x[3], (1 / m) * (-1 * cD_sphere * Area *
            Density * (x[3] ** 2) * numpy.sign(x[3]) - (m * g))]
    return dfdt

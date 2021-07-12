import math
import numpy
import scipy.integrate
import matplotlib.pyplot
import ballistics

steps = 1000000

# Reynolds Calcs
initial_velocity = 150  # m/s
Kinematic_viscosity = 1.516e-5  # m^2/s
bb_diameter = 6e-3  # m
density_of_air = 1.092  # kg/m^3
accuracy_angle = 0.1
angle = 0  # degrees
RE = (initial_velocity * bb_diameter) / Kinematic_viscosity

# Coefficient of Drag Calculation
cD_sphere = 0.5
area = math.pi * 0.25 * (bb_diameter ** 2)  # m^2

# Forces and Trajectory Parameters
m = 0.2e-3  # kg
gun_height = 1  # m
g = 9.81  # m/s
distance_measured = 20
angle_measured = 5
deltay = distance_measured * math.sin(math.radians(angle_measured))  # m
deltax = distance_measured * math.cos(math.radians(angle_measured))  # m
barrel_offset = 0.03 + gun_height

# time_in_air = sqrt(2 * gun_height / g)
tmax = 1000
angletable = numpy.linspace(-45, 45, 451)
number_of_angles = len(angletable)

# Initial Conditions (Solving for one angle)
x0 = 0
x1 = initial_velocity * math.cos(math.radians(angle))
y0 = barrel_offset
y1 = initial_velocity * math.sin(math.radians(angle))

p0 = [x0, x1, y0, y1]

tspan = [0, tmax]

timestep = numpy.linspace(0, tmax, steps)

results = scipy.integrate.solve_ivp(ballistics.ballistics, tspan, p0, t_eval=timestep, args=(cD_sphere, area,
                                    density_of_air, m, g))
t = results.t
p = results.y

target_val = 2
while p[2][target_val] > 0:
    target_val = target_val + 1
targetrange = p[0][target_val]
velocity = []
KE = []
PercentageKE = []
for i in range(len(p[0])):
    velocity.append(math.sqrt((p[1][i] ** 2) + p[3][i] ** 2))
    KE.append(0.5 * m * (velocity[i] ** 2))
    PercentageKE.append((KE[0] - KE[i]) / KE[0])
polynomial = numpy.polynomial.polynomial.Polynomial.fit(p[0][0:(target_val + 1)], p[2][0:(target_val + 1)], 5)
pathpolygraph = numpy.polynomial.polynomial.polyval(p[0][0:(target_val + 1)], polynomial.convert().coef)

matplotlib.pyplot.figure(figsize=(9, 9))
matplotlib.pyplot.subplot(311)
matplotlib.pyplot.plot(p[0][0:(target_val + 1)], p[2][0:(target_val + 1)], 'ro')
matplotlib.pyplot.plot(p[0][0:(target_val + 1)], p[2][0:(target_val + 1)])
matplotlib.pyplot.show()

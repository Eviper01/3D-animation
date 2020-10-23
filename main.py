import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
#Parameters


World_Size = 100
N_Particles = 10
Steps = 1000
#Classes

class Particle():

    def __init__(self, x=np.zeros(3), v=np.zeros(3), mass=1, size=1):
        self.x = x
        self.v = v
        self.mass = mass
        self.size = 1


#Data

Particles = []
Simulation_Data = []

#helpers

def random_x():
    return np.random.random(3)*World_Size

def random_v(magnitude=1):
    vec = np.random.random(3)
    return (magnitude/(np.sqrt(np.dot(vec,vec))))*vec

def save_state():
    xvalues = []
    yvalues = []
    zvalues = []
    for particle in Particles:
        xvalues.append(particle.x[0])
        yvalues.append(particle.x[1])
        zvalues.append(particle.x[2])
    Simulation_Data.append([xvalues,yvalues,zvalues])

def animate(State):
    map._offsets3d = ([State[0], State[1], State[2]])

def move(particle):
    next_x = particle.x + particle.v
    if (next_x)[0] < 0:
        particle.v[0] = -particle.v[0]
    if (next_x)[1] < 0:
        particle.v[1] = -particle.v[1]
    if (next_x)[0] > World_Size:
        particle.v[0] = -particle.v[0]
    if (next_x)[1] > World_Size:
        particle.v[1] = -particle.v[1]
    if (next_x)[2] < 0:
        particle.v[2] = -particle.v[2]
    if (next_x)[2] > World_Size:
        particle.v[2] = -particle.v[2]
    else:
        particle.x = next_x
#run loop

for i in range(N_Particles):
    Particles.append(Particle(x=random_x(),v=random_v()))
save_state()

for i in range(Steps):
    for particle in Particles:
        move(particle)
    save_state()

fig = plt.figure()
ax = p3.Axes3D(fig)
ax.set_xlim3d([0, World_Size])
ax.set_xlabel('X')

ax.set_ylim3d([0, World_Size])
ax.set_ylabel('Y')

ax.set_zlim3d([0, World_Size])
ax.set_zlabel('Z')
ax.axis([0,World_Size,0,World_Size])
map = ax.scatter(Simulation_Data[0][0], Simulation_Data[0][1], Simulation_Data[0][2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ani = animation.FuncAnimation(fig, animate, frames=Simulation_Data, interval=30, repeat=True)

plt.show()

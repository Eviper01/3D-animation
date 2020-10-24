import numpy as np
import time
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from random import random as random
import pandas as pd
import sys
#parameters
try:
    Pop = [P_Pop,R_Pop,S_Pop] = [int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])]
    Caps = [P_Cap,R_Cap,S_Cap] = [int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])]
    WorldSize = int(sys.argv[7])
    STEPS = int(sys.argv[8])
except Exception as e:
    print("invalid parameters")
    exit()
#commadline agruments






#object constructors
class Paper():
    def __init__(self, type = 0, position = (0,0), velocity = (0,0), size = 0.1, colour = (0, 1, 0, 1)):
        self.type = type
        self.position = position
        self.velocity = 3*velocity
        self.size = size
        self.colour = colour #default green
class Scissor():
    def __init__(self, type = 1, position = (0,0), velocity = (0,0), size = 1, colour = (1, 0, 0, 1)):
        self.type = type
        self.position = position
        self.velocity = velocity
        self.size = size
        self.colour = colour #default red
class Rock():
    def __init__(self, type = 2, position = (0,0), velocity = (0,0), size = 3, colour = (0, 0, 1, 1)):
        self.type = type
        self.position = position
        self.velocity = 0.5*velocity
        self.size = size
        self.colour = colour #default blue


#data
Lifeform_Types = [Paper,Scissor,Rock]
Lifeforms = [Paper_List,Scissors_List,Rock_List] = [[],[],[]]
Simulation_Data = []


#helpers
def random_velocity():
    v = np.random.random(2)
    return v/np.sqrt(np.dot(v,v))

def random_position():
    return WorldSize*np.random.random(2)


def babyStepChange(lifeform):
        next_position = lifeform.position + lifeform.velocity
        if (next_position)[0] < 0:
            lifeform.velocity[0] = -lifeform.velocity[0]
        if (next_position)[1] < 0:
            lifeform.velocity[1] = -lifeform.velocity[1]
        if (next_position)[0] > WorldSize:
            lifeform.velocity[0] = -lifeform.velocity[0]
        if (next_position)[1] > WorldSize:
            lifeform.velocity[1] = -lifeform.velocity[1]

        else:
            lifeform.position = next_position

def stepChange(lifeform):
    next_position = lifeform.position + lifeform.velocity
    for types in Lifeforms:
        for thing in iter(types):
            if np.sqrt(np.dot(next_position-thing.position,next_position-thing.position))<(lifeform.size+thing.size) and thing!=lifeform:
                if thing.type == lifeform.type:
                    if (random()>len(Lifeforms[(thing.type)])/Caps[(thing.type)]):
                    # if (random()<1/(1+np.exp(-(len(Lifeforms[(thing.type-1)%3])/Caps[(thing.type-1)%3]-len(Lifeforms[(thing.type+1)%3])/Caps[(thing.type+1)%3]-len(Lifeforms[(thing.type)%3])/Caps[(thing.type)%3])))):
                        baby = Lifeform_Types[lifeform.type](position=lifeform.position,velocity=random_velocity())
                        for i in range(30):
                            babyStepChange(baby)
                        Lifeforms[lifeform.type].append(baby)
                        print("spawning",lifeform.position)
                try:
                    if thing.type == 0 and lifeform.type == 1:
                        Lifeforms[0].remove(thing)
                    if thing.type == 1 and lifeform.type == 2:
                        Lifeforms[1].remove(thing)
                    if thing.type == 2 and lifeform.type == 0:
                        Lifeforms[2].remove(thing)
                    if lifeform.type == 0 and thing.type == 1:
                        Lifeforms[0].remove(lifeform)
                    if lifeform.type == 1 and thing.type == 2:
                        Lifeforms[1].remove(lifeform)
                    if lifeform.type == 2 and thing.type == 0:
                        Lifeforms[2].remove(lifeform)
                except ValueError:
                    pass
    if (next_position)[0] < 0:
        lifeform.velocity[0] = -lifeform.velocity[0]
    if (next_position)[1] < 0:
        lifeform.velocity[1] = -lifeform.velocity[1]
    if (next_position)[0] > WorldSize:
        lifeform.velocity[0] = -lifeform.velocity[0]
    if (next_position)[1] > WorldSize:
        lifeform.velocity[1] = -lifeform.velocity[1]

    else:
        lifeform.position = next_position

def animate(State):
    map.set_offsets(np.transpose([State[0], State[1]]))
    map.set_color(State[2])

def Save_State():
    xvalues = []
    yvalues = []
    colours = []
    for types in Lifeforms:
        for thing in types:
            xvalues.append(thing.position[0])
            yvalues.append(thing.position[1])
            colours.append(thing.colour)
    State = [xvalues,yvalues,colours]
    return State

#main loop
for i in range(P_Pop):
    Lifeforms[0].append(Paper(position = random_position(), velocity = random_velocity()))
for i in range(S_Pop):
    Lifeforms[1].append(Scissor(position = random_position(), velocity = random_velocity()))
for i in range(R_Pop):
    Lifeforms[2].append(Rock(position = random_position(), velocity = random_velocity()))

Simulation_Data.append(Save_State())
for step in range(STEPS):
    print(step)
    for types in Lifeforms:
        for thing in iter(types):
            stepChange(thing)
    Simulation_Data.append(Save_State())


#animation methods

fig,ax = plt.subplots()
plt.axis([0,WorldSize,0,WorldSize])
map = plt.scatter(Simulation_Data[0][0],Simulation_Data[0][1],c=Simulation_Data[0][2])
ani = animation.FuncAnimation(fig, animate, frames=Simulation_Data, interval=30, repeat=True)
df = pd.DataFrame(Simulation_Data)
df.to_csv("output.csv",index=False,header=False)
plt.show()

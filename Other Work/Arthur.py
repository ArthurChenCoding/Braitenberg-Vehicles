import tkinter as tk
import math as m
import numpy as np
from time import sleep


def create_circle(x, y, r, canvas):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill='#000000')


def create_Robot(w1x, w1y, s2x, s2y, canvas):
    x0 = w1x
    y0 = w1y
    x1 = s2x
    y1 = s2y
    cv = canvas.create_rectangle(x0, y0, x1, y1, outline='#000000')
    # cv.rotate(45)
    # cv += canvas.create_rectangle(x0, y0, x0-10, y0-15, fill='#000000')
    # cv += canvas.create_rectangle(x0+40, y0, x0 + 40 + 10, y0 - 15, fill='#000000')
    # cv += canvas.create_rectangle(x1, y1, x1-10, y1-7.5, fill='yellow')
    # cv += canvas.create_rectangle(x1-40, y1, x1 - 40 + 10, y1-7.5, fill='yellow')
    return cv


def rotatePoint(origin, endpoint, angle):
    tempPoint = (endpoint[0] - origin[0], endpoint[1] - origin[1])
    rad = angle * m.pi / 180
    xPrime = m.cos(rad) * tempPoint[0] - m.sin(rad) * tempPoint[1]
    yPrime = m.sin(rad) * tempPoint[0] + m.cos(rad) * tempPoint[1]

    xPrime += origin[0]
    yPrime += origin[1]

    return xPrime, yPrime


#
# class sensor:
#
#     def __init__(self, points):
#         self.sensorPoints = points
#
#

class light:

    def __init__(self, x, y, canv):
        self.xpos = x
        self.ypos = y
        self.radius = 10

        self.circle = create_circle(self.xpos, self.ypos, self.radius, canv)


class robot:

    def __init__(self, cx, cy, kMatrix, canv):
        self.width = 20
        self.height = 60
        # self.robotCenter = [cx, cy]
        # self.robotPerimeter = [cx - 20, cy, cx + 20, cy, cx - 20, cy - 60, cx + 20, cy - 60]
        self.w1Position = [cx - 20, cy]
        self.w2Position = [cx + 20, cy]
        self.sensor1Position = [cx - 20, cy - 60]
        self.sensor2Position = [cx + 20, cy - 60]
        self.w1velocity = 0
        self.w2velocity = 0
        # self.theta = 90
        self.k = kMatrix
        self.drawRobot = create_Robot(cx - 20, cy, cx + 20, cy - 60, canv)

    def calcWheelSpeeds(self, lightList):
        # sum up intensities of all light sources
        # return wheel speeds, w1 and w2
        s1 = 0
        s2 = 0
        for light in lightList:
            # Calculate distance between each light source and both sensors
            # sensor1Position and sensor2Position objects are not yet defined
            s1Distance = m.dist([light.xpos, light.ypos], self.sensor1Position)
            s2Distance = m.dist([light.xpos, light.ypos], self.sensor2Position)
            s1 = s1 + (100 / s1Distance)
            s2 = s2 + (100 / s2Distance)
        # w1 = self.k[0,0] * lightList[0] + self.k[0,1]
        if s1 > 100:
            s1 = 100
        if s2 > 100:
            s2 = 100
        print("received total intensity of the sensors")
        print(s1, s2)
        self.w1velocity = int(self.k[0]) * s1 + int(self.k[1]) * s2
        self.w2velocity = int(self.k[2]) * s1 + int(self.k[3]) * s2
        print("w1v, w2v")
        print(self.w1velocity, self.w2velocity)

    def calcRectanglePoints(self):
        # calculates the new position of the robots rectangle frame
        angle = 90
        angle2 = 90
        diff = m.dist([self.sensor1Position[0], 0], [self.sensor2Position[0], 0]) / m.dist([self.sensor1Position[0],
                                                                                            self.sensor1Position[1]],
                                                                                           [self.sensor2Position[0],
                                                                                            self.sensor2Position[1]])
        print("var diff in radian")
        print(diff)
        if (self.sensor1Position[1] >= self.sensor2Position[1]):  # left wheel is higher on y axis
            angle = 180 - 90 - (m.acos(diff) * 180 / m.pi)
        else:  # right wheel is higher on y axis
            angle = (m.acos(diff) * 180 / m.pi) + 90
        print("angle between the orientation of the car and x axis")
        print(angle)

        self.w1Position[0] = self.w1Position[0] - m.cos(angle) * self.w1velocity
        self.w1Position[1] = self.w1Position[1] - m.sin(angle) * self.w1velocity

        self.w2Position[0] = self.w2Position[0] - m.cos(angle) * self.w2velocity
        self.w2Position[1] = self.w2Position[1] - m.sin(angle) * self.w2velocity

        if self.sensor1Position[1] >= self.sensor2Position[1]:
            angle2 = 180 - 90 - diff #(m.acos(diff) * 180 / m.pi)
        else:
            angle2 = 90 + diff # (m.acos(diff) * 180 / m.pi) + 90

        # self.theta = angle2
        self.sensor2Position[0] = self.sensor2Position[0] - 60 * m.cos(angle2)
        self.sensor2Position[1] = self.sensor2Position[1] - 60 * m.sin(angle2)

        self.sensor1Position[0] = self.sensor1Position[0] - 60 * m.cos(angle2)
        self.sensor1Position[1] = self.sensor1Position[1] - 60 * m.sin(angle2)

        # self.robotPerimeter[6] = self.robotPerimeter[2] - m.cos(angle) * 60
        # self.robotPerimeter[7] = self.robotPerimeter[3] - m.sin(angle) * 60
        #
        # self.robotPerimeter[4] = self.robotPerimeter[0] - m.cos(angle) * 60
        # self.robotPerimeter[5] = self.robotPerimeter[1] - m.sin(angle) * 60
        #
        # self.sensor1Position = [self.robotPerimeter[4], self.robotPerimeter[5]]
        # self.sensor2Position = [self.robotPerimeter[6], self.robotPerimeter[7]]

        # print(self.sensor1Position[0], self.sensor1Position[1])
        return None

    def deleteRobotMove(self, canv):
        canv.delete(self.drawRobot)

    def drawRobotMove(self, canv):
        print("calling draw bot move")
        print("w1 and s2 coors")
        print(self.w1Position[0], self.w1Position[1])
        print(self.sensor2Position[0], self.sensor2Position[1])
        self.drawRobot = canv.create_rectangle(self.w1Position[0], self.w1Position[1],
                                               self.sensor2Position[0], self.sensor2Position[1], outline='#000000')

    def move(self, light_list, canv):
        self.deleteRobotMove(canv)
        self.calcWheelSpeeds(light_list)
        self.calcRectanglePoints()
        print("updated w1 and s2 coors")
        print(self.w1Position[0], self.w1Position[1])
        print(self.sensor2Position[0], self.sensor2Position[1])
        self.drawRobotMove(canv)


class environment:
    def __init__(self, canv):
        self.robotList = []
        self.lightList = []
        self.canv = canv
        self.start = False

    # creates a new robot and adds it to the list of robots in our system
    # this function will be called after submitting a form inside the gui to create a robot
    def addRobot(self, cx, cy, kMatrix):
        print("robot added at:", cx, cy, "with k matrix", kMatrix)
        newTim = robot(cx, cy, kMatrix, self.canv)
        self.robotList.append(newTim)

    # creates a new light source and adds it to the list of lights in our system
    # this function will be called after submitting a form inside the gui to create a light
    def addLight(self, x, y):
        print("light added at:", x, ", ", y)
        newLight = light(x, y, self.canv)
        self.lightList.append(newLight)

    # call this function every xxx period of time
    def update(self):
        for r in self.robotList:
            r.move(self.lightList, self.canv)

    def toggle(self):
        print("Toggled")
        self.start = not self.start

        while self.start:
            self.update()
            sleep(0.1)


# todo
# we need to create the canvas for our environment
window = tk.Tk()
leftBox = tk.Frame(window)
leftBox.pack(side=tk.LEFT)
rightBox = tk.Frame(window)
rightBox.pack(side=tk.RIGHT)

top = tk.Frame(window)
mid = tk.Frame(window)
bottom = tk.Frame(window)
paint = tk.Frame(window)
top.pack(in_=rightBox, side=tk.TOP)
mid.pack(in_=rightBox, side=tk.TOP)
bottom.pack(in_=rightBox, side=tk.TOP)
paint.pack(in_=rightBox, side=tk.TOP)

# -----------
canvas = tk.Canvas(window, width=800, height=600, bg="white")
canvas.pack(in_=leftBox, pady=20)

env = environment(canvas)

text_box1 = tk.Text(height=1, width=5)
text_box1.insert(tk.END, "0")
text_box1.pack(in_=top, side=tk.LEFT)
text_box2 = tk.Text(height=1, width=5)
text_box2.insert(tk.END, "0")
text_box2.pack(in_=top, side=tk.LEFT)
text_box3 = tk.Text(height=1, width=5)
button1 = tk.Button(
    window,
    text="Add Light",
    command=lambda: env.addLight(int(text_box1.get(1.0, 'end')), int(text_box2.get(1.0, 'end')))
)
button1.pack(in_=top, side=tk.LEFT)

text_box4 = tk.Text(height=1, width=5)
text_box4.insert(tk.END, "X")
text_box4.pack(in_=mid, side=tk.LEFT)
text_box5 = tk.Text(height=1, width=5)
text_box5.insert(tk.END, "Y")
text_box5.pack(in_=mid, side=tk.LEFT)
text_box6 = tk.Text(height=1, width=5)
text_box6.insert(tk.END, "K")
text_box6.pack(in_=mid, side=tk.LEFT)
button2 = tk.Button(
    window,
    text="Add Robot",
    command=lambda: env.addRobot(int(text_box4.get(1.0, 'end')), int(text_box5.get(1.0, 'end')),
                                 text_box6.get(1.0, 'end'))
)
button2.pack(in_=mid, side=tk.LEFT)

button4 = tk.Button(window, text="Play/Pause Simulation", command=env.toggle)
button4.pack(in_=bottom, side=tk.LEFT)

window.mainloop()

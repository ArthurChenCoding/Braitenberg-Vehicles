import tkinter as tk
import math as m
import numpy as np
from time import sleep
from PIL import Image, ImageTk

global tkimg

tkimg = 0


def rotatePoint(origin, endpoint, rad):
    tempPoint = (endpoint[0] - origin[0], endpoint[1] - origin[1])
    xPrime = m.cos(rad) * tempPoint[0] - m.sin(rad) * tempPoint[1]
    yPrime = m.sin(rad) * tempPoint[0] + m.cos(rad) * tempPoint[1]

    xPrime += origin[0]
    yPrime += origin[1]

    return [xPrime, yPrime]


def create_circle(x, y, r, canvas, color):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=color)


def create_Robot(x, y, canv, deg=0):

    global tkimg
    im = Image.open("../tim.png")
    im = im.rotate(180 - m.degrees(deg), expand=True)
    tkimg = ImageTk.PhotoImage(im)
    canvas_obj = canv.create_image(x, y, image=tkimg)
    return canvas_obj

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

        self.circle = create_circle(self.xpos, self.ypos, self.radius, canv, 'yellow')


class robot:

    def __init__(self, cx, cy, kMatrix, canv):
        self.width = 20
        self.height = 60
        self.robotCenter = [cx, cy]
        self.robotPerimeter = [cx - self.width, cy, cx + self.width, cy, cx - self.width, cy - self.height,
                               cx + self.width, cy - self.height]
        self.sensor1Position = [cx - self.width, cy - self.height]
        self.sensor2Position = [cx + self.width, cy - self.height]
        self.w1velocity = 0
        self.w2velocity = 0
        self.w1Position = [cx - self.width, cy]
        self.w2Position = [cx + self.width, cy]
        self.k = kMatrix
        self.drawRobot = create_Robot(cx, cy, canv)
        self.theta = 0

        self.c = canv

    def calcWheelSpeeds(self, lightList):
        # sum up intensities of all light sources
        # return wheel speeds, w1 and w2
        s1 = 0
        s2 = 0
        for light in lightList:
            # Calculate distance between each light source and both sensors
            # sensor1Position and sensor2Position objects are not yet defined
            # TODO change w1pos and w2pos to sensors
            s1Distance = m.dist([light.xpos, light.ypos], self.w1Position)
            s2Distance = m.dist([light.xpos, light.ypos], self.w2Position)
            s1 = s1 + (100 / s1Distance)
            s2 = s2 + (100 / s2Distance)
        # w1 = self.k[0,0] * lightList[0] + self.k[0,1]
        self.w1velocity = int(self.k[0]) * s1 + int(self.k[1]) * s2
        self.w2velocity = int(self.k[2]) * s1 + int(self.k[3]) * s2

        print("w1V: ", self.w1velocity)
        print("w2V: ", self.w2velocity)

    # calculates the new position of the robots rectangle frame
    def calcRectanglePoints(self, lightList):
        # Calculate distances between each wheel and ICC
        R = self.width * (self.w1velocity + self.w2velocity) / ((self.w2velocity - self.w1velocity))
        # Calculate theta to help find ICC
        difference = (self.w1Position[0] - self.w2Position[0]) / (2*self.width)
        print("difference: ", difference)
        theta = m.acos(difference)
        self.theta = theta

        # Find ICC
        # Calculate center point on diff drive axis
        center_x = (self.w1Position[0] + self.w2Position[0]) / 2
        center_y = (self.w1Position[1] + self.w2Position[1]) / 2
        center = [center_x, center_y]
        icc = []
        l = lightList[0]
        # turn right
        if self.w1velocity > self.w2velocity:

            if self.w1Position[1] == self.w2Position[1]:
                if m.dist([l.xpos, l.ypos], self.w1Position) > m.dist([l.xpos, l.ypos], self.w2Position):
                    icc = [center_x - R, center_y]
                else:
                    icc = [center_x + R, center_y]

            # tilted right
            elif self.w1Position[1] > self.w2Position[1]:
                icc_x = center_x + R * m.cos(theta)
                icc_y = center_y - R * m.sin(theta)
                icc = [icc_x, icc_y]

            # tilted left
            else:
                icc_x = center_x + R * m.cos(theta)
                icc_y = center_y + R * m.sin(theta)
                icc = [icc_x, icc_y]

            # Rotate clockwise (assuming w1 = left wheel and facing forwards)
            # icc_x = center_x + R * m.cos(theta)
            # icc_y = center_y - R * m.sin(theta)
            # Calculate angular velocity
            omega = (self.w2velocity - self.w1velocity) / (2*self.width)
            # Apply rotate function around ICC for each wheel
            # self.w1Position = rotatePoint(icc, self.w1Position, omega)
            # self.w2Position = rotatePoint(icc, self.w2Position, omega)
            center = rotatePoint(icc, center, omega)

            self.w1Position = [center[0] - self.width*m.cos(theta), center[1] + self.width*m.sin(theta)]
            self.w2Position = [center[0] + self.width * m.cos(theta), center[1] - self.width * m.sin(theta)]

        elif self.w1velocity < self.w2velocity:

            if self.w1Position[1] == self.w2Position[1]:
                if m.dist([l.xpos, l.ypos], self.w1Position) > m.dist([l.xpos, l.ypos], self.w2Position):
                    icc = [center_x - R, center_y]
                else:
                    icc = [center_x + R, center_y]

            elif self.w1Position[1] > self.w2Position[1]:
                icc_x = center_x - R * m.cos(theta)
                icc_y = center_y + R * m.sin(theta)
                icc = [icc_x, icc_y]

            else:
                icc_x = center_x - R * m.cos(theta)
                icc_y = center_y - R * m.sin(theta)
                icc = [icc_x, icc_y]

            # Rotate CCW
            # icc_x = center_x - R * m.cos(theta)
            # icc_y = center_y + R * m.sin(theta)
            # Calculate angular velocity
            omega = (self.w2velocity - self.w1velocity) / (2*self.width)
            # Apply rotate function around ICC for each wheel

            center = rotatePoint(icc, center, omega)
            self.w1Position = rotatePoint(icc, self.w1Position, omega)
            self.w2Position = rotatePoint(icc, self.w2Position, omega)

        else:
            print("w1 and w2 have same velocity")

        dot = create_circle(center[0], center[1], 2, self.c, '#000000')
        dot2 = create_circle(icc[0], icc[1], 2, self.c, 'green')
        #dot1 = create_circle(self.w1Position[0], self.w1Position[1], 2, self.c)
        #dot1 = create_circle(self.w2Position[0], self.w2Position[1], 2, self.c)

        print("icc: ", icc)
        print("w1P: ", self.w1Position)
        print("w2P: ", self.w2Position)
        # Apply rotate function around ICC for each wheel
        # w1_new = rotatePoint(icc)

        self.robotCenter = center
        return None

    def move(self, light_list):
        self.calcWheelSpeeds(light_list)
        self.calcRectanglePoints(light_list)

        # todo
        # still have to redraw robot position
        # as well as sensor positions

        self.c.delete(self.drawRobot)
        create_Robot(self.robotCenter[0], self.robotCenter[1], self.c, self.theta)


class environment:
    def __init__(self, canv, window):
        self.robotList = []
        self.lightList = []
        self.canv = canv
        self.start = False
        self.wind = window

    # creates a new robot and adds it to the list of robots in our system
    # this function will be called after submitting a form inside the gui to create a robot
    def addRobot(self, cx, cy, kMatrix):
        print("robot added at:", cx, cy, "with k matrix", kMatrix)
        newRobot = robot(cx, cy, kMatrix, self.canv)
        self.robotList.append(newRobot)

    # creates a new light source and adds it to the list of lights in our system
    # this function will be called after submitting a form inside the gui to create a light
    def addLight(self, x, y):
        print("light added at:", x, y)
        newLight = light(x, y, self.canv)
        self.lightList.append(newLight)

    # call this function every xxx period of time
    def update(self):
        for robit in self.robotList:
            robit.move(self.lightList)

    def toggle(self):
        print("Toggled")
        self.start = not self.start

        if self.start:
            self.canv.update_idletasks()
            self.update()
            sleep(0.01)

        self.wind.after(500, self.toggle)

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

env = environment(canvas, window)

text_box1 = tk.Text(height=1, width=5)
text_box1.insert(tk.END, "200")
text_box1.pack(in_=top, side=tk.LEFT)
text_box2 = tk.Text(height=1, width=5)
text_box2.insert(tk.END, "200")
text_box2.pack(in_=top, side=tk.LEFT)
text_box3 = tk.Text(height=1, width=5)
button1 = tk.Button(
    window,
    text="Add Light",
    command=lambda: env.addLight(int(text_box1.get(1.0, 'end')), int(text_box2.get(1.0, 'end')))
)
button1.pack(in_=top, side=tk.LEFT)

text_box4 = tk.Text(height=1, width=5)
text_box4.insert(tk.END, "400")
text_box4.pack(in_=mid, side=tk.LEFT)
text_box5 = tk.Text(height=1, width=5)
text_box5.insert(tk.END, "350")
text_box5.pack(in_=mid, side=tk.LEFT)
text_box6 = tk.Text(height=1, width=5)
text_box6.insert(tk.END, "0990")
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

env.update()

window.mainloop()
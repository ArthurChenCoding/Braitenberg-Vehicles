import tkinter as tk
import math as m
import numpy as np


def rotatePoint(origin, endpoint, rad):
    tempPoint = (endpoint[0] - origin[0], endpoint[1] - origin[1])
    xPrime = m.cos(rad) * tempPoint[0] - m.sin(rad) * tempPoint[1]
    yPrime = m.sin(rad) * tempPoint[0] + m.cos(rad) * tempPoint[1]

    xPrime += origin[0]
    yPrime += origin[1]

    return [xPrime, yPrime]


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
    cv += canvas.create_rectangle(x0, y0, x0 - 10, y0 - 15, fill='#000000')
    cv += canvas.create_rectangle(x0 + 40, y0, x0 + 40 + 10, y0 - 15, fill='#000000')
    cv += canvas.create_rectangle(x1, y1, x1 - 10, y1 - 7.5, fill='yellow')
    cv += canvas.create_rectangle(x1 - 40, y1, x1 - 40 + 10, y1 - 7.5, fill='yellow')
    return cv


#
# class sensor:
#
#     def __init__(self, points):
#         self.sensorPoints = points
#
#

class light:

    def __init__(self, x, y, intensity, canv):
        self.xpos = x
        self.ypos = y
        self.intensity = intensity
        self.radius = 10

        self.circle = create_circle(self.xpos, self.ypos, self.radius, canv)


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
        self.drawRobot = create_Robot(cx - self.width, cy, cx + self.width, cy - self.height, canv)

    def calcWheelSpeeds(self, lightList):
        # sum up intensities of all light sources
        # return wheel speeds, w1 and w2
        for light in lightList:
            # Calculate distance between each light source and both sensors
            # sensor1Position and sensor2Position objects are not yet defined
            s1Distance = m.dist([light.xpos, light.ypos], self.sensor1Position)
            s2Distance = m.dist([light.xpos, light.ypos], self.sensor2Position)
        # w1 = self.k[0,0] * lightList[0] + self.k[0,1]
        # return None
        # For testing, predefine w1 and w2. Normally this is found with sensor values.
        w1 = 1
        w2 = 1

    # calculates the new position of the robots rectangle frame
    def calcRectanglePoints(self):
        # Calculate distances between each wheel and ICC
        R = self.width * (self.w1velocity + self.w2velocity) / 2 * (self.w2velocity - self.w1velocity)
        r1 = R + self.width / 2
        r2 = R - self.width / 2
        # Calculate theta to help find ICC
        difference = (self.w1Position[0] - self.w2Position[0]) / self.width
        theta = m.acos(difference)

        # Find ICC
        # Calculate center point on diff drive axis
        center_x = (self.w1Position[0] + self.w2Position[0]) / 2
        center_y = (self.w1Position[1] + self.w2Position[1]) / 2
        center = [center_x, center_y]
        if self.w1velocity > self.w2velocity:
            # Rotate clockwise (assuming w1 = left wheel and facing forwards)
            icc_x = center_x + R * m.cos(theta)
            icc_y = center_y + R * m.sin(theta)
            icc = [icc_x, icc_y]
            # Calculate angular velocity
            omega = (self.w2velocity - self.w1velocity) / self.width
            # Apply rotate function around ICC for each wheel
            self.w1Position = rotatePoint(icc, self.w1Position, omega)
            self.w2Position = rotatePoint(icc, self.w2Position, omega)
        elif self.w1velocity < self.w2velocity:
            # Rotate CCW
            icc_x = center_x - R * m.cos(theta)
            icc_y = center_y - R * m.sin(theta)
            icc = [icc_x, icc_y]
            # Calculate angular velocity
            omega = (self.w2velocity - self.w1velocity) / self.width
            # Apply rotate function around ICC for each wheel
            self.w1Position = rotatePoint(icc, self.w1Position, omega)
            self.w2Position = rotatePoint(icc, self.w2Position, omega)
        else:
            print("w1 and w2 have same velocity")

        # Apply rotate function around ICC for each wheel
        w1_new = rotatePoint(icc)
        return None

    def move(self, lightList):
        self.w1velocity, self.w2velocity = self.calcWheelSpeeds(lightList)
        self.robotPos = self.calcRectanglePoints()

        # todo
        # still have to redraw robot position
        # as well as sensor positions


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
        newRobot = robot(cx, cy, kMatrix, self.canv)
        self.robotList.append(newRobot)

    # creates a new light source and adds it to the list of lights in our system
    # this function will be called after submitting a form inside the gui to create a light
    def addLight(self, x, y, intensity):
        print("light added at:", x, y, "with intensity", intensity)
        newLight = light(x, y, intensity, self.canv)
        self.lightList.append(newLight)

    # call this function every xxx period of time
    def update(self):
        while start:
            print("moving")
            for robit in self.robotList:
                robit.move(self.lightList)

    def toggle(self):
        print("Toggled")
        self.start = not self.start


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

tim = robot(500, 500, 1001, canvas)
tim2 = robot(200, 200, 1001, canvas)

text_box1 = tk.Text(height=1, width=5)
text_box1.insert(tk.END, "0")
text_box1.pack(in_=top, side=tk.LEFT)
text_box2 = tk.Text(height=1, width=5)
text_box2.insert(tk.END, "0")
text_box2.pack(in_=top, side=tk.LEFT)
text_box3 = tk.Text(height=1, width=5)
text_box3.insert(tk.END, "0")
text_box3.pack(in_=top, side=tk.LEFT)
button1 = tk.Button(
    window,
    text="Add Light",
    command=lambda: env.addLight(int(text_box1.get(1.0, 'end')), int(text_box2.get(1.0, 'end')),
                                 int(text_box3.get(1.0, 'end')))
)
button1.pack(in_=top, side=tk.LEFT)

text_box4 = tk.Text(height=1, width=5)
text_box4.insert(tk.END, "0")
text_box4.pack(in_=mid, side=tk.LEFT)
text_box5 = tk.Text(height=1, width=5)
text_box5.insert(tk.END, "0")
text_box5.pack(in_=mid, side=tk.LEFT)
text_box6 = tk.Text(height=1, width=5)
text_box6.insert(tk.END, "0")
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
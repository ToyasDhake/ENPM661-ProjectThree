from time import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from math import sin, cos, radians

multiplier = 5
height, width = 200 * multiplier, 300 * multiplier
count = 0

radius = int(input("Enter radius: "))
clearance = int(input("Enter Clearance: "))
clearance += radius
coordinates = []
env = Environment([0, 0], clearance)
startBool = True
goalBool = True


while startBool:

    startPos = input("Enter start position: ")


    if "," in startPos:
        startPos = startPos.replace(" ", "")
        startPos = startPos.split(",")
    else:
        startPos = startPos.split(" ")


    if env.possiblePostion([int(startPos[0]), int(startPos[1])]):
        coordinates.append([int(startPos[0]) * multiplier, (200 - int(startPos[1])) * multiplier, int(startPos[2])])
        count += 1
        startBool = False
    else:
        print("Invalid position.")

while goalBool:

    goalPos = input("Enter goal position: ")


    if "," in goalPos:
        goalPos = goalPos.replace(" ", "")
        goalPos = goalPos.split(",")
    else:
        goalPos = goalPos.split(" ")


    if env.possiblePostion([int(goalPos[0]), int(goalPos[1])]):
        coordinates.append([int(goalPos[0]) * multiplier, (200 - int(goalPos[1])) * multiplier, int(goalPos[2])])
        count += 1
        goalBool = False
    else:
        print("Invalid position.")

stepSize = int(input("Enter step size: "))



pygame.init()
display = pygame.display.set_mode((width, height))
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10 * multiplier)
ticks = 400
clock = pygame.time.Clock()

hexagon = [((25 * multiplier), height - (185 * multiplier)), ((75 * multiplier), height - (185 * multiplier)),
           ((100 * multiplier), height - (150 * multiplier)), ((75 * multiplier), height - (120 * multiplier)),
           ((50 * multiplier), height - (150 * multiplier)), ((20 * multiplier), height - (120 * multiplier))]
rectangle = [((95 * multiplier), height - (30 * multiplier)), ((30 * multiplier), height - (68 * multiplier)),
             ((35 * multiplier), height - (77 * multiplier)), ((100 * multiplier), height - (38 * multiplier))]
diamond = [((225 * multiplier), height - (10 * multiplier)), ((200 * multiplier), height - (25 * multiplier)),
           ((225 * multiplier), height - (40 * multiplier)), ((250 * multiplier), height - (25 * multiplier))]
ellipse = [(110 * multiplier), (height - (120 * multiplier)), (80 * multiplier), (40 * multiplier)]

def draw():
    global count
    pygame.draw.polygon(display, (138, 132, 226), hexagon)
    pygame.draw.polygon(display, (138, 132, 226), rectangle)
    pygame.draw.polygon(display, (138, 132, 226), diamond)
    pygame.draw.circle(display, (138, 132, 226), ((225 * multiplier), height - (150 * multiplier)), 25 * multiplier)
    pygame.draw.ellipse(display, (138, 132, 226), pygame.Rect(ellipse))

    if count > 0:
        env = Environment(coordinates[0], clearance)
        if env.possiblePostion([int(coordinates[0][0] / multiplier), int(200 - coordinates[0][1] / multiplier)]):
            if radius != 0:
                pygame.draw.circle(display, (0, 0, 255), (coordinates[0][0], coordinates[0][1]), radius * multiplier, 1)
            pygame.draw.rect(display, (0, 0, 255),
                             pygame.Rect(coordinates[0][0], coordinates[0][1], multiplier, multiplier))

            textsurface = myfont.render("Initial Postion", False, (255, 0, 0))
            if height - coordinates[0][1] > 40:
                display.blit(textsurface, (coordinates[0][0] - 10 * multiplier, coordinates[0][1] + multiplier))
            else:
                display.blit(textsurface, (coordinates[0][0] - 10 * multiplier, coordinates[0][1] + multiplier - 40))
        else:
            print("Invalid position")
            count = 0
            coordinates.pop(0)

    if count > 1:
        env = Environment(coordinates[1], clearance)
        if env.possiblePostion([int(coordinates[1][0] / multiplier), int(200 - coordinates[1][1] / multiplier)]):
            if radius != 0:
                pygame.draw.circle(display, (0, 0, 255), (coordinates[1][0], coordinates[1][1]), radius * multiplier, 1)
            pygame.draw.rect(display, (0, 0, 255),
                             pygame.Rect(coordinates[1][0], coordinates[1][1], multiplier, multiplier))

            textsurface = myfont.render("Goal Postion", False, (255, 0, 0))
            if height - coordinates[1][1] > 40:
                display.blit(textsurface, (coordinates[1][0] - 10 * multiplier, coordinates[1][1] + multiplier))
            else:
                display.blit(textsurface, (coordinates[1][0] - 10 * multiplier, coordinates[1][1] + multiplier - 40))
        else:
            print("Invalid position")
            count = 1
            coordinates.pop(1)
    pygame.display.flip()
    clock.tick(ticks)

def drawArrow(i, color, list, stroke):
    pygame.draw.line(display, color, [list[i].parent.env[0]*multiplier, height - list[i].parent.env[1]*multiplier], [list[i].env[0]*multiplier, height - list[i].env[1]*multiplier], stroke)
    x = (list[i].env[0] - 2 * cos(radians(list[i].env[2] - 45)))*multiplier
    y = (list[i].env[1] - 2 * sin(radians(list[i].env[2] - 45)))*multiplier
    pygame.draw.line(display, color, [x, height - y], [list[i].env[0]*multiplier, height - list[i].env[1]*multiplier], stroke)
    x = (list[i].env[0] - 2 * cos(radians(list[i].env[2] + 45)))*multiplier
    y = (list[i].env[1] - 2 * sin(radians(list[i].env[2] + 45)))*multiplier
    pygame.draw.line(display, color,  [x, height - y], [list[i].env[0]*multiplier, height - list[i].env[1]*multiplier], stroke)



draw()

pygame.time.wait(3000)
pygame.quit()
exit()



from math import sqrt, cos, sin, radians, atan2, floor


class Node:
    # Initialize
    def __init__(self, start, env, goal, stepSize, parent=None):
        self.env = env
        self.parent = parent
        self.goal = goal
        if parent is not None:
            self.g = parent.g + stepSize
        else:
            self.g = 0
        # Heuristic function
        self.weight = self.g + sqrt((env[0] - goal[0]) ** 2 + (env[1] - goal[1]) ** 2) + (
                    (env[2] - floor(atan2((goal[1] - start[1]), (goal[0] - start[0])))) / 30) * (stepSize / 5)

    # Solve for path from goal to start node
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    # Get possible actions
    def actions(self):
        if self.action is None:
            return self.env.possibleMoves()
        else:
            return self.env.possibleMoves(self.action)


class Environment:
    # Initialize
    def __init__(self, currentPosition, clearance):
        self.currentPosition = currentPosition
        self.clearance = clearance

    # Check if node is in rectangle using half planes
    def insideRectangle(self, position):
        temp = False
        if ((1112 / 13) - ((38 / 65) * (position[0] + self.clearance * 0.5))) <= (
                position[1] + self.clearance * 0.866) and (position[1] - self.clearance * 0.5) <= (
                ((9 / 5) * (position[0] + self.clearance * 0.866)) + 14) and (
                ((8 / 5) * (position[0] - self.clearance * 0.866)) - 122) <= (position[1] + self.clearance * 0.5) and (
                position[1] - self.clearance * 0.866) <= (
                98 - ((3 / 5) * (position[0] - self.clearance * 0.5))):
            temp = True
        if position[1] <= 30 - self.clearance or position[1] >= 77 + self.clearance or position[
            0] <= 30 - self.clearance or position[0] >= 100 + self.clearance:
            temp = False
        if (position[0] - 95) ** 2 + (position[1] - 30) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 30) ** 2 + (position[1] - 68) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 35) ** 2 + (position[1] - 77) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 100) ** 2 + (position[1] - 38) ** 2 <= (self.clearance) ** 2:
            temp = True
        return temp

    # Check if node is in cirlce
    def insideCircle(self, position):
        if (position[0] - 225) ** 2 + (position[1] - 150) ** 2 <= (25 + self.clearance) ** 2:
            return True
        else:
            return False

    # Check if node is in elipse
    def insideElipse(self, position):
        if ((position[0] - 150) ** 2) / (40 + self.clearance) ** 2 + ((position[1] - 100) ** 2) / (
                20 + self.clearance) ** 2 <= 1:
            return True
        else:
            return False

    # Check if node is in diamond using half planes
    def insideDiamond(self, position):
        temp = False
        if (145 - ((3 / 5) * (position[0] + self.clearance * 0.5))) <= (position[1] + self.clearance * 0.866) and (
                ((3 / 5) * (position[0] - self.clearance * 0.5)) - 125) <= (position[1] + self.clearance * 0.866) and (
                175 - ((3 / 5) * (position[0] - self.clearance * 0.5))) >= (position[1] - self.clearance * 0.866) and (
                ((3 / 5) * (position[0] + self.clearance * 0.5)) - 95) >= (position[1] - self.clearance * 0.866):
            temp = True
        if position[1] >= 40 + self.clearance or position[1] <= 10 - self.clearance / 2 or position[
            0] <= 200 - self.clearance / 2 or position[0] >= 250 + self.clearance / 2:
            temp = False
        if (position[0] - 225) ** 2 + (position[1] - 10) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 200) ** 2 + (position[1] - 25) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 225) ** 2 + (position[1] - 40) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 250) ** 2 + (position[1] - 25) ** 2 <= (self.clearance) ** 2:
            temp = True
        return temp

    # Check if node is in polygon using half planes
    def insidePoly(self, position):
        temp = False
        if (((position[0] - self.clearance * 0.7071) + 100) <= (position[1] + self.clearance * 0.7071) and (
                ((7 / 5) * position[0]) + 80) <= position[1] and 185 >= position[1] - self.clearance * 1
            and (13 * (position[0] + self.clearance * 0.997) - 140) >= (position[1] - self.clearance * 0.07672)) or (
                (((7 / 5) * position[0]) + 80) >= position[1]
                and (290 - ((7 / 5) * (position[0] - self.clearance * 0.8137))) >= (
                        position[1] - self.clearance * 0.5812) and (
                        (6 / 5) * (position[0] - self.clearance * 0.7682) + 30) <= (
                        position[1] + self.clearance * 0.64023)
                and (210 - (6 / 5) * (position[0] + self.clearance * 0.7682)) <= (
                        position[1] + self.clearance * 0.64023)):
            temp = True
        if (((7 / 5) * position[0]) + 80) >= position[1] and (
                210 - (6 / 5) * (position[0] + self.clearance * 0.7682)) >= (
                position[1] + self.clearance * 0.64023) and ((position[0] - self.clearance * 0.7071) + 100) <= (
                position[1] + self.clearance * 0.7071):
            temp = True
        if position[0] + 160 + self.clearance / 2 <= position[1]:
            temp = False
        if 228.2975 + self.clearance / 2 - 0.5773 * position[0] <= position[1]:
            temp = False
        if position[1] <= 120 - self.clearance / 2 and temp:
            temp = False
        if position[0] >= 100 + self.clearance and temp:
            temp = False
        if (position[0] - 20) ** 2 + (position[1] - 120) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 75) ** 2 + (position[1] - 120) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 100) ** 2 + (position[1] - 150) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 75) ** 2 + (position[1] - 185) ** 2 <= (self.clearance) ** 2:
            temp = True
        if (position[0] - 25) ** 2 + (position[1] - 185) ** 2 <= (self.clearance) ** 2:
            temp = True
        return temp

    # Check if position is inside map or inside an object
    def possiblePostion(self, position):
        possiblity = True
        if position[0] < self.clearance:
            possiblity = False
        if position[1] < self.clearance:
            possiblity = False
        if position[0] > 300 - self.clearance:
            possiblity = False
        if position[1] > 200 - self.clearance:
            possiblity = False
        if self.insideRectangle(position):
            possiblity = False
        if self.insideCircle(position):
            possiblity = False
        if self.insideElipse(position):
            possiblity = False
        if self.insideDiamond(position):
            possiblity = False
        if self.insidePoly(position):
            possiblity = False
        return possiblity

    # Check if each action is possible
    def possibleMoves(self, start, node, stepSize):
        actions = []
        temp = self.move(start, '1', stepSize, node)
        if temp is not None:
            actions.append(temp)
        temp = self.move(start, '2', stepSize, node)
        if temp is not None:
            actions.append(temp)
        temp = self.move(start, '3', stepSize, node)
        if temp is not None:
            actions.append(temp)
        temp = self.move(start, '4', stepSize, node)
        if temp is not None:
            actions.append(temp)
        temp = self.move(start, '5', stepSize, node)
        if temp is not None:
            actions.append(temp)
        return actions

    # Move robot position according to action
    def move(self, start, val, stepSize, node):
        temp = None
        if val == '1':
            angle = self.currentPosition[2] + 60
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(stepSize):
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        if val == '2':
            angle = self.currentPosition[2] + 30
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(stepSize):
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        if val == '3':
            angle = self.currentPosition[2]
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(stepSize):
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        if val == '4':
            angle = self.currentPosition[2] - 30
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(stepSize):
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        if val == '5':
            angle = self.currentPosition[2] - 60
            angle = self.angleCheck(angle)
            tempBoolean = True
            for i in range(stepSize):
                x = self.currentPosition[0] + i * cos(radians(angle))
                y = self.currentPosition[1] + i * sin(radians(angle))
                if not self.possiblePostion([x, y]):
                    tempBoolean = False
            if tempBoolean:
                x = self.currentPosition[0] + stepSize * cos(radians(angle))
                y = self.currentPosition[1] + stepSize * sin(radians(angle))
                temp = Node(start, [x, y, angle], node.goal, stepSize, node)
        return temp

    # Keep angle value from 0 to 360
    def angleCheck(self, angle):
        if angle >= 360:
            angle -= 360
        if angle < 0:
            angle = 360 + angle
        return angle

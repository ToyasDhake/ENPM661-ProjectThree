from copy import deepcopy
from math import sqrt


# This class will hold attributes of each position
class Node:
    # Initialize 
    def __init__(self, env, parent=None, action=None):
        self.env = env
        self.parent = parent
        self.action = action
        if action is not None:
            # add cost based on action taken
            self.weight = parent.weight + sqrt(len(action))
        else:
            self.weight = 0

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
    def possibleMoves(self, remove='A'):
        actions = []
        if self.possiblePostion([self.currentPosition[0], self.currentPosition[1] + 1]):
            actions.append('U')
        if self.possiblePostion([self.currentPosition[0], self.currentPosition[1] - 1]):
            actions.append('D')
        if self.possiblePostion([self.currentPosition[0] - 1, self.currentPosition[1]]):
            actions.append('L')
        if self.possiblePostion([self.currentPosition[0] + 1, self.currentPosition[1]]):
            actions.append('R')
        if self.possiblePostion([self.currentPosition[0] - 1, self.currentPosition[1] + 1]):
            actions.append('UL')
        if self.possiblePostion([self.currentPosition[0] + 1, self.currentPosition[1] + 1]):
            actions.append('UR')
        if self.possiblePostion([self.currentPosition[0] - 1, self.currentPosition[1] - 1]):
            actions.append('DL')
        if self.possiblePostion([self.currentPosition[0] + 1, self.currentPosition[1] - 1]):
            actions.append('DR')
        if remove == 'U' and 'D' in actions:
            actions.remove('D')
        if remove == 'D' and 'U' in actions:
            actions.remove('U')
        if remove == 'L' and 'R' in actions:
            actions.remove('R')
        if remove == 'R' and 'L' in actions:
            actions.remove('L')
        if remove == 'UL' and 'DR' in actions:
            actions.remove('DR')
        if remove == 'UR' and 'DL' in actions:
            actions.remove('DL')
        if remove == 'DL' and 'UR' in actions:
            actions.remove('UR')
        if remove == 'DR' and 'UL' in actions:
            actions.remove('UL')
        return actions

    # Move robot position according to action
    def move(self, val):
        temp = deepcopy(self)
        if val == 'U':
            temp.currentPosition[1] += 1
        if val == 'D':
            temp.currentPosition[1] -= 1
        if val == 'R':
            temp.currentPosition[0] += 1
        if val == 'L':
            temp.currentPosition[0] -= 1
        if val == 'UL':
            temp.currentPosition[0] -= 1
            temp.currentPosition[1] += 1
        if val == 'UR':
            temp.currentPosition[0] += 1
            temp.currentPosition[1] += 1
        if val == 'DL':
            temp.currentPosition[0] -= 1
            temp.currentPosition[1] -= 1
        if val == 'DR':
            temp.currentPosition[0] += 1
            temp.currentPosition[1] -= 1
        return temp

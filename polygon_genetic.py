"Getting best fit for formal plygon"
from random import randint
from math import sqrt
from operator import add
from graphics import Point, Polygon, GraphWin, Line


def individual(count, min_val, max_val):
    points = []
    for i in range(count):
        x = randint(min_val, max_val)
        y = randint(min_val, max_val)
        points.append(Point(x, y))
    return Polygon(points)


def population(count, indie_count, min_val, max_val):
    return [individual(indie_count, min_val, max_val) for x in range(count)]


def fitness(polygon: Polygon):
    def next_index(i, items):
        return 0 if i + 1 == len(items) else i + 1

    def get_line_length(line):
        return sqrt(add(pow(line.p2.x - line.p1.x, 2), pow(line.p2.y - line.p1.y, 2)))

    for line in [Line(point, polygon.points[next_index(i, polygon.points)]) for i, point in enumerate(polygon.points)]:
        length = get_line_length(line)
        print(length)

for i, indie in enumerate(population(5, 5, 10, 90)):
    fitness(indie)
    win = GraphWin("Polygon " + str(i), 100, 100)
    indie.draw(win)
    win.getMouse()
    win.close()

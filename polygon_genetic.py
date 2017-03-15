"Getting best fit for formal plygon"
import time
from random import randint, random
from math import sqrt, acos, degrees
from operator import add, itemgetter
from statistics import pstdev, mean
from functools import reduce
from graphics import Point, Polygon, GraphWin, Line, Text


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

    def next_item(i, items):
        return items[next_index(i, items)]

    def get_lines(points):
        return [Line(point, next_item(i, polygon.points)) for i, point in enumerate(polygon.points)]

    lines = get_lines(polygon.points)

    def get_line_length(line):
        return sqrt(add(pow(line.p2.x - line.p1.x, 2), pow(line.p2.y - line.p1.y, 2)))

    length_sd = pstdev([get_line_length(line) for line in lines])

    def get_angle_between_lines(line1: Line, line2: Line):
        len1 = get_line_length(line1)
        len2 = get_line_length(line2)
        if len1 == 0 or len2 == 0:
            return 0
        len3 = get_line_length(Line(line2.p2, line1.p1))
        angle = degrees(
            acos((pow(len1, 2) + pow(len2, 2) - pow(len3, 2)) / (2 * len1 * len2)))
        return angle

    perfect_angle = ((len(lines) - 2) * 180) / len(lines)
    angles_sd = pstdev([get_angle_between_lines(
        line, next_item(i, lines)) for i, line in enumerate(lines)], perfect_angle)

    def get_line_equation(line: Line):
        def func(x):
            gradient = (line.p2.y - line.p1.y) / (line.p2.x - line.p1.x)
            constant = line.p1.y - (gradient * line.p1.x)
            return (gradient * x) + constant

        return func

    return mean([length_sd, angles_sd])


def evolve(pop, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [(fitness(x), x) for x in pop]
    graded = [x[1] for x in sorted(graded, key=itemgetter(0))]
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for indie in graded[retain_length:]:
        if random_select > random():
            parents.append(indie)

    # mutate some individuals
    for indie in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(indie.points) - 1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            points_x = [p.x for p in indie.points]
            points_y = [p.y for p in indie.points]
            indie.points[pos_to_mutate] = Point(
                randint(min(points_x), max(points_x)), randint(min(points_y), max(points_y)))

    # crossover parents to create children
    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length - 1)
        female = randint(0, parents_length - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = int(len(male.points) / 2)
            child = Polygon(male.points[:half] + female.points[half:])
            children.append(child)

    parents.extend(children)
    return parents


def view_pop(pop, hold=False):
    win = GraphWin("Polygons", 200, 200)
    for i, indie in enumerate(pop):
        text = Text(Point(180, 180), fitness(indie))
        indie.draw(win)
        text.draw(win)
        time.sleep(0.5)
        indie.undraw()
        text.undraw()
    if hold:
        win.getMouse()
    win.close()


def grade(pop):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x) for x in pop), 0)
    return summed / (len(pop) * 1.0)


def test():
    pop = population(50, 5, 10, 170)
    print("Original Population:")
    [print(indie) for indie in pop]
    origranl_grade = grade(pop)
    print("grade: " + str(origranl_grade))
    view_pop(pop)
    population_history = [pop, ]
    fitness_history = [origranl_grade, ]

    for i in range(50):
        pop = evolve(pop)
        print("-[start]--Generation[" + str(i) + "]:")
        [print(indie) for indie in pop]
        generation_grade = grade(pop)
        print("grade: " + str(generation_grade))
        print("--[end]---Generation[" + str(i) + "]:")
        view_pop(pop)
        population_history.append(pop)
        fitness_history.append(generation_grade)

    for i in fitness_history:
        print(i)

    last_generation = population_history[len(population_history) - 1]
    fittist = last_generation[0]
    view_pop([fittist], True)

test()
#view_pop([Polygon(Point(35.0, 24.0), Point(103.0, 46.0), Point(84.0, 123.0), Point(16.0, 107.0))],True)

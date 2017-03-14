'implementing genetic algorithm'
from random import randint, random
from operator import add
from functools import reduce


def individual(length, min_value, max_value):
    'Create a member of the population'
    return [randint(min_value, max_value) for x in range(length)]


def population(count, length, min_value, max_value):
    """
    Create a number of individuals (i.e. a population).

    count: the number of individuals in the population
    length: the number of values per individual
    min: the min possible value in an individual's list of values
    max: the max possible value in an individual's list of values
    """
    return [individual(length, min_value, max_value) for x in range(count)]


def fitness(indie, target):
    """
    Determine the fitness of an individual. Lower is better.

    individual: the individual to evaluate
    target: the sum of numbers that individuals are aiming for
    """
    summed = reduce(add, indie, 0)
    return abs(target - summed)


def grade(pop, target):
    'Find average fitness for a population.'
    summed = reduce(add, (fitness(x, target) for x in pop), 0)
    return summed / (len(pop) * 1.0)


def evolve(pop, target, retain=0.2, random_select=0.05, mutate=0.01):
    'Evolve population'
    graded = [(fitness(x, target), x) for x in pop]
    graded = [x[1] for x in sorted(graded)]
    retain_length = int(len(graded) * retain)
    parents = graded[:retain_length]

    # randomly add other individuals to promote genetic diversity
    for indie in graded[retain_length:]:
        if random_select > random():
            parents.append(indie)

    # mutate some individuals
    for indie in parents:
        if mutate > random():
            pos_to_mutate = randint(0, len(indie) - 1)
            # this mutation is not ideal, because it
            # restricts the range of possible values,
            # but the function is unaware of the min/max
            # values used to create the individuals,
            indie[pos_to_mutate] = randint(
                min(indie), max(indie))

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
            half = int(len(male) / 2)
            child = male[:half] + female[half:]
            children.append(child)

    parents.extend(children)
    return parents


def test():
    'testing genetic algorithm'
    target = 371
    p_count = 100
    i_length = 5
    i_min = 0
    i_max = 100

    pop = population(p_count, i_length, i_min, i_max)
    
    fitness_history = [grade(pop, target), ]
    for i in range(100):
        pop = evolve(pop, target)
        fitness_history.append(grade(pop, target))

    for i in fitness_history:
        print(i)

test()

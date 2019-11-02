from itertools import chain, combinations


def all_subsets(population):
    return chain(*map(lambda x: combinations(population, x), range(0, len(population) + 1)))


def remove_subsets(sets):
    removed = []
    for s in sets:
        subset = False
        for o in sets:
            if s.issubset(o) and s is not o:
                subset = True
        if not subset:
            removed.append(s)
    return removed


def sets_to_sorted_lists(sets):
    return [sorted(list(s)) for s in sets]


def remove_intersecting_sets(sets):
    removed = []
    for s in sets:
        intersect = False
        for r in removed:
            if s.intersection(r):
                intersect = True
                break
        if not intersect:
            removed .append(s)
    return removed



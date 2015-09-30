import itertools
import functools
import random


class Domain(object):
    ''' Cartesian domain. '''
    def __init__(self, ranges, rand=None):
        if rand is None:
            rand = random.Random()

        volume = 1
        for r in ranges:
            volume = volume * (r[1] - r[0])
        self._volume = volume

        _dists = []
        for r in ranges:
            dist = functools.partial(rand.uniform, r[0], r[1])
            _dists.append(dist)
        self._dists = _dists

    def rand_point(self):
        return [d() for d in self._dists]

    @property
    def volume(self):
        return self._volume

def simulation(domain, func, n):
    ''' Runs Monte-Carlo simulation on specified *domain*. '''
    points = (domain.rand_point() for i in xrange(n))
    values = (func(*p) for p in points)
    total = sum(values)
    ratio = total / float(n)
    return ratio * domain.volume

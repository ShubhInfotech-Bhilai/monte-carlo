'''Simple Monte-Carlo module.

Usage:
    >>> d = Domain([(0, 1), (0, 1)])
    >>> f = lambda x, y: y < x*x
    >>> area = simulation(d, f, n=10**5)
    >>> round(area, 2)
    0.33
'''

import functools
import random


class Domain(object):
    ''' Cartesian domain. '''
    def __init__(self, ranges, rand=None):
        if rand is None:
            rand = random.Random()

        self._volume = 1
        for low, high in ranges:
            self._volume *= (high - low)

        self._samplers = []
        for low, high in ranges:
            sampler = functools.partial(rand.uniform, low, high)
            self._samplers.append(sampler)

    def sample(self):
        ''' Uniformly sample domain. '''
        return [s() for s in self._samplers]

    @property
    def volume(self):
        ''' Return pre-computed domain's volume. '''
        return self._volume


def simulation(domain, func, iters):
    ''' Runs Monte-Carlo simulation on specified *domain*. '''
    points = (domain.sample() for _ in xrange(iters))
    values = (func(*p) for p in points)
    total = sum(values)
    ratio = total / float(iters)
    return ratio * domain.volume

''' Monte-Carlo simulation module. '''

import functools
import random


class Simulation(object):
    ''' Construct simulation over cartesian domain. '''
    def __init__(self, domain, rand=None):
        if rand is None:
            rand = random.Random()

        self._volume = 1
        for low, high in domain:
            self._volume *= (high - low)

        self._samplers = []
        for low, high in domain:
            sampler = functools.partial(rand.uniform, low, high)
            self._samplers.append(sampler)

    def sample(self):
        ''' Uniformly sample domain. '''
        return [s() for s in self._samplers]

    @property
    def volume(self):
        ''' Return pre-computed domain's volume. '''
        return self._volume

    def run(self, func, iters):
        ''' Runs Monte-Carlo simulation on specified *domain*. '''
        points = (self.sample() for _ in xrange(iters))
        values = (func(*p) for p in points)
        total = sum(values)
        ratio = total / float(iters)
        return ratio * self.volume


def simulate(domain, func, iters, rand=None):
    ''' Helper function. '''
    dom = Simulation(domain, rand)
    return dom.run(func, iters)

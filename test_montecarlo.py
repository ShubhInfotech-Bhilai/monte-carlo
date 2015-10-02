import montecarlo as mc
import math
import random
import unittest
import itertools


class RandomStub(object):
    def __init__(self, values):
        self.values = itertools.cycle(values)

    def uniform(self, low, high):
        value = next(self.values)
        return low + value * (high - low)


class TestDomain(unittest.TestCase):

    def test_empty(self):
        sim = mc.Simulation(domain=[])
        self.assertEquals(1, sim.volume)
        self.assertEquals([], sim.sample())

    def test_1d(self):
        stub = RandomStub([0.5])
        sim = mc.Simulation(domain=[(10, 20)], rand=stub)
        self.assertEquals(10, sim.volume)
        self.assertEquals([15], sim.sample())

    def test_2d(self):
        stub = RandomStub([0.5, 0.25])
        sim = mc.Simulation(domain=[(10, 20), (1, 5)], rand=stub)
        self.assertEquals(40, sim.volume)
        self.assertEquals([15, 2], sim.sample())

    def test_zero(self):
        res = mc.simulate([], func=lambda: 0, iters=1)
        self.assertEquals(0, res)


class Test2D(unittest.TestCase):

    def setUp(self):
        r = random.Random(1)
        self.sim = mc.Simulation(domain=[(0, 1), (0, 1)], rand=r)

    def test_half(self):
        area = self.sim.run(
            func=lambda x, y: (x + y < 1),
            iters=10**5)
        self.assertAlmostEqual(0.5, area, places=2)

    def test_circle(self):
        area = self.sim.run(
            func=lambda x, y: (x*x + y*y < 1),
            iters=10**5)
        self.assertAlmostEqual(math.pi / 4.0, area, places=2)


class Test3D(unittest.TestCase):

    def setUp(self):
        r = random.Random(1)
        self.sim = mc.Simulation(domain=[(-1, 1)]*3, rand=r)

    def test_shpere(self):
        volume = self.sim.run(
            func=lambda x, y, z: (x*x + y*y + z*z < 1),
            iters=10**5)
        self.assertAlmostEqual((4 * math.pi) / 3.0, volume, places=2)


if __name__ == '__main__':
    unittest.main()

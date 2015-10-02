import mc
import math
import random
import unittest


class MonteCarloTest2D(unittest.TestCase):

    def setUp(self):
        r = random.Random(1)
        self.dom = mc.Domain(ranges=[(0, 1), (0, 1)], rand=r)

    def test_diamond(self):
        area = mc.simulation(
            domain=self.dom,
            func=lambda x, y: (x + y < 1),
            iters=10**5)
        self.assertAlmostEqual(0.5, area, places=2)

    def test_circle(self):
        area = mc.simulation(
            domain=self.dom,
            func=lambda x, y: (x*x + y*y < 1),
            iters=10**5)
        self.assertAlmostEqual(math.pi / 4.0, area, places=2)


class MonteCarloTest3D(unittest.TestCase):

    def setUp(self):
        r = random.Random(1)
        self.dom = mc.Domain(ranges=[(-1, 1)]*3, rand=r)

    def test_shpere(self):
        volume = mc.simulation(
            domain=self.dom,
            func=lambda x, y, z: (x*x + y*y + z*z < 1),
            iters=10**5)
        self.assertAlmostEqual((4 * math.pi) / 3.0, volume, places=2)


if __name__ == '__main__':
    unittest.main()

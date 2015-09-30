import mc
import math
import random
import unittest

class MonteCarloTest(unittest.TestCase):

    def test_circle(self):
        r = random.Random(1)
        dom = mc.Domain(ranges=[(-1, 1), (-1, 1)], rand=r)
        func = lambda x, y: (x*x + y*y < 1)
        area = mc.simulation(domain=dom, func=func, n=10**5)
        self.assertAlmostEqual(math.pi, area, places=2)


if __name__ == '__main__':
    unittest.main()

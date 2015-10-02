''' Compute and plot the "XOR" of two circles. '''
import montecarlo as mc
from matplotlib import pyplot as plt


def main():
    dom = [(-1, 2), (-1, 1)]
    points = []

    def func(x, y):
        res = ((x**2 + y**2 < 1) != ((x-1)**2 + y**2 < 1))
        if res:
            points.append((x, y))
        return res

    area = mc.simulate(dom, func, 10**5)
    msg = 'Area: {:.3f}'.format(area)
    print msg
    xs, ys = zip(*points)
    plt.plot(xs, ys, '.')
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    main()

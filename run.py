''' Command line interface for running Monte-Carlo simulations. '''
import montecarlo as mc
import multiprocessing
from matplotlib import pyplot as plt
import logging
import time

log = logging.getLogger(__name__)


def parallel(domain, func, iters, pool_size=None):
    ''' Run simulation in parallel using multiprocessing. '''
    if pool_size is None:
        return mc.simulate(domain, func, iters)

    log.info('using pool of %d processes', pool_size)
    pool = multiprocessing.Pool(pool_size)
    results = []
    for _ in range(pool_size):
        args = [domain, func, iters / pool_size]
        # NOTE: args must be serializable (via cPickle),
        # since mc.simulate will run in another Python process.
        res = pool.apply_async(mc.simulate, args)
        results.append(res)
    results = [res.get() for res in results]

    return sum(results) / len(results)


def collect_points(func, points):
    def wrapper(*coords):
        res = func(*coords)
        if res:
            points.append(coords)
        return res
    return wrapper


def circle(x, y):
    return x**2 + y**2 < 1


def main(func):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--pool', type=int)
    p.add_argument('--iters', type=int, default=10**6)
    p.add_argument('--plot', action='store_true', default=False)
    args = p.parse_args()

    domain = [(-1, 1), (-1, 1)]

    if args.plot:
        points = []
        func = collect_points(func, points)

    start = time.time()
    area = parallel(
        domain=domain,
        func=func,
        iters=args.iters,
        pool_size=args.pool)
    duration = time.time() - start

    log.info('area: %.5f', area)
    log.info('duration: %.3f seconds', duration)

    if args.plot:
        xs, ys = zip(*points)
        plt.plot(xs, ys, '.')
        plt.axis('equal')
        plt.show()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s [%(process)s] %(levelname)-10s: %(message)s',
        level=logging.DEBUG)
    main(circle)

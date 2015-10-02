''' Compute PI in parallel. '''
import montecarlo as mc
import multiprocessing


def parallel(domain, func, iters, pool_size=None):
    ''' Run simulation in parallel using multiprocessing. '''
    if pool_size is None:
        return mc.simulate(domain, func, iters)

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


def func(x, y):
    return x**2 + y**2 < 1


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--pool', type=int)
    p.add_argument('--iters', type=int, default=10**6)
    args = p.parse_args()

    dom = [(-1, 1), (-1, 1)]
    area = parallel(dom, func, iters=args.iters, pool_size=args.pool)
    msg = 'Area: {:.5f}'.format(area)
    print msg


if __name__ == '__main__':
    main()

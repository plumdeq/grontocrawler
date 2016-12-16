#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# :author: Asan Agibetov
#
# Utils module, i.e., transformations of strings, urls etc.
#
from functools import wraps
import time


def memo(f):
    """
    Memoization for function ``f``, if recompute is True, then we force
    recomputation

    Args:
        f (func): function to memoize

    """
    cache = {}

    @wraps(f)
    def wrap(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]

    return wrap


def timeit(f, log=True):
    """
    Times the execution of the function ``f``

    Returns:
        *: result of applying ``f`` to ``args`` and ``kw``
        float: time needed to execute ``f``

    Usage
    -----

    Either use it as

    .. code-block:: python

        @timeit
        def new_fn():
            ...

    Or re-alias the function

    .. code-block:: python

        new_fn = timeit(new_fn)

    """
    def timed(*args, **kw):
        tstart = time.time()
        result = f(*args, **kw)
        tend = time.time()

        if log:
            print('func:%r args: [%r, %r] took: %2.4f sec' % \
                    (f.__name__, args, kw, tend-tstart))

        return (result, tend-tstart)

    return timed

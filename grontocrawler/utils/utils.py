#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# :author: Asan Agibetov

"""
   Copyright 2015-2017 Asan Agibetov <asan.agibetov@gmail.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

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

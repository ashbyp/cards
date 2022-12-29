import timeit
from functools import wraps
from time import perf_counter


def timefunc(name: str = None, repeat: int = 0):
    def decorate(func):
        @wraps(func)
        def _time_it(*args, **kwargs):
            start = timeit.default_timer()
            try:
                ret = func(*args, **kwargs)
                for _ in range(repeat):
                    ret = func(*args, **kwargs)
                return ret
            finally:
                elapsed = timeit.default_timer() - start
                print(f'Function:{name or "unknown"} elapsed seconds {elapsed:.10f} runs={repeat + 1:,d}')

        return _time_it

    return decorate


class timeblock:
    def __init__(self, name='Time', printout=True):
        self.name = name
        self.printout = printout

    def __enter__(self):
        self.time = perf_counter()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.time = perf_counter() - self.time  #
        self.readout = f'{self.name or "Time"}: {self.time:.10f} seconds'
        if self.printout:
            print(self.readout)


class StageTimer:
    def __init__(self, name='start'):
        self.times = [(perf_counter(), name)]

    def check(self, name=''):
        self.times.append((perf_counter(), name or str(len(self.times))))

    def report(self):
        print(f'{"Stage":<10}    {"Time":<12}    {"Total":<12}')
        start = prev = self.times[0][0]
        for curr, name in self.times:
            print(f'{name:<10}    {curr - prev:.10f}    {curr - start:.10f}')
            prev = curr


def time_and_check(fn, fn_args, expected, check_success=True, repeat=0):
    with timeblock(printout=False) as t:
        for _ in range(repeat + 1):
            res = fn(*fn_args)

    if check_success:
        success = res == expected
        print(f'  Got: {res} Expected: {expected} {t.readout}, Success: {success}')
        return success
    else:
        print(f'  Got: {res} Expected: {expected} {t.readout}')
        return None


class checker:
    def __init__(self, fn, check_success=True, repeat=0):
        self.fn = fn
        self.check_success = check_success
        self.repeat = repeat
        self.results = []
        msg = f'Testing "{self.fn.__name__}"'
        if repeat:
            msg += f' (function call will be repeated {self.repeat} times)'
        print(msg)

    def __enter__(self):
        return self

    def check_1(self, fn_arg, expected):
        self.results.append(time_and_check(self.fn, (fn_arg,), expected,
                                           check_success=self.check_success, repeat=self.repeat))

    def check_2(self, fn_arg1, fn_arg2, expected):
        self.results.append(time_and_check(self.fn, (fn_arg1, fn_arg2), expected,
                                           check_success=self.check_success, repeat=self.repeat))

    def check_3(self, fn_arg1, fn_arg2, fn_arg3, expected):
        self.results.append(time_and_check(self.fn, (fn_arg1, fn_arg2, fn_arg3), expected,
                                           check_success=self.check_success, repeat=self.repeat))

    def check_4(self, fn_arg1, fn_arg2, fn_arg3,fn_arg4, expected):
        self.results.append(time_and_check(self.fn, (fn_arg1, fn_arg2, fn_arg3, fn_arg4), expected,
                                           check_success=self.check_success, repeat=self.repeat))

    def __exit__(self, exception_type, exception_value, traceback):
        if self.check_success:
            if all(self.results):
                print('All passed')
            else:
                print(f'{self.results.count(False)} tests FAILED')

#-*- coding:utf-8 -*-

import time

class ProgBar():
    def __init__(self, step=100):
        self.step = int(step / 20)
        self.count = 1
        self.progress = 0
    def update(self):
        if self.count % self.step == 0:
            self.progress += 1
            print('\r[{:s}{:s}]'.format('#'*self.progress, ' '*(20 - self.progress)), end='')
        self.count += 1

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('\'{:s}\'  {:2.2f} ms  {:2.2f} sec  {:2.2f} min  {:2.2f} hour'.format(
                  method.__name__, (te - ts) * 1000, (te - ts), (te - ts) / 60, (te - ts) / 3600))
        return result
    return timed
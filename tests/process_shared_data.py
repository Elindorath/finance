#! /usr/bin/env python

from logging.handlers import DatagramHandler
import os
import time
import ctypes
from functools import partial
import traceback
from multiprocessing import Process, Pool, Value, Array, Manager
import pandas
import psutil
from sub_process import func
import global_vars


def memory_size_format(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return f'{num:3.1f}{unit}{suffix}'

        num /= 1024.0

    return f'{num:.1f}Yi{suffix}'



def print_traceback(e):
    print(traceback.print_exception(type(e), e, e.__traceback__))



def main():
    print(f'BEFORE DATAFRAME')
    print(psutil.virtual_memory())
    dataframe = pandas.DataFrame({
        'a': [i for i in range(10000000)],
        'b': [i for i in range(10000000)],
        'c': [i for i in range(10000000)],
    })

    # manager = Manager()
    # k = manager.Value(ctypes.py_object, dataframe)
    global_vars.init()
    k = Value(ctypes.py_object, lock=False)
    k.value = dataframe
    global_vars.g_dataframe = k
    # global_vars.g_dataframe = dataframe

    print(f'AFTER DATAFRAME')
    print(psutil.virtual_memory())



    # def func():
    #     print(f'CHILD: \n{dataframe}')
    #     print(f'CHILD: {os.getpid()}')
    #     p = psutil.Process()
    #     with p.oneshot():
    #         print(f'CHILD: {p.pid}')
    #         print(f'CHILD: {p.memory_full_info()}')
    #     time.sleep(10)



    dataframe.info(memory_usage="deep")
    print(f'PARENT: {os.getpid()}')
    p = psutil.Process()
    with p.oneshot():
        print('BEFORE')
        print(f'PARENT {p.pid}')
        print(f'PARENT {memory_size_format(p.memory_full_info().uss)}')
        print(f'PARENT {psutil.virtual_memory()}')

    count = 10

    with Pool(processes=len(os.sched_getaffinity(0))) as pool:
        # for id in range(count):
        #     pool.apply_async(func=func, args=(k, id), error_callback=print_traceback)
        # pool.map(func, ids)
        # pool.starmap(func=func, iterable=[(k, id) for id in range(count)])
        pool.map(func=func, iterable=[id for id in range(count)])

    # process = Process(target=func, args=(k,))

    # process.start()

    # with p.oneshot():
    #     print('AFTER')
    #     print(f'PARENT {p.pid}')
    #     print(f'PARENT {memory_size_format(p.memory_full_info().uss)}')
    #     print(f'PARENT {psutil.virtual_memory()}')

    # process.join()

    with p.oneshot():
        print('AFTER JOIN')
        print(f'PARENT {p.pid}')
        print(f'PARENT {memory_size_format(p.memory_full_info().uss)}')
        print(f'PARENT {psutil.virtual_memory()}')

main()

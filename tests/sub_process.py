import time
import os
import psutil
import global_vars


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def func(id):
# def func(dataframe, id):
    # print(f'CHILD: \n{dataframe}')
    # global g_dataframe
    # global_vars.g_dataframe.info(memory_usage="deep")
    global_vars.g_dataframe.value.info(memory_usage="deep")
    # dataframe.value.info(memory_usage="deep")
    # print(f'CHILD {id}: {id2}')
    print(f'CHILD {id}: {os.getpid()}')
    p = psutil.Process()
    with p.oneshot():
        print(f'CHILD {id}: {p.pid}')
        print(f'CHILD {id}: {sizeof_fmt(p.memory_full_info().uss)}')
        print(f'CHILD {id} {psutil.virtual_memory()}')
    # time.sleep(10)

def init(Value, ctypes):
    global world
    world = Value(ctypes.py_object, lock=False)

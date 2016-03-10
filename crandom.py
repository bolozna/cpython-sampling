"""Module for sampling uniformly random elements from dict and set data structures in linear time.
"""
import ctypes,random

dummy_key='<dummy key>'
ulong_len = ctypes.sizeof(ctypes.c_ulong)
py_object_len=ctypes.sizeof(ctypes.py_object)
entry_len=ulong_len+2*py_object_len
table_size_offset=ulong_len*4
table_pointer_offset=ulong_len*5

def choice_dict_ctypes(d):
    """Sample a uniformly random element from a non-empty dictionary in linear time using ctypes.
    """
    #Dict format:
    #refcount
    #type
    #number of slots that are not empty (including dummy elements)
    #number of slots containing actual values
    #total number of slots -1
    #total number of slots -1
    #*table

    #Table format:
    #hash
    #key
    #val

    table_size=ctypes.c_void_p.from_address(id(d)+table_size_offset).value+1
    table_pointer=ctypes.c_void_p.from_address(id(d)+table_pointer_offset).value
    table_value_offset=table_pointer+ulong_len+py_object_len

    while True:
        i=random.randrange(0,table_size)
        value=ctypes.c_void_p.from_address(table_value_offset+i*entry_len).value
        if value!=None:
            return ctypes.cast(ctypes.c_void_p.from_address(table_pointer+ulong_len+i*entry_len).value, ctypes.py_object).value


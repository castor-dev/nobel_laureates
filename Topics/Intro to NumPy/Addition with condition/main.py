import numpy as np

def custom_sum(arg1, arg2):

    if( isinstance(arg1, np.ndarray) and isinstance(arg2, np.ndarray) ):
        return arg1 + arg2
    elif( isinstance(arg1, list) and (isinstance(arg2, list))) :
        return 'Both arguments are lists, not arrays'
    else:
        return 'One argument is a list'


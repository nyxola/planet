import numpy as np
import unittest


# Setting the exception for when the UDMs are not the same size
class ShapeMismatch(Exception):
    pass

# Function to apply mask to original UDM and overwrite the product UDM
# where there is the value 1
def applymask(npinput, npmask):
    if npinput.shape != npmask.shape:
        raise ShapeMismatch
    npinput[npmask == 1] = 1
    return npinput

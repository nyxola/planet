import sys
import numpy as np
from optparse import OptionParser
from Task1 import applymask

# Reading in testing arguments
parser = OptionParser()
parser.add_option(
    "-e",
    "--example",
    default=1,
    type=int,
    help="choose an example mask")
(opts, args) = parser.parse_args()
example = opts.example
print('Example Mask ', example)

# Initialising example masks
npinput = np.array([[1, 1, 0], [1, 2, 2], [0, 2, 2]])
if example == 1:
    npmask = np.array([[1, 1, 1], [1, 0, 0], [2, 2, 2]])
elif example == 2:
    npmask = np.array([[1, 1, 2], [1, 0, 1], [2, 2, 1]])
else:
    print('WARNING: argument not recognised, please select --example 1 or 2')
    sys.exit()

# Run the function defined in __init__.py and print the UDMs to screen
print('Product Input:')
print(npinput)
print('=====')
print('Mask:')
print(npmask)
print('=====')
result = applymask(npinput, npmask)
print('Final Product Input:')
print(result)

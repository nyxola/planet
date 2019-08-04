import numpy as np


# Setting the exception for when the calibration vector is larger than the
# matrix
class MatrixMismatch(Exception):
    pass


# Preparing the calibration vector using calbration spacing, json vector and
# input matrix as arguments.  The m dimension of the matrix is used to determine
# how the calibrated vector is indexed.
def prep_vec(calib_space, calib_vec, M):
    calib_vec_len = len(calib_vec)
    M_col = len(M[0])
    if calib_vec_len < M_col:
        # Create a list of the matrix index increments
        m_col_index = [0]*M_col
        for i in range(M_col):
            m_col_index[i] = i
        # Generate the pixel indexes which are dependent on the calibration
        # spacing
        pixel_index = [0]*calib_vec_len
        for i in range(calib_vec_len):
            pixel_index[i] = pixel_index[i]+calib_space*i
        # Interpolate the calibration vector
        calib_vec_index = np.interp([m_col_index], pixel_index, calib_vec)
    # Raise exception when the calibrated vector is larger than the m dimension
    # of the matrix
    elif calib_vec_len > M_col:
        raise MatrixMismatch
    # New calibrated vector is the same as the original calibrated vector
    else:
        calib_vec_index = calib_vec
    return calib_vec_index


# Performing the calibration calculation by reading in the new calibrated vector
# and the matrix.
# NB Square rooting a matrix, as implied in the formula, is only possible if the
# matrix is a square, as this is not the case, for interpretation this step in
# the calculation has been omitted
def apply_calibration(index_vec, image_matrix):
    sq_index_vec = np.square(index_vec)
    calibrated_image_matrix = np.multiply(image_matrix, sq_index_vec)
    return calibrated_image_matrix

# This Python file uses the following encoding: utf-8

import cv2
import numpy as np

class CameraIntrisicsValue():
    def __init__(self,
                 CHECKERBOARD,
                 *arg, **args):
        self.CHECKERBOARD = CHECKERBOARD
        self.criteria = (cv2.TERM_CRITERIA_EPS + 
                         cv2.TERM_CRITERIA_MAX_ITER,
                         30,
                         0.001)
        # Creating vector to store vectors of 3D points for each checkerboard image
        self.objpoints = list()
        # Creating vector to store vectors of 2D points for each checkerboard image
        self.imgpoints = list()

        self.intrisics = list()


    def extracting_corners(self, foto):
        gray = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
        self.shape = foto.shape[:2]
        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        
        ret, corners = cv2.findChessboardCornersSB(gray,
                                                   self.CHECKERBOARD,
                                                   flags = (
                                                       cv2.CALIB_CB_NORMALIZE_IMAGE +
                                                       cv2.CALIB_CB_EXHAUSTIVE  +
                                                       cv2.CALIB_CB_ACCURACY +
                                                       cv2.CALIB_CB_LARGER
                                                          ))

        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display 
        them on the images of checker board
        """
        if ret == True:
            # Defining the world coordinates for 3D points
            objp = np.zeros((1, self.CHECKERBOARD[0] * self.CHECKERBOARD[1], 3), np.float32)
            objp[0,:,:2] = np.mgrid[0:self.CHECKERBOARD[0], 
                                         0:self.CHECKERBOARD[1]].T.reshape(-1, 2)
            self.objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray,
                                        corners, 
                                        (11,11),
                                        (-1,-1), 
                                        self.criteria)
            self.imgpoints.append(corners2)
            # Draw and display the corners
            return cv2.drawChessboardCorners(foto,
                                            self.CHECKERBOARD, 
                                            corners2, 
                                            ret)
        else:
            return foto

    def get_intrisic_parameters(self):
        """
        Performing camera calibration by 
        passing the value of known 3D points (objpoints)
        and corresponding pixel coordinates of the 
        detected corners (imgpoints)
        """
        return cv2.calibrateCamera(self.objpoints,
                                              self.imgpoints,
                                              self.shape,
                                              None,
                                              None)
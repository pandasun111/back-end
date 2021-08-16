import cv2
import numpy as np

from py_MVO import VisualOdometry
from collections import OrderedDict

def pose_estimate(input_frames, input_intrinsic, feature_detector):
    K = input_intrinsic
    vo = VisualOdometry(K, feature_detector, None)

    img_id = 0
    T_v_dict = OrderedDict()  # dictionary with image and translation vector as value

    for i, frame in enumerate(input_frames):
        imgKLT = np.array(frame)
        img = cv2.cvtColor(imgKLT, cv2.COLOR_RGB2GRAY)  # image for Visual Odometry

        # Create a CLAHE object (contrast limiting adaptive histogram equalization)
        clahe = cv2.createCLAHE(clipLimit=5.0)
        img = clahe.apply(img)

        if vo.update(img, img_id):  # Updating the vectors in VisualOdometry class
            if img_id == 0:
                T_v_dict[img_id] = ([[0], [0], [0]])
            else:
                T_v_dict[img_id] = vo.cur_t   # Retrieve the translation vectors for dictionary
            cur_t = vo.cur_t  # Retrieve the translation vectors

        img_id += 1  # Increasing the image id

    poses = []
    for t_v, R_m in zip(vo.T_vectors, vo.R_matrices):
        T = np.hstack((R_m, t_v))
        T = np.insert(T, 3, np.array([0.0, 0.0, 0.0, 1.0]), 0)
        poses.append(T)
    
    return poses

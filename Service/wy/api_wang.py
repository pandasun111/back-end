import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/src/RGBReconstruct/")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/src/PoseEstimate/")

from src.RGBReconstruct.reconstruct import reconstruct
from src.PoseEstimate.pose_estimation import pose_estimate

def reconstruct_from_rgb(input_frames, input_extrincs, input_intrinsic):
    """
    Args:
        input_frames: input video stream
        input_extrincs: input extrincs of frames
        input_intrinsic: input intrinsic

    return:
        mesh: object of the scene reconstruction, the type of 'mesh' is <class 'trimesh.base.Trimesh'>
    """
    intrinsic = input_intrinsic[:3, :3]
    frame_num = len(input_frames)
    frames = []
    for i in range(frame_num):
        frame = {"file":input_frames[i], "intrinsics":intrinsic, "pose":input_extrincs[i]}
        frames.append(frame)
    info = {"dataset": "dateset",
            "path": "path",
            "scene": "scene",
            "frames": frames}

    mesh = reconstruct(info)
    
    return mesh

def pose_estimation_from_rgb(input_frames, input_intrinsic, feature_detector="SIFT"):
    """
    Args:
        input_frames: input video stream
        input_intrinsic: input intrinsic
        feature_detector: SIFT, FAST, SURF, SHI-TOMAS

    return:
        poses: camera pose predicted from video sequence
    """
    intrinsic = input_intrinsic[:3, :3]
    poses = pose_estimate(input_frames, intrinsic, feature_detector)

    return poses
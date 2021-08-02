import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/src/")

from src.process import process

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

    mesh = process(info)
    
    return mesh
 
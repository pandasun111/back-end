from src.fusion_depth import depth2mesh, rgbd2mesh


def reconstruct_from_depth(Input_depths, Input_extrincs, intrinsics, Input_frames=None):
    n_imgs = len(Input_depths)

    if Input_frames is None:
        colors = None
        vertices, triangles = depth2mesh(Input_depths, Input_extrincs, intrinsics, n_imgs)
    else:
        vertices, triangles, colors = rgbd2mesh(Input_depths, Input_extrincs, Input_frames, intrinsics, n_imgs)

    return vertices, triangles, colors

import os
import cv2
import sys
import numpy as np
import glob
def progressbar(current, total, num=40, prefix=""):
    sys.stdout.write("\r{} {}/{} |{}{}| {:.2f}%".format(prefix, current, total,
                                                        "*" * int(num * current / total),
                                                        " " * (num - int(num * current / total)),
                                                        100 * current / total))
    sys.stdout.flush()
    if current == total:
        print("")

def depth_raw2_rgb(depth):
    min, max = np.min(depth), np.max(depth)
    dep = (depth - min) / (max - min)

    dep = (dep * 255).astype(np.uint8)
    return dep

def frames2video(save_path, frames, fps=24):
    base_folder = os.path.split(save_path)[0]
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    H, W = frames[0].shape[0:2]
    img_size = (W, H)

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    video_writer = cv2.VideoWriter(save_path, fourcc, fps, img_size)

    num = 0
    for frame in frames:
        video_writer.write(frame)
        num += 1
        progressbar(num, len(frames), prefix="write video")

    video_writer.release()

def framepaths2video(save_path, frames_paths, fps=24):
    base_folder = os.path.split(save_path)[0]
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    H, W = cv2.imread(frames_paths[0]).shape[0:2]
    img_size = (W, H)

    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    video_writer = cv2.VideoWriter(save_path, fourcc, fps, img_size)

    num = 0
    for fp in frames_paths:
        frame = cv2.imread(fp)
        video_writer.write(frame)
        num += 1
        progressbar(num, len(frames_paths), prefix="write video")

    video_writer.release()

if __name__ == '__main__':
    rgb_folder = r"J:\datasets\Scannet\data\scans\scene0000_01\rgbd\rgb"
    depth_folder = r"J:\datasets\Scannet\data\scans\scene0000_01\rgbd\depth"

    #rgb_files = glob.glob(os.path.join(rgb_folder, "*.jpg"))
    #framepaths2video("../Data/demo/rgb.mp4", rgb_files, fps=30)
    depth_raw_files = glob.glob(os.path.join(depth_folder, "*.png"))

    tmp_folder = "./depth_tmp"
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)
    for i, df in enumerate(depth_raw_files):
        if i == 28:
            continue
        dim = cv2.imread(df)
        dim = depth_raw2_rgb(dim)
        cv2.imwrite(os.path.join(tmp_folder, "%06d.png" % i), dim)
        progressbar(i+1, len(depth_raw_files))

    depth_files = glob.glob(os.path.join(tmp_folder, "*.png"))
    framepaths2video("../Data/demo/depth.mp4", depth_files, fps=30)

import torch
import numpy as np
from networks import PointNet2
from skimage.color import label2rgb
import open3d as o3d
import copy

def write_ply(file_path, pcs,  colors):
	colors = (colors * 256).clip(0, 255).astype(np.uint8)
	with open(file_path, "w") as f:
		f.write("ply\n")
		f.write("format binary_little_endian 1.0\n")
		f.write("element vertex {}\n".format(len(pcs)))
		f.write("property double x\n")
		f.write("property double y\n")
		f.write("property double z\n")
		f.write("property uchar red\n")
		f.write("property uchar green\n")
		f.write("property uchar blue\n")
		f.write("end_header")

		for i in range(len(pcs)):
			f.write("{} {} {} {} {} {}\n".format(pcs[i,0], pcs[i,1], pcs[i,2], colors[i, 0],colors[i, 1], colors[i, 2]))


	f.close()

def split_pcs(pcs, per_split=4096):
	pc_num = len(pcs)
	pc_channle = len(pcs[0, :])
	if pc_num < per_split:
		return pcs

	batches = int(pc_num / per_split)
	upper_pc_index = np.arange(0, batches * per_split)
	rest_pc_index = np.arange(batches * per_split, pc_num)

	upper_pc = pcs[upper_pc_index, :].reshape((-1, per_split, pc_channle))
	rest_pc = np.array([pcs[rest_pc_index, :]])

	if rest_pc.shape[1] == 0:
		rest_pc = None
	return upper_pc, rest_pc


def SemanticSeg(pcs):
	org_pcs = copy.deepcopy(pcs)
	device = torch.device("cuda")

	network = PointNet2(use_xyz=True, attr_channel=6, class_num=13, task="sem", group_type="ssg")

	pth_path = "./epoch=15-val_loss=0.53-val_acc=0.862.ckpt"

	paramters = torch.load(pth_path, map_location=device)["state_dict"]

	pointnet2_state_dict = {}
	for k, v in paramters.items():

		pointnet2_state_dict["network." + k] = v

	network.load_state_dict(pointnet2_state_dict)
	network.eval().to(device)

	pcs, pcs_rest = split_pcs(pcs, per_split=40960)
	print(pcs.shape)
	labels = []
	with torch.no_grad():
		for c in range(len(pcs)):
			#print(c)
			ppcs = torch.from_numpy(pcs[c]).unsqueeze(0).float().cuda()

			_, outs = network(ppcs)
			label = torch.argmax(outs, dim=1).cpu().detach().numpy()
			labels.append(label)

		if pcs_rest is not None:
			pcs_rest = torch.from_numpy(pcs_rest).float().cuda()

			_, outs = network(pcs_rest)
			label_rest = torch.argmax(outs, dim=1).cpu().detach().numpy()
		#labels.append(label)
	#print(np.concatenate(labels, axis=0).reshape(-1).shape)
	if pcs_rest is not None:
		labels = np.concatenate(labels, axis=0).reshape(-1).tolist() + label_rest.reshape(-1).tolist()
	else:
		labels = np.concatenate(labels, axis=0).reshape(-1).tolist()
	rgb = label2rgb(np.array(labels))
	xyz = org_pcs[:, 6:9]
	return labels



if __name__ == "__main__":
	pcs = o3d.io.read_point_cloud("./t.ply")

	# 需要 pcs [N, 3]点云， rgb [N, 3]逐点颜色 
	import open3d as o3d

	pcs = o3d.geometry.PointCloud()
	pcs.points = o3d.utility.Vector3dVector(xyz)
	ppc.colors = o3d.utility.Vector3dVector(rgb)

	pcs.estimate_normals()
	points = pcs.points
	colors = pcs.colors
	normals = pcs.normals

	#pcs = torch.load("./test.pth")["data"].numpy()

	#pcs = pcs.reshape((-1, 9))


	pcs = np.concatenate([colors, normals, points], axis=1)
	print(pcs.shape)
	label = SemanticSeg(pcs)

	colors = [np.random.uniform(0,1,(3)) for _ in range(13)]

	xyz = pcs[:, 6:9]
	rgb = label2rgb(np.array(label), colors = colors)

	ppc = o3d.geometry.PointCloud()
	ppc.points = o3d.utility.Vector3dVector(xyz)
	ppc.colors = o3d.utility.Vector3dVector(rgb)

	o3d.io.write_point_cloud("./test1.ply", ppc)
import os
import torch

from data_wy import SceneDataset
from model import VoxelNet
import transforms as transforms

def process(info):
    """
    Args:
        info: info for the scene
        model: pytorch model that implemets Atlas
        
    return:
        mesh: object of the scene reconstruction whose type is <class 'trimesh.base.Trimesh'>
    """
    # load model
    model = VoxelNet.load_from_checkpoint(os.path.dirname(os.path.realpath(__file__)) + "/model.ckpt")
    model = model.cuda().eval()
    torch.set_grad_enabled(False)

    # if GPU does not have enough memory
    model.voxel_dim_test = [208, 208, 80]
    model.voxel_dim_val = model.voxel_dim_test

    voxel_scale = model.voxel_sizes[0]
    dataset = SceneDataset(info, voxel_sizes=[voxel_scale],
                           voxel_types=model.voxel_types)

    # compute voxel origin
    if 'file_name_vol_%02d'%voxel_scale in dataset.info:
        tsdf_trgt = dataset.get_tsdf()['vol_%02d'%voxel_scale]
        voxel_size = float(voxel_scale)/100
        shift = torch.tensor([.5, .5, .5])//voxel_size
        offset = tsdf_trgt.origin - shift*voxel_size

    else:
        offset = torch.tensor([0,0,-.5])
    T = torch.eye(4)
    T[:3,3] = offset

    transform = transforms.Compose([
        transforms.ResizeImage((640,480)),
        transforms.ToTensor(),
        transforms.TransformSpace(T, model.voxel_dim_val, [0,0,0]),
        transforms.IntrinsicsPoseToProjection(),
    ])
    dataset.transform = transform
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=None,
                                             batch_sampler=None, num_workers=2)

    scene = dataset.info['scene']

    model.initialize_volume()
    torch.cuda.empty_cache()

    for j, d in enumerate(dataloader):
        model.inference1(d['projection'].unsqueeze(0).cuda(),
                         image=d['image'].unsqueeze(0).cuda())
    outputs, losses = model.inference2()

    tsdf_pred = model.postprocess(outputs)[0]

    tsdf_pred.origin = offset.view(1,3).cuda()
  
    if 'semseg' in tsdf_pred.attribute_vols:
        mesh_pred = tsdf_pred.get_mesh('semseg')
    else:
        mesh_pred = tsdf_pred.get_mesh()

    return mesh_pred

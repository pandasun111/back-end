import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/pointnet2_sem/")
from pointnet2_sem.sem_seg import SemanticSeg

def api_semantic_segmentation(pcs):
	return SemanticSeg(pcs)
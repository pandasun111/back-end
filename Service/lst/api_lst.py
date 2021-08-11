from pointnet2_sem import SemanticSeg
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/pointnet2_sem/")

def api_semantic_segmentation(pcs):
	return SemanticSeg(pcs)
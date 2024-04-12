import os

class Config():
    def __init__(self, input_video, out_video_path):
        self.det_config = "demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py"
        self.det_checkpoint = "./pretrained_models/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth"
        self.pose_config = "configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/ViTPose_huge_coco_256x192.py"
        self.pose_checkpoint = "./pretrained_models/vitpose-h.pth"
        self.video_path = input_video
        self.device = 'cuda:0'
        self.bbox_thr = 0.3
        self.kpt_thr = 0.001
        self.det_cat_id = 1
        self.radius = 4
        self.thickness = 1
        self.show = False
        self.out_video_path = out_video_path
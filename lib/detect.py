# Copyright (c) OpenMMLab. All rights reserved.
import os
import cv2
import warnings
import numpy as np

from mmpose.apis import (inference_top_down_pose_model, init_pose_model,
                         process_mmdet_results, vis_pose_result)
from mmpose.datasets import DatasetInfo

try:
    from mmdet.apis import inference_detector, init_detector
    has_mmdet = True
except (ImportError, ModuleNotFoundError):
    has_mmdet = False

assert has_mmdet, 'Please install mmdet to run the demo.'

from lib.config import Config

def detect(input_video, out_video_path, csv_out_path=None):
    '''config:
    python demo/top_down_video_demo_with_mmdet.py \                                                                               ─╯
        demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py \
        https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth \
        configs/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/ViTPose_huge_coco_256x192.py \
        ./pretrained_models/vitpose-h.pth \
        --img-root tests/data/coco/ \
        --img 000000196141.jpg \
        --out-img-root vis_results
    '''

    config = Config(input_video, out_video_path)
    det_model = init_detector(
        config.det_config, config.det_checkpoint, device=config.device.lower())
    # build the pose model from a config file and a checkpoint file
    pose_model = init_pose_model(
        config.pose_config, config.pose_checkpoint, device=config.device.lower())

    dataset = pose_model.cfg.data['test']['type']
    dataset_info = pose_model.cfg.data['test'].get('dataset_info', None)
    if dataset_info is None:
        warnings.warn(
            'Please set `dataset_info` in the config.'
            'Check https://github.com/open-mmlab/mmpose/pull/663 for details.',
            DeprecationWarning)
    else:
        dataset_info = DatasetInfo(dataset_info)

    ###############################
        
    cap = cv2.VideoCapture(config.video_path)
    # assert cap.isOpened(), f'Faild to load video file {config.video_path}'

    if config.out_video_path == '':
        save_out_video = False
    else:
        os.makedirs(os.path.split(config.out_video_path)[0], exist_ok=True)
        save_out_video = True
    
    fps = None
    if save_out_video:
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        videoWriter = cv2.VideoWriter(config.out_video_path, fourcc, fps, size)

    # optional
    return_heatmap = False

    # e.g. use ('backbone', ) to return backbone feature
    output_layer_names = None

    frame_index = 0
    result = []
    while (cap.isOpened()):
        flag, img = cap.read()
        if not flag:
            break
        # test a single image, the resulting box is (x1, y1, x2, y2)
        mmdet_results = inference_detector(det_model, img)

        # keep the person class bounding boxes.
        person_results = process_mmdet_results(mmdet_results, config.det_cat_id)

        # test a single image, with a list of bboxes.
        pose_results, returned_outputs = inference_top_down_pose_model(
            pose_model,
            img,
            person_results,
            bbox_thr=config.bbox_thr,
            format='xyxy',
            dataset=dataset,
            dataset_info=dataset_info,
            return_heatmap=return_heatmap,
            outputs=output_layer_names)

        # show the results
        vis_img = vis_pose_result(
            pose_model,
            img,
            pose_results[:1],
            dataset=dataset,
            dataset_info=dataset_info,
            kpt_score_thr=config.kpt_thr,
            radius=config.radius,
            thickness=config.thickness,
            show=False)
        
        # May not need in video mode        
        ### Save landmarks if all landmarks were detected
        # min_landmark_score = min(
        #     [keypoint[2] for keypoint in person_results["keypoints"]])
        # should_keep_image = min_landmark_score >= detection_threshold
        # if not should_keep_image:
        #   self._messages.append('Skipped ' + video_path +
        #                         '. No pose was confidentlly detected.')
        #   continue
        
        ## Dont need to record the playback time bc have already fix the FPS of each video
        # playback_time = np.round((frame_index/fps)*1000, 1)
        # playback_time in milliseconds
        
        frame_index += 1
        if len(pose_results) == 0:
            result.append([None]*51) # [playback_time]+ [None]*51
            continue

        # choose the first person in results -> pose_results[0]
        pose_landmarks = np.array(
            [[keypoint[0] , keypoint[1], keypoint[2]]
              for keypoint in pose_results[0]["keypoints"]],
            dtype=np.float32)
        
        
        coordinates = pose_landmarks.flatten().astype(np.str_).tolist()
        
        result.append(coordinates)

        if save_out_video:
            videoWriter.write(vis_img)


    cap.release()

    if save_out_video:
        videoWriter.release()

    return result
    # if config.show:
    #     cv2.destroyAllWindows()

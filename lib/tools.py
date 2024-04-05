import cv2
import ffmpeg

def verify_video(video_path):
    try:
        vid = cv2.VideoCapture(video_path)
        if not vid.isOpened():
            raise NameError('Just a Dummy Exception, write your own')
    except cv2.error as e:
        print("cv2.error:", e)
        return False
    except Exception as e:
        print("Exception:", e)
        return False
    else:
        return True

def convert_video(video_path, out_video_root, target_fps=30):
    stream = ffmpeg.input(video_path) # video location
    stream = stream.filter('fps', fps=30, round='up')
    # stream = stream.filter('scale', w=1920, h=1080) # optional
    stream = ffmpeg.output(stream, out_video_root).overwrite_output()

    ffmpeg.run(stream)

def get_video_info(video_path):
    vid = cv2.VideoCapture(video_path)
    width  = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    return {"width": width, "height": height, "frame_count": frame_count}
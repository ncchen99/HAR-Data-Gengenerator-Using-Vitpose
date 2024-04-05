# Data format

### data.csv

```csv=
NOSE_x,NOSE_y,NOSE_score,LEFT_EYE_x,LEFT_EYE_y,...RIGHT_ANKLE_y,RIGHT_ANKLE_score
850.5722,183.71024,0.98314494,851.8405,175.64206,...,595.28613,0.93685526
...
```

### info.csv

> Our generator will normolize FPS to 30 for each video. So we don't store FPS info to file

#### format

```csv=
category_name,category_id,video_amount
filename,width,height,frame_count
filename,width,height,frame_count
....
category_name,category_id,video_amount
filename,width,height,frame_count
filename,width,height,frame_count
...
...
```

#### example

```csv=
armNotHigh,1,1
19-Right.mp4,1920,1080,65
headBack,2,1
17-Right.mp4,1280,768,45
...
```

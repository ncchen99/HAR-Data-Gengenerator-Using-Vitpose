import pandas as pd
import os
import shutil
import sys
import csv
import tempfile
import tqdm

from lib.data import BodyPart
from lib.detect import detect
from lib.tools import verify_video, convert_video, get_video_info

#@title Code to load the images, detect pose landmarks and save them into a CSV file

class VitPosePreprocessor():
  """Helper class to preprocess pose sample images for classification."""

  def __init__(self,
               videos_in_folder,
               videos_out_folder,
               csvs_out_path):
    """Creates a preprocessor to detection pose from images and save as CSV.
    config:
      videos_in_folder: Path to the folder with the input images. It should
        follow this structure:
        yoga_poses
        |__ downdog
            |______ 00000128.jpg
            |______ 00000181.bmp
            |______ ...
        |__ goddess
            |______ 00000243.jpg
            |______ 00000306.jpg
            |______ ...
        ...
      videos_out_folder: Path to write the images overlay with detected
        landmarks. These images are useful when you need to debug accuracy
        issues.
      csvs_out_path: Path to write the CSV containing the detected landmark
        coordinates and label of each image that can be used to train a pose
        classification model.
    """
    self._videos_in_folder = videos_in_folder
    self._videos_out_folder = videos_out_folder
    self._csvs_out_path = csvs_out_path
    self._messages = []

    # Create a temp dir to store the pose CSVs per class
    self._csvs_out_folder_per_class = tempfile.mkdtemp()

    # Get list of pose classes and print image statistics
    self._pose_class_names = sorted(
        [n for n in os.listdir(self._videos_in_folder) if not n.startswith('.')]
        )
    
    os.makedirs(csvs_out_path, exist_ok=True)
    self.all_data_csv_path = os.path.join(csvs_out_path, "data.csv")
    self.all_info_csv_path = os.path.join(csvs_out_path, "info.csv")
    
    self.all_info_table = pd.DataFrame(columns=range(4)) 
    
    title = []
    for bodypart in BodyPart:
        title.extend([bodypart.name + '_x', bodypart.name + '_y', bodypart.name + '_score'])

    with open(self.all_data_csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(title)
        

  def process(self, per_pose_class_limit=None, detection_threshold=0.1):
    """Preprocesses images in the given folder.
    config:
      per_pose_class_limit: Number of images to load. As preprocessing usually
        takes time, this parameter can be specified to make the reduce of the
        dataset for testing.
      detection_threshold: Only keep images with all landmark confidence score
        above this threshold.
    """
    info_table_line_count = 0
    # Loop through the classes and preprocess its images
    for pose_class_index, pose_class_name in enumerate(self._pose_class_names):
      print('Preprocessing', pose_class_name, file=sys.stderr)

      # Paths for the pose class.
      videos_in_folder = os.path.join(self._videos_in_folder, pose_class_name)
      videos_out_folder = os.path.join(self._videos_out_folder, pose_class_name)

      if not os.path.exists(videos_out_folder):
        os.makedirs(videos_out_folder)

      # Detect landmarks in each image and write it to a CSV file

      # Get list of images
      videos_names = sorted(
          [n for n in os.listdir(videos_in_folder) if not n.startswith('.')])
      if per_pose_class_limit is not None:
        videos_names = videos_names[:per_pose_class_limit]

      valid_video_count = 0
      
      self.all_info_table.loc[info_table_line_count] = [pose_class_name, pose_class_index+1, 0, ""]
      self.all_info_table.to_csv(self.all_info_csv_path, index=False, header=False)
      
      # Detect pose landmarks from each image
      for video_name in tqdm.tqdm(videos_names):
        video_path = os.path.join(videos_in_folder, video_name)

        # Verify if the video is valid
        if not verify_video(video_path):
          self._messages.append('Skipped ' + video_path + '. Invalid video.')
          continue
        
        # Convert the video FPS 30
        tmp = tempfile.NamedTemporaryFile(suffix='.mp4')
        convert_video(video_path, tmp.name, 30)
        
        video_info = get_video_info(tmp.name)
        
        csv_out_path = os.path.join(videos_out_folder,
                                  f"{video_name}.csv")
        
        res = detect(tmp.name, os.path.join(videos_out_folder, video_name))
        
        tmp.close()
        
        if res:
          valid_video_count += 1
          self.all_info_table.loc[info_table_line_count + valid_video_count] = [video_name, video_info["width"], video_info["height"], video_info["frame_count"]]
          self.all_info_table.iat[info_table_line_count, 2] = valid_video_count
          self.all_info_table.to_csv(self.all_info_csv_path, index=False, header=False)
    
        pd.DataFrame(res).to_csv(csv_out_path, index=False)

        # combine this csv into big one
        with open(self.all_data_csv_path, "ab") as fout:
            with open(csv_out_path, "rb") as f:
                next(f)  # skip the header
                fout.write(f.read())

      if not valid_video_count:
        raise RuntimeError(
            'No valid videos found for the "{}" class.'
            .format(pose_class_name))
      
      # Add the class info to the info table
      info_table_line_count += valid_video_count + 1
      

    # Print the error message collected during preprocessing.
    print('\n'.join(self._messages))

  def class_names(self):
    """List of classes found in the training dataset."""
    return self._pose_class_names



"""useless class functions

  def _all_landmarks_as_dataframe(self):
    # Merge all per-class CSVs into a single dataframe.
    total_df = None
    for class_index, class_name in enumerate(self._pose_class_names):
      csv_out_path = os.path.join(self._csvs_out_folder_per_class,
                                  class_name + '.csv')
      per_class_df = pd.read_csv(csv_out_path, header=None)

      # Add the labels
      per_class_df['class_no'] = [class_index]*len(per_class_df)
      per_class_df['class_name'] = [class_name]*len(per_class_df)

      # Append the folder name to the filename column (first column)
      per_class_df[per_class_df.columns[0]] = (os.path.join(class_name, '')
        + per_class_df[per_class_df.columns[0]].astype(str))

      if total_df is None:
        # For the first class, assign its data to the total dataframe
        total_df = per_class_df
      else:
        # Concatenate each class's data into the total dataframe
        total_df = pd.concat([total_df, per_class_df], axis=0)

    list_name = [[bodypart.name + '_x', bodypart.name + '_y',
                  bodypart.name + '_score'] for bodypart in BodyPart]
    header_name = []
    for columns_name in list_name:
      header_name += columns_name
    header_name = ['file_name'] + header_name
    header_map = {total_df.columns[i]: header_name[i]
                  for i in range(len(header_name))}

    total_df.rename(header_map, axis=1, inplace=True)

    return total_df

"""
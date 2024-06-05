import os
import re
import pandas as pd
from pathlib import Path 

video_extensions = ('.mp4', '.MP4', '.mov', '.MOV')
    
def remove_emoji(text):
    return text.replace("❓", "") # no emoji


def file_exists_with_extension(directory, extension):
    if os.path.isfile(directory):
        return False
    for file in os.listdir(directory):
        if file.endswith(extension):
            return True
    return False

def find_videos_and_csvs(root_folder):
    categories = os.listdir(root_folder)
    
    category_data = {}
    for category in categories:
        category_path = os.path.join(root_folder, category)
        if not file_exists_with_extension(category_path, video_extensions):
            continue
        if os.path.isdir(category_path):
            # videos = [f for f in os.listdir(category_path) if f.endswith(video_extensions)]
            csv_paths = [os.path.join("poses_videos_out_train/all-data", f + ".csv") for f in os.listdir(category_path) if f.endswith(video_extensions)]
            category_data[category] = {
                # 'videos': videos,
                'csv_path': csv_paths
            }
    
    return category_data

def merge_csvs(category_data, all_info_csv_path ,header_csv, output_folder):
    all_info_table = pd.read_csv(all_info_csv_path, header=None)
    all_info_table.columns = ['a', 'b', 'c', 'd']
    for category, data in category_data.items():
        csv_paths = data['csv_path']
        combined_df = pd.read_csv(header_csv, nrows=0)
        info_df = pd.DataFrame([[category, 0, len(csv_paths), ""]], columns=["a", "b", "c", "d"])
        for csv_path in csv_paths:
            csv_path = remove_emoji(csv_path)
            if os.path.exists(csv_path):
                tmp_df = pd.read_csv(csv_path, header=None, skiprows=1)
                # tmp_df['Category'] = category  # Add category column for identification
                tmp_df.columns = combined_df.columns
                combined_df = pd.concat([combined_df, tmp_df], ignore_index=True)
                info_df = pd.concat([info_df, all_info_table.loc[all_info_table['a'] == "".join([a + "." for a in csv_path.split("/")[-1].split(".")][:-1])[:-1]]])
            else:
                print(f"CSV for category {category} not found: {csv_path}")
        combined_df.to_csv(os.path.join(output_folder, f"{category}_data.csv"), index=False)
        info_df.to_csv(os.path.join(output_folder,f"{category}_info.csv"), index=False, header=False)
    return combined_df

def main(root_folder, output_folder):
    category_data = find_videos_and_csvs(root_folder)
    combined_df = merge_csvs(category_data, "/home/mcnlab/桌面/VitPose/ViTPose/poses_videos_out_train/info.csv", "poses_videos_out_train/data.csv", output_folder)
    
    print(f"Combined CSV saved to {output_csv}")

if __name__ == "__main__":
    root_folder = '/home/mcnlab/桌面/VitPose/ViTPose/Backflip_Dataset'  # 替換為你的根目錄路徑
    output_csv = '/home/mcnlab/桌面/VitPose/ViTPose/data/'  # 替換為你想要輸出的 CSV 路徑
    main(root_folder, output_csv)

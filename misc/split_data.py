import os
import random
import shutil

# 設定根目錄
root_dir = './all'  # 請將根目錄設定為包含所有類別資料夾的父目錄

# 設定切分後的目標資料目錄
train_dir = './data/train'
test_dir = './data/test'

# 建立目標資料目錄
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 設定訓練集和測試集的比例
train_split = 0.8  # 80% 的資料用於訓練，20% 的資料用於測試

# 遍歷根目錄下的所有子目錄
for class_folder in os.listdir(root_dir):
    class_path = os.path.join(root_dir, class_folder)

    # 確認路徑是資料夾且不是 train 或 test 目錄
    if os.path.isdir(class_path) and class_folder not in ['train', 'test']:
        # 取得該類別資料夾下所有影片檔案
        files = [f for f in os.listdir(class_path) if f.endswith('.mp4') or f.endswith('.MOV')]

        # 隨機打亂影片順序
        random.shuffle(files)

        # 計算訓練集和測試集的分界點
        split_index = int(len(files) * train_split)

        # 分割成訓練集和測試集
        train_files = files[:split_index]
        test_files = files[split_index:]

        # 將影片複製到目標資料夾中的相應類別資料夾
        for file in train_files:
            src_path = os.path.join(class_path, file)
            dest_path = os.path.join(train_dir, class_folder, file)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(src_path, dest_path)

        for file in test_files:
            src_path = os.path.join(class_path, file)
            dest_path = os.path.join(test_dir, class_folder, file)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(src_path, dest_path)

print("資料切分完成。")

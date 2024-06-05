import os
import random
import shutil

# 設定根目錄
root_dir = './Backflip_Dataset'  # 請將根目錄設定為包含所有類別資料夾的父目錄

# 設定切分後的目標資料目錄
train_dir = './data/train'
test_dir = './data/test'

# 建立目標資料目錄
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 設定訓練集和測試集的比例
train_split = 0.8  # 80% 的資料用於訓練，20% 的資料用於測試

# 定義需要匹配數量的類別對
category_pairs = [
    ('0+_left', '0-_left'), ('0+_right', '0-_right'),
    ('1+_left', '1-_left'), ('1+_right', '1-_right'),
    ('2+_left', '2-_left'), ('2+_right', '2-_right'),
    ('3+_left', '3-_left'), ('3+_right', '3-_right'),
    ('4+_left', '4-_left'), ('4+_right', '4-_right'),
    ('5+_left', '5-_left'), ('5+_right', '5-_right'),
    ('6+_left', '6-_left'), ('6+_right', '6-_right')
]

category_pairs2 = [
    ('0+', '0-'), ('1+', '1-'), ('2+', '2-'), ('3+', '3-'), ('4+', '4-'), ('5+', '5-'), ('6+', '6-')
]


# 遍歷每對類別
for pos_category, neg_category in category_pairs2:
    pos_class_path = os.path.join(root_dir, pos_category)
    neg_class_path = os.path.join(root_dir, neg_category)

    # 確認兩個路徑都是資料夾
    if os.path.isdir(pos_class_path) and os.path.isdir(neg_class_path):
        # 取得正類別和負類別資料夾下的所有影片檔案
        pos_files = [f for f in os.listdir(pos_class_path) if f.endswith('.mp4') or f.endswith('.MOV') or f.endswith('.mov')]
        neg_files = [f for f in os.listdir(neg_class_path) if f.endswith('.mp4') or f.endswith('.MOV') or f.endswith('.mov')]

        # 隨機打亂影片順序
        random.shuffle(pos_files)
        random.shuffle(neg_files)
        

        # 確保每對類別的數量一致
        min_size = min(len(pos_files), len(neg_files))
        print(f"min_size: {min_size}")
        pos_files = pos_files[:min_size]
        neg_files = neg_files[:min_size]

        # 計算訓練集和測試集的分界點
        split_index = int(min_size * train_split)

        # 分割成訓練集和測試集
        pos_train_files = pos_files[:split_index]
        pos_test_files = pos_files[split_index:]
        neg_train_files = neg_files[:split_index]
        neg_test_files = neg_files[split_index:]

        # 將正類別影片複製到目標資料夾中的相應類別資料夾
        for file in pos_train_files:
            src_path = os.path.join(pos_class_path, file)
            dest_path = os.path.join(train_dir, pos_category, file)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(src_path, dest_path)

        for file in pos_test_files:
            src_path = os.path.join(pos_class_path, file)
            dest_path = os.path.join(test_dir, pos_category, file)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(src_path, dest_path)

        # 將負類別影片複製到目標資料夾中的相應類別資料夾
        for file in neg_train_files:
            src_path = os.path.join(neg_class_path, file)
            dest_path = os.path.join(train_dir, neg_category, file)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(src_path, dest_path)

        for file in neg_test_files:
            src_path = os.path.join(neg_class_path, file)
            dest_path = os.path.join(test_dir, neg_category, file)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(src_path, dest_path)

print("資料切分完成。")

import os
import random

def generate_txt_content(image_path, data_root_dir):
    data_root_dir = os.path.normpath(data_root_dir)  # '/home/cluster/Desktop/3d_eye/test_data'
    relative_path = os.path.relpath(image_path, data_root_dir) #'stream1_20220727_172431/POSTERIOR/image_03/data/000000821.jpg'
    data_name = os.path.dirname(os.path.dirname(os.path.dirname(relative_path))) #'stream1_20220727_172431/POSTERIOR'
    image_type = 'l' if 'image_02' in image_path else 'r' #'r'
    image_number = os.path.splitext(os.path.basename(image_path))[0]#'000000821'
    # 删除 "000000" 部分
    image_number = image_number[6:]#'821'
	# 生成原始条目
    original_entry = f"{data_name} {image_number} {image_type}\n"
    # 如果图像类型为 'r'，则生成一个相同的条目，但将 'r' 替换为 'l'
    if image_type == 'r':
        mirrored_entry = f"{data_name} {image_number} l\n"
    else:
        mirrored_entry = None  # 对于 'l' 类型的图像，不需要生成镜像条目

    return original_entry, mirrored_entry

def search_image_paths(root_dir):
    image_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
                image_paths.append(os.path.join(root, file))
    return image_paths

def split_train_val(image_paths):
    # 提取图像文件名，并随机打乱
    image_numbers = [os.path.splitext(os.path.basename(image_path))[0] for image_path in image_paths if 'image_02' in image_path]
    # 删除最小和最大的号码
    min_number = min(image_numbers)
    max_number = max(image_numbers)
    image_numbers = [num for num in image_numbers if num != min_number and num != max_number]
    random.shuffle(image_numbers)

    # 根据分割点分割图像路径
    total_images = len(image_numbers) 
    split_point = total_images * 9 // 10  # 按照9：1的比例分割

    # 根据分割点分割图像路径
    train_image_numbers = image_numbers[:split_point]
    val_image_numbers = image_numbers[split_point:]

    train_paths = []
    val_paths = []

    # 用集合跟踪已写入的文件名
    written_names = set()

    for path in image_paths:
        image_number = os.path.splitext(os.path.basename(path))[0]
        if image_number in train_image_numbers:
            if image_number not in written_names:
                train_paths.append(path)
                written_names.add(image_number)
        elif image_number in val_image_numbers:
            if image_number not in written_names:
                val_paths.append(path)
                written_names.add(image_number)

    # 再次打乱图像路径的顺序
    random.shuffle(train_paths)
    random.shuffle(val_paths)

    return train_paths, val_paths

# 設定資料的根目錄路徑
data_root_dir = '/home/cluster/Desktop/3d_eye/test_data'

# 搜尋圖片路徑
image_paths = search_image_paths(data_root_dir)

# 將圖片路徑分成訓練集和驗證集
train_paths, val_paths = split_train_val(image_paths)

# 生成并打乱训练集内容
train_contents = []
for image_path in train_paths:
    original_entry, mirrored_entry = generate_txt_content(image_path, data_root_dir)
    train_contents.append(original_entry)
    if mirrored_entry is not None:
        train_contents.append(mirrored_entry)
random.shuffle(train_contents)

# 生成并打乱验证集内容
val_contents = []
for image_path in val_paths:
    original_entry, mirrored_entry = generate_txt_content(image_path, data_root_dir)
    val_contents.append(original_entry)
    if mirrored_entry is not None:
        val_contents.append(mirrored_entry)
random.shuffle(val_contents)

with open('train_files.txt', 'w') as train_file:
    written_entries = set()  # 用于跟踪已写入的条目
    for entry in train_contents:
        if entry not in written_entries:
            train_file.write(entry)
            written_entries.add(entry)

# 将验证集内容写入 val.txt 文件
with open('val_files.txt', 'w') as val_file:
    written_entries = set()  # 用于跟踪已写入的条目
    for entry in val_contents:
        if entry not in written_entries:
            val_file.write(entry)
            written_entries.add(entry)

print("已生成 train.txt 和 val.txt 文件。")

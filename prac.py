# %%

# ocr跑批结果转ocr_tools可干预的格式

import os

def process_files(file_path):
    # 获取文件路径下的所有文件名
    file_names = os.listdir(file_path)
    
    # 创建新的rec_pred_train.txt文件，保存在与file_path同一级目录下
    with open(os.path.join(file_path, 'rec_pred_train.txt'), 'w', encoding='utf-8') as output_file:
        # 遍历所有文件名
        for file_name in file_names:
            # 检查文件是否为txt文本
            if file_name.endswith('.tcm.rtcm'):
                # 获取对应的jpg图片文件名
                jpg_file_name = file_name[:-9]
                
                # 读取txt文本内容
                with open(os.path.join(file_path, file_name), 'r', encoding='utf-8') as txt_file:
                    txt_content = txt_file.read().strip()
                
                # 将数据写入到rec_pred_train.txt文件中
                output_file.write(f"{jpg_file_name},{txt_content}#\n")
    
    # 在file_path目录下创建一个新的空rec_pred_train-fixed.txt文件
    fixed_file_path = os.path.join(file_path, 'rec_pred_train-fixed.txt')
    with open(fixed_file_path, 'w', encoding='utf-8') as fixed_file:
        pass

# 指定文件路径
file_path = '/home/mao/github_repo/PaddleOCR/推理样本存放位置/04/'

# 调用函数处理文件
process_files(file_path)

# %%

# ocr_tools干预结果转PaddleOCR训练格式

import os

def process_txt_file(txt_file_path, output_file_path, parent_path):
    # 读取txt文件
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()
    
    # 处理每一行
    processed_lines = []
    for line in lines:
        # 去除行末的换行符
        line = line.strip()
        
        # 解析每一行,只分割第一个逗号
        img_name, ocr_result = line.split(',', 1)
        ocr_result = ocr_result[:-1]
        
        # 如果ocr_result为"delete",则丢弃该行
        if ocr_result == "delete":
            continue
        
        # 计算图片的相对路径
        img_relative_path = os.path.relpath(os.path.dirname(txt_file_path), parent_path)
        img_relative_path = os.path.join(img_relative_path, img_name)
        
        # 检查图片文件是否存在
        img_full_path = os.path.join(parent_path, img_relative_path)
        if not os.path.isfile(img_full_path):
            print(f"警告: 图片文件不存在,已剔除数据: {img_full_path}")
            continue
        
        # 构建新的行
        new_line = f"{img_relative_path}\t{ocr_result}\n"
        processed_lines.append(new_line)
    
    # 将处理后的结果写入新的txt文件
    with open(output_file_path, 'w') as output_file:
        output_file.writelines(processed_lines)
    
    print(f"处理完成,结果已写入: {output_file_path}")

def process_folder(folder_path, parent_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "index.txt":
                txt_file_path = os.path.join(root, file)
                output_file_path = os.path.join(root, "answer.txt")
                process_txt_file(txt_file_path, output_file_path, parent_path)

# 测试代码
folder_path = "/home/mao/github_repo/PaddleOCR/train_data/rec/20240520-汉字-字母-数字-训练样本汇总/支票各区域子图/"
parent_path = "/home/mao/github_repo/PaddleOCR/train_data/rec/20240520-汉字-字母-数字-训练样本汇总"
process_folder(folder_path, parent_path)
# %%

# 合并多个answer.txt文件到一个文件

import os

def concatenate_txt_files(file_paths, output_path):
    with open(output_path, 'w') as outfile:
        for file_path in file_paths:
            if os.path.isfile(file_path):
                with open(file_path, 'r') as infile:
                    outfile.write(infile.read())
            else:
                print(f"文件不存在: {file_path}")

# 获取所有包含answer.txt的文件夹路径
def get_answer_file_paths(root_dir):
    answer_files = []
    for root, dirs, files in os.walk(root_dir):
        if 'answer.txt' in files:
            answer_files.append(os.path.join(root, 'answer.txt'))
    return answer_files

# 指定根目录路径
root_directory = "/home/mao/github_repo/PaddleOCR/train_data/rec/20240520-汉字-字母-数字-训练样本汇总/支票各区域子图/"

# 获取所有answer.txt文件的路径
txt_files = get_answer_file_paths(root_directory)

# 指定输出文件路径
output_file = os.path.join(root_directory, 'answer.txt')

# 调用函数进行文件合并
concatenate_txt_files(txt_files, output_file)
# %%

import cv2
import os
import glob

# 指定文件路径
base_path = "/home/mao/Downloads/ftp_ocr数据存放/RCTW"
image_folder = os.path.join(base_path, "train_images")
gt_folder = os.path.join(base_path, "train_gts")

# 创建输出文件夹
output_folder = os.path.join(base_path, "output")
os.makedirs(output_folder, exist_ok=True)

# 打开输出文件
output_file = open(os.path.join(output_folder, "ocr_result.txt"), "w")

# 遍历所有图片文件
image_files = glob.glob(os.path.join(image_folder, "*.jpg"))
for image_file in image_files:
    # 读取图片
    image = cv2.imread(image_file)
    
    # 获取对应的标注文件
    gt_file = os.path.join(gt_folder, os.path.splitext(os.path.basename(image_file))[0] + ".txt")
    
    # 读取标注文件
    with open(gt_file, "r") as f:
        lines = f.readlines()
    
    # 遍历标注文件中的每一行
    for i, line in enumerate(lines):
        # 提取坐标信息和文字信息
        try:
            parts = line.strip().split(",")
            coords = list(map(int, parts[:8]))
            text = parts[-1].strip('"')
        except:
            continue
        
        # 判断text中是否出现多次#
        if text.count("#") >= 1:
            continue
        
        # 切割子图
        sub_image = image[coords[1]:coords[5], coords[0]:coords[2]]
        
        # 检查子图是否为空
        if sub_image.size == 0:
            continue

        # 判断子图的高度是否大于宽度
        h, w = sub_image.shape[:2]
        if h > w or h < 15 or w < 15:
            continue
        
        # 生成子图文件名
        sub_image_name = f"{os.path.splitext(os.path.basename(image_file))[0]}_{i}.jpg"
        
        # 保存子图
        cv2.imwrite(os.path.join(output_folder, sub_image_name), sub_image)
        
        # 写入ocr_result.txt文件
        output_file.write(f"{sub_image_name},{text}#\n")

# 关闭输出文件
output_file.close()
# %%

import os
import shutil

def copy_jpg_images_in_shoukuanren(root_path, destination_path):
    jpg_count = 0

    # Ensure destination directory exists
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)

    # Walk through the directory structure
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check if the current directory is named '收款人'
        if os.path.basename(dirpath) == '收款人':
            # Iterate over files in the directory
            for file in filenames:
                if file.lower().endswith('.jpg'):
                    jpg_count += 1
                    src_file_path = os.path.join(dirpath, file)
                    dest_file_path = os.path.join(destination_path, file)
                    shutil.copy2(src_file_path, dest_file_path)
    
    return jpg_count

# Define the root path
root_path = "/home/mao/workspace/yolov5/runs/detect/支票类"
# Define the destination path
destination_path = "/home/mao/workspace/yolov5/runs/detect/04收款人所有子图"

# Copy jpg images and get the count
jpg_image_count = copy_jpg_images_in_shoukuanren(root_path, destination_path)

print(f"Number of jpg images copied to '{destination_path}': {jpg_image_count}")
# %%

import os
import random
import shutil

def split_images_into_folders(src_folder, dest_folder_base, N):
    # 获取源文件夹中的所有jpg文件
    jpg_files = [f for f in os.listdir(src_folder) if f.lower().endswith('.jpg')]
    
    # 打乱文件列表
    random.shuffle(jpg_files)
    
    # 计算每个文件夹中应包含的文件数量
    num_files = len(jpg_files)
    files_per_folder = num_files // N
    remainder = num_files % N
    
    # 创建目标文件夹并将文件分配到这些文件夹中
    for i in range(N):
        dest_folder = os.path.join(dest_folder_base, f'folder_{i+1}')
        os.makedirs(dest_folder, exist_ok=True)
        
        # 计算当前文件夹应包含的文件数量
        if i < remainder:
            current_files_count = files_per_folder + 1
        else:
            current_files_count = files_per_folder
        
        # 获取当前文件夹的文件
        current_files = jpg_files[:current_files_count]
        jpg_files = jpg_files[current_files_count:]
        
        # 移动文件到当前文件夹
        for file_name in current_files:
            src_file = os.path.join(src_folder, file_name)
            dest_file = os.path.join(dest_folder, file_name)
            shutil.move(src_file, dest_file)
            print(f'Moved {file_name} to {dest_folder}')

# 示例用法
src_folder = "/home/mao/Downloads/ftp_ocr数据存放/百度中文场景文字识别技术创新大赛/train_images"
dest_folder_base = "/home/mao/Downloads/ftp_ocr数据存放/百度中文场景文字识别技术创新大赛/train_images"
N = 100  # 将图片分成5个文件夹

split_images_into_folders(src_folder, dest_folder_base, N)
# %%

import os
import shutil

# 输入文件路径
input_file_path = "/home/mao/workspace/yolov5/runs/detect/04收款人/测试集/converted_results-fixed.txt"

# 原始图片文件夹路径
original_images_folder = "/home/mao/Downloads/图片原始文件夹"

# 目标文件夹路径
target_folder = "/home/mao/Downloads/匹配到的图片"

# 确保目标文件夹存在
os.makedirs(target_folder, exist_ok=True)

# 读取输入文件
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 处理每一行
for line in lines:
    # 分割行，获取img_name
    img_name, _ = line.strip().split(',', 1)
    
    # 获取img_name的ID部分
    img_id = img_name.split('_')[0]
    
    # 构造原始图片文件名
    original_img_name = f"{img_id}_*.jpg"
    
    # 找到匹配的图片
    for filename in os.listdir(original_images_folder):
        if filename.startswith(img_id) and filename.endswith('.jpg'):
            # 构造原始图片路径
            original_img_path = os.path.join(original_images_folder, filename)
            
            # 构造目标图片路径
            target_img_path = os.path.join(target_folder, filename)
            
            # 复制文件
            shutil.copyfile(original_img_path, target_img_path)
            print(f"Copied {original_img_path} to {target_img_path}")
            break

print("所有文件处理完毕。")
# %%

def replace_suffix_in_file(input_file, old_suffix, new_suffix):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    updated_lines = []
    
    for line in lines:
        img_name, ocr_result = line.split(',')
        if img_name.endswith(old_suffix):
            img_name = img_name.replace(old_suffix, new_suffix)
        updated_lines.append(f"{img_name},{ocr_result}")
    
    with open(input_file, 'w', encoding='utf-8') as file:
        file.writelines(updated_lines)

input_file = '推理样本存放位置/04/rec_pred_train.txt'
old_suffix = '_04_0.jpg'
new_suffix = '-收款人.jpg'

replace_suffix_in_file(input_file, old_suffix, new_suffix)
# %%


# %%

import unicodedata

def to_halfwidth(s):
    # 将全角字符转换为半角字符
    halfwidth_str = ''.join(unicodedata.normalize('NFKC', char) for char in s)
    # 去除字符串中的空格
    return halfwidth_str.replace(' ', '')

input_file = "/home/mao/Downloads/ftp_ocr数据存放/百度中文场景文字识别技术创新大赛/train.list"
output_file = "/home/mao/Downloads/ftp_ocr数据存放/百度中文场景文字识别技术创新大赛/train_processed.list"

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        parts = line.strip().split('\t')
        if len(parts) == 4:
            img_name = parts[2]
            ocr_result = to_halfwidth(parts[3])
            # 如果ocr_result中包含#，则跳过该行
            if '#' in ocr_result:
                continue
            outfile.write(f"{img_name},{ocr_result}#\n")

print("Processing complete. Output saved to", output_file)


# %%

import os

# 指定目录路径
directory = "/home/mao/Downloads/ftp_ocr数据存放/MTWI-2018/txt_train/"

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    # 检查文件名是否以".jpg.jpg"结尾
    if filename.endswith(".jpg.txt"):
        # 构造旧文件路径和新文件路径
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, filename.replace('.jpg', ''))  # 去掉最后一个".jpg"
        
        # 重命名文件
        os.rename(old_file, new_file)
        print(f"Renamed: {old_file} -> {new_file}")

print("All files have been renamed.")

# %%

import os

# 定义文件路径
txt_file_path = "/home/mao/github_repo/PaddleOCR/train_data/rec/20240520-汉字-字母-数字-训练样本汇总/支票各区域子图/20240507-04收款人/rec_pred_train.txt"
jpg_dir_path = "/home/mao/workspace/yolov5/runs/detect/04收款人所有子图/"
output_file_path = "/home/mao/workspace/yolov5/runs/detect/04收款人所有子图/matched_results.txt"

# 读取txt文件内容
with open(txt_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 创建一个字典来存储ID和OCR结果
id_to_ocr = {}
for line in lines:
    img_name, ocr_result = line.strip().split(',')
    img_id = img_name.split('_')[0]
    id_to_ocr[img_id] = ocr_result

# 遍历jpg目录下的文件，匹配ID并写入新的txt文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for jpg_file in os.listdir(jpg_dir_path):
        if jpg_file.endswith('.jpg'):
            img_id = jpg_file.split('_')[0]
            if img_id in id_to_ocr:
                output_file.write(f"{jpg_file},{id_to_ocr[img_id]}\n")

print("匹配完成，结果已写入", output_file_path)

# %%

import os

# 定义文件路径
txt_file_path = "/home/mao/github_repo/PaddleOCR/train_data/测试训练/04收款人所有子图/index.txt"
image_directory = os.path.dirname(txt_file_path)

# 读取txt文件中的图片名称
with open(txt_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 提取图片名称
img_names_in_txt = set()
for line in lines:
    img_name = line.split(',')[0]
    img_names_in_txt.add(img_name)

# 获取目录下所有jpg图片
all_jpg_images = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]

# 检查并删除未出现在txt文件中的jpg图片
for img in all_jpg_images:
    if img not in img_names_in_txt:
        img_path = os.path.join(image_directory, img)
        os.remove(img_path)
        print(f"Deleted: {img_path}")

print("Operation completed.")


# %%

import os
import json
import cv2

# 定义输入txt文件路径和输出目录
input_txt_path = '/home/mao/github_repo/PaddleOCR/checkpoints/det_db/predicts_db.txt'
output_dir = '/home/mao/github_repo/PaddleOCR/推理样本存放位置/1111/subs_2'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 读取txt文件
with open(input_txt_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 处理每一行
for line in lines:
    img_path, det_result = line.strip().split('\t')
    det_result = json.loads(det_result)
    
    # 读取图像
    img = cv2.imread(img_path)
    if img is None:
        print(f"Failed to read image: {img_path}")
        continue
    
    # 获取图像的宽度和高度
    img_height, img_width = img.shape[:2]
    
    # 定义扩展比例
    expand_ratio = 0.001  # 0.01% 的扩展比例
    
    # 裁切并保存子图
    for i, det in enumerate(det_result):
        points = det['points']
        # 获取裁切区域的边界框
        x_min = min(point[0] for point in points)
        x_max = max(point[0] for point in points)
        y_min = min(point[1] for point in points)
        y_max = max(point[1] for point in points)
        
        # 计算扩展后的边界框
        x_min = max(0, int(x_min - img_width * expand_ratio))
        x_max = min(img_width, int(x_max + img_width * expand_ratio))
        y_min = max(0, int(y_min - img_height * expand_ratio))
        y_max = min(img_height, int(y_max + img_height * expand_ratio))
        
        # 裁切子图
        sub_img = img[y_min:y_max, x_min:x_max]
        
        # 构建输出子图的文件名
        base_name = os.path.basename(img_path)
        name, ext = os.path.splitext(base_name)
        sub_img_name = f"{name}_sub_{i}{ext}"
        sub_img_path = os.path.join(output_dir, sub_img_name)
        
        # 保存子图
        cv2.imwrite(sub_img_path, sub_img)
        print(f"Saved sub-image: {sub_img_path}")

# %%

43860/45651*100

#%%

45175/45651*100

#%%

45510/45651*100

#%%

300/10000
# %%

import os
import cv2
import numpy as np

# 定义文件路径
base_path = "/home/mao/Downloads/ftp_ocr数据存放/MTWI-2018"
img_folder = os.path.join(base_path, "img_filter")
txt_folder = os.path.join(base_path, "txt_filter")
output_img_folder = os.path.join(base_path, "output_images")
output_txt_file = os.path.join(base_path, "output.txt")

# 创建输出文件夹
os.makedirs(output_img_folder, exist_ok=True)

# 打开输出txt文件
with open(output_txt_file, 'w', encoding='utf-8') as output_file:
    # 遍历txt文件夹中的每个txt文件
    for txt_filename in os.listdir(txt_folder):
        if txt_filename.endswith('.txt'):
            txt_filepath = os.path.join(txt_folder, txt_filename)
            img_filename = txt_filename.replace('.txt', '.jpg')
            img_filepath = os.path.join(img_folder, img_filename)

            # 读取图像
            img = cv2.imread(img_filepath)
            if img is None:
                print(f"图像文件 {img_filepath} 不存在或无法读取")
                continue

            # 读取txt文件内容
            with open(txt_filepath, 'r', encoding='utf-8') as txt_file:
                for line in txt_file:
                    parts = line.strip().split(',')
                    if len(parts) < 9:
                        print(f"文件 {txt_filepath} 中的行格式不正确: {line}")
                        continue

                    # 提取坐标和文本
                    x1, y1, x2, y2, x3, y3, x4, y4, text = float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7]), parts[8]

                    # 计算外接矩形
                    pts = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                    rect = cv2.boundingRect(cv2.convexHull(np.array(pts, dtype=np.float32)))

                    # 裁剪子图
                    x, y, w, h = rect
                    sub_img = img[y:y+h, x:x+w]
                    
                    try:
                        # 保存子图
                        sub_img_name = f"{os.path.splitext(img_filename)[0]}_{x}_{y}.jpg"
                        sub_img_path = os.path.join(output_img_folder, sub_img_name)
                        cv2.imwrite(sub_img_path, sub_img)

                        # 写入输出txt文件
                        output_file.write(f"{sub_img_name},{text}#\n")
                    except:
                        pass

print("处理完成")

# %%

import os
import shutil

# 指定要处理的根目录
base_path = "/home/mao/github_repo/PaddleOCR/推理样本存放位置/sub_imgs-不带水印"

# 遍历目录中的所有文件
for filename in os.listdir(base_path):
    # 确保处理的是.jpg文件
    if filename.endswith('.jpg'):
        # 提取类名，这里假设文件名格式为 "img20240524_10371586-yinjianleixing.jpg"
        parts = filename.split('-')
        if len(parts) > 1:
            # 类名是最后一个'-'后面的部分，但要去掉'.jpg'
            class_name = parts[-1].split('.')[0]
            
            # 创建目标目录路径
            target_dir = os.path.join(base_path, class_name)
            
            # 如果目标目录不存在，则创建它
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            # 构建源文件的完整路径
            source_path = os.path.join(base_path, filename)
            
            # 构建目标文件的完整路径
            target_path = os.path.join(target_dir, filename)
            
            # 移动文件
            shutil.move(source_path, target_path)
            print(f"Moved {filename} to {target_path}")
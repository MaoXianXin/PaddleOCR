# %%

import os
import shutil

# 定义源文件路径和目标目录
source_file_path = "/home/mao/workspace/PaddleOCR/test_data/Date_sub_imgs/fixed_converted_results.txt"
target_directory = "/home/mao/workspace/PaddleOCR/test_data/fixed_Date_sub_imgs_20240829/"  # 请替换为你的目标目录

# 确保目标目录存在，如果不存在则创建
os.makedirs(target_directory, exist_ok=True)

# 读取文件并处理每一行
with open(source_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 去掉行末的换行符，并分割img_name和ocr_result
        img_name, _ = line.strip().split('\t')
        
        # 构造完整的图像路径
        img_path = os.path.join(os.path.dirname(source_file_path), img_name)
        
        # 检查文件是否存在
        if os.path.isfile(img_path):
            # 复制文件到目标目录
            shutil.move(img_path, target_directory)
            print(f"已复制: {img_name} 到 {target_directory}")
        else:
            print(f"文件不存在: {img_path}")

print("所有文件处理完成。")

# %%

import json
import os
from PIL import Image

def crop_image_from_json(json_file, images_dir, output_dir, target_names, width_expand_ratio=0.1, height_expand_ratio=0.1):
    # 读取 JSON 文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取图片文件名
    image_name = data['fileName'] + ".jpg"  # 假设图片为jpg格式
    image_path = os.path.join(images_dir, image_name)
    
    if not os.path.exists(image_path):
        print(f"Image {image_path} does not exist!")
        return
    
    # 打开图片
    image = Image.open(image_path)
    img_width, img_height = image.size

    # 处理目标字段
    for item in data['db_datas_ocr']:
        item_name = item['name'].strip().lower()
        
        if item_name in target_names:
            # 获取text_region的四个点
            text_region = item['text_region']
            
            # Check if text_region is not empty
            if not text_region:
                print(f"No points found in text_region for {item_name} in {json_file}")
                continue
            
            # 计算裁剪区域的边界框
            x_min = min([point[0] for point in text_region])
            y_min = min([point[1] for point in text_region])
            x_max = max([point[0] for point in text_region])
            y_max = max([point[1] for point in text_region])
            
            # 计算文本框的宽度和高度
            box_width = x_max - x_min
            box_height = y_max - y_min
            
            # 分别按比例外扩宽度和高度
            x_min = max(0, int(x_min - box_width * width_expand_ratio))
            x_max = min(img_width, int(x_max + box_width * width_expand_ratio))
            y_min = max(0, int(y_min - box_height * height_expand_ratio))
            y_max = min(img_height, int(y_max + box_height * height_expand_ratio))
            
            # 裁剪图像
            cropped_image = image.crop((x_min, y_min, x_max, y_max))
            
            # 保存裁剪后的图像
            output_image_path = os.path.join(output_dir, f"{data['fileName']}_{item_name}.jpg")
            cropped_image.save(output_image_path)
            print(f"Cropped image for {item_name} saved to {output_image_path}")
    
    print(f"Processing of {json_file} completed.")

def process_all_json_files(json_dir, images_dir, output_dir, target_names, width_expand_ratio=0.1, height_expand_ratio=0.1):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取目录下所有的 JSON 文件
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    for json_file in json_files:
        json_path = os.path.join(json_dir, json_file)
        print(f"Processing {json_file}...")
        crop_image_from_json(json_path, images_dir, output_dir, target_names, width_expand_ratio, height_expand_ratio)

# 示例用法
json_dir = '/home/mao/Downloads/随机抽样样本结构化结果'       # JSON文件所在目录
images_dir = '/home/mao/workspace/PaddleOCR/test_data/随机抽样样本汇总'        # 原始图像所在目录
output_dir = '/home/mao/workspace/PaddleOCR/test_data/Target_sub_imgs'  # 裁剪后图像的保存目录

# 目标字段名称列表
target_names = ['dateofissue', 'dateofexpiry', 'dateofbirth']

# 设置宽度和高度的扩展比例
width_expand_ratio = 0.03
height_expand_ratio = 0.1

process_all_json_files(json_dir, images_dir, output_dir, target_names, width_expand_ratio, height_expand_ratio)

# %%

import re

def process_and_filter_ocr_results(input_file, corpus_output_file):
    # 使用正则表达式来匹配合法字符
    def is_valid_ocr_result(ocr):
        return re.fullmatch(r"[A-Za-z0-9/\- '<.,]+", ocr) is not None

    written_ocr_results = set()  # 创建一个集合用于存储已经写入的OCR结果

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(corpus_output_file, 'w', encoding='utf-8') as corpus_outfile:
        
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                image_name, ocr_result = parts
                # 去除ocr_result的首尾空格
                ocr_result = ocr_result.strip()
                # 将两个以上的连续空格替换为一个空格
                ocr_result = re.sub(r'\s{2,}', ' ', ocr_result)
                if is_valid_ocr_result(ocr_result) and ocr_result not in written_ocr_results:
                    # 如果OCR结果有效且未写入过，则写入并添加到集合中
                    corpus_outfile.write(ocr_result + '\n')
                    written_ocr_results.add(ocr_result)

# 原始输入文件路径
input_file_path = '/home/mao/workspace/PaddleOCR/output/rec/converted_results.txt'
# 仅包含OCR结果的输出文件路径
corpus_output_file_path = '/home/mao/workspace/PaddleOCR/test_data/corpus_Name.txt'

# 调用函数，执行过滤和写文件操作
process_and_filter_ocr_results(input_file_path, corpus_output_file_path)


# %%

from collections import defaultdict

def read_filter_file(filter_file):
    filter_set = set()
    with open(filter_file, 'r') as f:
        for line in f:
            _, ocr_result = line.strip().split('\t')
            filter_set.add(ocr_result)
    return filter_set

# 读取过滤文件
filter_file = '/home/mao/workspace/PaddleOCR/test_data/fixed_Date_sub_imgs_20240829/index.txt'  # 替换为您的过滤文件名
filter_set = read_filter_file(filter_file)

# 创建一个字典来存储唯一的 OCR 结果
unique_ocr_results = defaultdict(list)

# 读取输入文件
input_file = '/home/mao/workspace/PaddleOCR/test_data/Date_sub_imgs/converted_results.txt'  # 替换为您的输入文件名
output_file = '/home/mao/workspace/PaddleOCR/test_data/Date_sub_imgs/converted_results-0.txt'  # 输出文件名

with open(input_file, 'r') as f:
    for line in f:
        # 分割每行为图片名和 OCR 结果
        img_name, ocr_result = line.strip().split('\t')
        # 将图片名添加到对应的 OCR 结果列表中
        unique_ocr_results[ocr_result].append(img_name)

# 写入结果到输出文件，同时应用过滤
with open(output_file, 'w') as f:
    for ocr_result, img_names in unique_ocr_results.items():
        # 如果 OCR 结果不在过滤集合中，则写入文件
        if ocr_result not in filter_set:
            # 只取第一个图片名（可以根据需要修改选择逻辑）
            f.write(f"{img_names[0]}\t{ocr_result}\n")

print(f"去重和过滤完成。结果已保存到 {output_file}")

# %%

# 定义输入和输出文件名
input_file = 'input.txt'
output_file = 'output.txt'

# 打开输入文件和输出文件
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    # 逐行读取输入文件
    for line in infile:
        # 使用制表符分割每行
        parts = line.strip().split('\t')
        
        # 检查是否有至少两个部分（文件名和OCR结果）
        if len(parts) >= 2:
            # 检查OCR结果是否包含 '/'
            if '/' in parts[1]:
                # 如果包含 '/'，则将整行写入输出文件
                outfile.write(line)

print(f"过滤完成。结果已保存到 {output_file}")

#%%


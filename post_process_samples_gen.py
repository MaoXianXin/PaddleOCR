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
        
        # 解析每一行,只分割第一个\t
        img_name, ocr_result = line.split('\t', 1)
        
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
folder_path = "/home/mao/workspace/PaddleOCR/train_data/rec/训练样本汇总"
parent_path = "/home/mao/workspace/PaddleOCR/train_data/rec/训练样本汇总"
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
root_directory = "/home/mao/workspace/PaddleOCR/train_data/rec/训练样本汇总"

# 获取所有answer.txt文件的路径
txt_files = get_answer_file_paths(root_directory)

# 指定输出文件路径
output_file = os.path.join(root_directory, 'generated_sub_imgs.txt')

# 调用函数进行文件合并
concatenate_txt_files(txt_files, output_file)
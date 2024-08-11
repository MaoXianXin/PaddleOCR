import re
import os

def process_and_filter_ocr_results(input_file, filtered_output_file, corpus_output_file):
    # 使用正则表达式来匹配只包含A-Z, 0-9, 和 '<' 的字符串
    def is_valid_ocr_result(ocr):
        return re.fullmatch(r'[A-Z0-9<]+', ocr) is not None

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(filtered_output_file, 'w', encoding='utf-8') as filtered_outfile, \
         open(corpus_output_file, 'w', encoding='utf-8') as corpus_outfile:
        
        for line in infile:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                image_path, ocr_result = parts
                image_name = os.path.basename(image_path)  # 提取文件名
                if is_valid_ocr_result(ocr_result):
                    # 将image_name和ocr_result按照新格式写入filtered_ocr_results.txt
                    filtered_outfile.write(f'{image_name},{ocr_result}#\n')
                    # 只写入OCR结果部分到corpus_1.txt
                    corpus_outfile.write(ocr_result + '\n')

# 原始输入文件路径
input_file_path = '/home/mao/workspace/PaddleOCR/test_data/ocr_results.txt'
# 过滤后的输出文件路径
filtered_output_file_path = '/home/mao/workspace/PaddleOCR/test_data/filtered_ocr_results.txt'
# 仅包含OCR结果的输出文件路径
corpus_output_file_path = '/home/mao/workspace/PaddleOCR/test_data/corpus_1.txt'

# 调用函数，执行过滤和写文件操作
process_and_filter_ocr_results(input_file_path, filtered_output_file_path, corpus_output_file_path)

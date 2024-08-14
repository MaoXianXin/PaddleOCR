import random

def split_string(input_string, min_len=5, max_len=10):
    substrings = []
    remaining_string = input_string.strip()  # 去掉字符串首尾的空白字符
    
    while len(remaining_string) >= min_len:
        length = random.randint(min_len, min(max_len, len(remaining_string)))
        substring = remaining_string[:length].strip()  # 去掉子串首尾的空白字符
        
        if substring not in substrings:
            substrings.append(substring)
        
        remaining_string = remaining_string[length:].strip()  # 去掉剩余字符串首尾的空白字符
    
    if remaining_string and remaining_string not in substrings:
        substrings.append(remaining_string)
    
    return substrings

def process_file(input_filename, output_filename, min_len=5, max_len=10):
    all_substrings = set()  # 使用集合来自动避免重复子串
    
    with open(input_filename, "r", encoding="utf-8") as infile:
        lines = infile.readlines()  # 读取所有行
        random.shuffle(lines)  # 对行进行打乱

        for line in lines:
            # 对文件中的每一行（即每个字符串）进行切分
            substrings = split_string(line, min_len, max_len)
            all_substrings.update(substrings)
    
    # 将结果写入输出文件
    with open(output_filename, "w", encoding="utf-8") as outfile:
        for substring in all_substrings:
            outfile.write(substring + "\n")

# 示例使用
input_filename = "/home/mao/workspace/PaddleOCR/test_data/corpus_Name.txt"  # 输入文件名
output_filename = "/home/mao/workspace/PaddleOCR/test_data/split_corpus.txt"  # 输出文件名
min_len = 1  # 用户自定义的最小子串长度
max_len = 10  # 用户自定义的最大子串长度

process_file(input_filename, output_filename, min_len, max_len)
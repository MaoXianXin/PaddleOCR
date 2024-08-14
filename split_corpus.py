import random

# 我们使用random模块来生成随机的子串长度和起始位置
INPUT_FILE = "/home/mao/workspace/PaddleOCR/test_data/corpus_MRZ.txt"  # 输入文件名
OUTPUT_FILE = "/home/mao/workspace/PaddleOCR/test_data/split_corpus.txt"  # 输出文件名
STRING_LENGTH = 44  # 每个字符串的预期长度
MIN_SUBSTRING_LENGTH = 15  # 最小子串长度
MAX_SUBSTRING_LENGTH = 24  # 最大子串长度

def get_random_substrings(string, existing_substrings):
    """
    从给定的字符串中随机提取子串，并确保不重复
    """
    substrings = []
    remaining = string
    while len(remaining) >= MIN_SUBSTRING_LENGTH:  # 确保剩余字符串足够长
        length = random.randint(MIN_SUBSTRING_LENGTH, min(MAX_SUBSTRING_LENGTH, len(remaining)))
        substring = remaining[:length]
        remaining = remaining[length:]
        if substring not in existing_substrings:
            substrings.append(substring)
            existing_substrings.add(substring)
    return substrings

def main():
    existing_substrings = set()  # 用于跟踪已写入的子串

    # 读取文件内容并进行shuffle
    with open(INPUT_FILE, 'r') as infile:
        lines = infile.readlines()
    
    random.shuffle(lines)  # shuffle the lines

    with open(OUTPUT_FILE, 'w') as outfile:
        for line_number, line in enumerate(lines, 1):
            line = line.strip()  # 移除行末的换行符
            if len(line) != STRING_LENGTH:
                print(f"警告: 第 {line_number} 行的字符串长度不是 {STRING_LENGTH}。跳过此行。")
                continue
            
            substrings = get_random_substrings(line, existing_substrings)
            for substring in substrings:
                outfile.write(substring + '\n')

    print(f"处理完成。结果已保存到 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
import os

def convert_predictions(input_file, output_file):
    # 读取predicts_ppocrv3.txt文件
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 创建一个新的文件用于写入转换后的结果
    with open(output_file, 'w', encoding='utf-8') as output_file:
        for line in lines:
            # 去除行首尾的空格和换行符
            line = line.strip()
            
            # 按空格分割每一行
            parts = line.split()
            
            # 提取所需的信息
            image_path = parts[0]
            ocr_result = parts[1]
            
            # 提取图片文件名
            image_name = os.path.basename(image_path)
            
            # 构建转换后的行
            converted_line = f"{image_name},{ocr_result}#\n"
            
            # 将转换后的行写入新文件
            output_file.write(converted_line)

    print("转换完成。结果已保存在converted_results.txt文件中。")

def lcs(X, Y):
    m = len(X)
    n = len(Y)
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    lcs.reverse()
    return ''.join(lcs)

def calculate_accuracy(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    
    lines1_dict = {line.split(',')[0]: line.strip() for line in lines1}
    lines2_dict = {line.split(',')[0]: line.strip() for line in lines2}
    
    total_samples = len(lines1_dict)
    correct_samples = 0
    total_chars = 0
    correct_chars = 0
    
    for image_name, line1 in lines1_dict.items():
        if image_name not in lines2_dict:
            total_samples -= 1
            continue
        
        line2 = lines2_dict[image_name]
        try:
            _, result1 = line1.split(',')
            _, result2 = line2.split(',')
        except:
            print(line1)
            print(line2)
        
        result1 = result1.rstrip('#')
        result2 = result2.rstrip('#')
        
        if result2 == 'delete':
            total_samples -= 1
            continue
        
        if result1 == result2:
            correct_samples += 1
        
        total_chars += len(result2)
        correct_chars += len(lcs(result1, result2))
    
    sample_accuracy = correct_samples / total_samples if total_samples > 0 else 0
    char_accuracy = correct_chars / total_chars if total_chars > 0 else 0
    
    return sample_accuracy, char_accuracy

# 指定文件路径
input_file = './output/rec/predicts_ppocrv3.txt'
output_file = './output/rec/converted_results.txt'
correct_file = '/home/mao/workspace/PaddleOCR/test_data/fixed_MRZ_sub_imgs/fixed_ocr_result.txt'

# 转换预测结果
convert_predictions(input_file, output_file)

# 计算准确率
sample_accuracy, char_accuracy = calculate_accuracy(output_file, correct_file)
print(f"样本级准确率: {sample_accuracy:.4f}")
print(f"字符级准确率: {char_accuracy:.4f}")

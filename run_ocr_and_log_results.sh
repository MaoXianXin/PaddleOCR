#!/bin/bash

# 定义根目录变量
BASE_DIR="./推理样本存放位置/sub_imgs-不带水印"

# 输出结果文件
RESULT_FILE="ocr_accuracy_results.txt"

# 初始化或清空结果文件
echo "Directory, Sample Accuracy, Character Accuracy, Sample Count" > $RESULT_FILE

# 列出所有子目录和文件
directories=$(ls $BASE_DIR)

# 迭代每个子目录
for dir in $directories; do
    # 检查是否为目录
    if [ -d "$BASE_DIR/$dir" ]; then
        echo "Processing directory: $dir"

        # 统计该目录下的jpg文件数量
        sample_count=$(find "$BASE_DIR/$dir" -name '*.jpg' | wc -l)

        # 执行 OCR 推理
        python3 tools/infer_rec.py \
          -c configs/rec/PP-OCRv4/ch_PP-OCRv4_rec_hgnet.yml \
          -o Global.infer_img="$BASE_DIR/$dir" \
             Global.pretrained_model="./output/rec_ppocr_v4_hgnet/latest"

        # 计算准确率并捕获输出
        output=$(python3 ocr_accuracy_calculator.py)

        # 从输出中提取样本级和字符级准确率
        sample_accuracy=$(echo "$output" | grep '样本级准确率' | grep -o -E '[0-9]+\.[0-9]+')
        char_accuracy=$(echo "$output" | grep '字符级准确率' | grep -o -E '[0-9]+\.[0-9]+')

        # 写入结果到文件
        echo "$dir, $sample_accuracy, $char_accuracy, $sample_count" >> $RESULT_FILE

        echo "--------------------------------"
    fi
done

# 输出全部完成
echo "All directories processed. Results are saved in $RESULT_FILE."
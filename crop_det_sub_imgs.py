import os
import json
from PIL import Image

def crop_images(image_dir, ocr_result_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(ocr_result_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 2:
                continue
            
            image_name, bounding_boxes = parts
            image_path = os.path.join(image_dir, image_name)
            
            if not os.path.exists(image_path):
                print(f"Image not found: {image_path}")
                continue
            
            try:
                img = Image.open(image_path)
            except Exception as e:
                print(f"Error opening image {image_path}: {e}")
                continue
            
            try:
                boxes = json.loads(bounding_boxes.replace("'", '"'))
            except json.JSONDecodeError:
                print(f"Error parsing bounding boxes for {image_name}")
                continue
            
            for i, box in enumerate(boxes):
                try:
                    left = min(point[0] for point in box)
                    top = min(point[1] for point in box)
                    right = max(point[0] for point in box)
                    bottom = max(point[1] for point in box)
                    
                    width = right - left
                    height = bottom - top
                    
                    # 检查宽高比是否大于30
                    if width / height > 20:
                        cropped_img = img.crop((left, top, right, bottom))
                        
                        output_filename = f"{os.path.splitext(image_name)[0]}_{i}.jpg"
                        output_path = os.path.join(output_dir, output_filename)
                        cropped_img.save(output_path)
                        print(f"Cropped and saved: {output_filename}")
                    else:
                        print(f"Skipped {image_name} box {i}: width/height ratio not > 30")
                except Exception as e:
                    print(f"Error processing {image_name}, box {i}: {e}")

    print("Cropping completed.")

# 使用示例
image_dir = "/home/mao/workspace/PaddleOCR/test_data/随机抽样样本汇总"
ocr_result_file = "/home/mao/workspace/PaddleOCR/inference_results/det_results.txt"
output_dir = "/home/mao/workspace/PaddleOCR/inference_results_sub_imgs"

crop_images(image_dir, ocr_result_file, output_dir)
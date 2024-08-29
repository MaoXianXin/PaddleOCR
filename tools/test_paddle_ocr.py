import requests
import json
import base64
import cv2
import os

OCR_URL_WD = "http://192.168.1.15:12343/predict/ocr_rec_vis"

def getOcrDatasWithRec(images):
    data = {"images": []}
    for img in images:
        imgData = cv2.imencode('.jpg', img)[1]
        imgStr  = str(base64.b64encode(imgData))[2:-1]
        data['images'].append(imgStr)

    headers = {"content-type": "application/json"}
    response = requests.post(OCR_URL_WD, data=json.dumps(data), headers=headers)
    ocrDatas = []
    if response:
        rsp_data = response.json()
        results = rsp_data['results']
        print(results)
        if len(results) > 0:
            id = 0
            for result in results:
                for line in result:
                    id = id + 1
                    data = {'id': id, 'text': line['text']}
                    ocrDatas.append(data)
        else:
            print('返回的数据异常？', results)
    else:
        print("错误了")

    return ocrDatas

def process_images_in_directory(directory_path):
    output_file = "ocr_results.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for filename in os.listdir(directory_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                img_path = os.path.join(directory_path, filename)
                img = cv2.imread(img_path)
                
                if img is None:
                    print(f"无法读取图片: {img_path}")
                    continue
                
                ocrDatas = getOcrDatasWithRec([img])
                
                result_str = "\n".join([data['text'] for data in ocrDatas])
                f.write(f"{filename}\t{result_str}\n")
                
                print(f"处理完成: {filename}")

    print(f"所有结果已写入 {output_file}")

# 使用示例
directory_path = "/home/mao/Pictures/Date-20240829/generated_sub_imgs/"
process_images_in_directory(directory_path)

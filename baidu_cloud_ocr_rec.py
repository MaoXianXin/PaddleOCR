import base64
import urllib
import requests
import os

API_KEY = "pCMWAHmMdHozx1NVlAqXFG3a"
SECRET_KEY = "ETlW8NUvQzq9Be9QIIZrYprjz1b0yN8W"

def main(folder_path, output_directory):
    # 确保输出目录存在，如果不存在则创建
    os.makedirs(output_directory, exist_ok=True)

    # 输出文件路径
    output_file = os.path.join(output_directory, 'ocr_results.txt')
    
    # 打开文件以写入结果
    with open(output_file, 'w', encoding='utf-8') as f:
        # 遍历文件夹中的所有 jpg 文件
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.jpg'):
                image_path = os.path.join(folder_path, filename)
                ocr_result = recognize_image(image_path)
                
                # 检查 OCR 结果的长度
                if len(ocr_result) == 44:
                    # 写入结果到文件
                    f.write(f"{image_path}\t{ocr_result}\n")
                    print(f"Processed: {image_path} -> {ocr_result}")
                else:
                    print(f"Skipped: {image_path} -> Result length is not 44 (length: {len(ocr_result)})")

def recognize_image(image_path):
    # url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + get_access_token()
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + get_access_token()
    
    # 获取图像的 base64 编码
    image_base64 = get_file_content_as_base64(image_path, True)
    
    # 构建 payload
    payload = f'image={image_base64}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.post(url, headers=headers, data=payload)
    
    # 解析并返回 OCR 结果
    if response.status_code == 200:
        try:
            result_json = response.json()
            words = result_json.get("words_result", [{}])[0].get("words", "No result")
            return words
        except Exception as e:
            print(f"Error parsing result for {image_path}: {e}")
            return "Error"
    else:
        print(f"Failed to get result for {image_path}: {response.status_code} {response.text}")
        return "Request failed"

def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

if __name__ == '__main__':
    # 传入包含图片的文件夹路径和输出结果的目录
    input_folder = "/home/mao/workspace/PaddleOCR/inference_results_sub_imgs/"  # 请替换为您的图片文件夹路径
    output_directory = "./"  # 请替换为您想要输出结果的目录
    main(input_folder, output_directory)
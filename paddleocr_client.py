# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import requests
import json
import base64
import os

from PIL import ImageDraw,Image

#~ import argparse

#~ parser = argparse.ArgumentParser(description="args for paddleserving")
#~ parser.add_argument("--image_dir", type=str, default="../../doc/imgs/")
#~ args = parser.parse_args()

'''
def cv2_to_base64(image):
    return base64.b64encode(image).decode('utf8')

url = "http://192.168.30.218:9998/ocr/prediction"

test_img_dir = args.image_dir

for idx, img_file in enumerate(os.listdir(test_img_dir)):
    with open(os.path.join(test_img_dir, img_file), 'rb') as file:
        image_data1 = file.read()
    # print file name
    print('{}{}{}'.format('*' * 10, img_file, '*' * 10))

    image = cv2_to_base64(image_data1)
    
    data = {"key": ["image"], "value": [image]}
    print("to requests")
    r = requests.post(url=url, data=json.dumps(data))
    print("recieve:", r)
    result = r.json()
    print("erro_no:{}, err_msg:{}".format(result["err_no"], result["err_msg"]))
    # check success
    if result["err_no"] == 0:
        ocr_result = result["value"][0]
        try:
            for item in eval(ocr_result):
                # return transcription and points
                print("{}, {}".format(item[0], item[1]))
        except Exception as e:
            print("No results")
            #continue
    else:
        print(
            "For details about error message, see PipelineServingLogs/pipeline.log"
        )

print("==> total number of test imgs: ", len(os.listdir(test_img_dir)))
'''

#~ 

def til_paddleocr_recog(imgDataBase64, url):
    headers = {"Content-type": "application/json"}
    data = {'images': [imgDataBase64]}
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    result = r.json()
    print("show res")
    print(result)
    
    recogRstList = []
    if result["status"] == "000":
        for item in result["results"][0]:
            confidence = item["confidence"]
            text = item["text"]
            addone = [confidence, text]
            recogRstList.append(addone)
    else:
        print("Error occurred. For details, see the 'msg' field in the response.")
        
    return recogRstList

def cv2_to_base64(image):
    return base64.b64encode(image).decode('utf8')

def write_recog_rst(img_file, rJson, outPath):
	with open(outPath, "a") as file:
		for oneR in rJson:
			print(type(oneR))
			print(oneR)	# ['91320192797102273P', 0.99496907, 19.0, 14.0, 595.0, 57.0, 588.0, 94.0, 12.0, 51.0]
			#~ input(1)

def draw_area(imgpath, imgfile, outpath, recogRstList):
	img = Image.open(imgpath+'/'+imgfile)
	w = img.size[0]
	h = img.size[1]
	draw = ImageDraw.Draw(img)
	for oneR in recogRstList:
		[strone, rate, p0,p1,p2,p3,p4, p5, p6, p7] = oneR
		draw.polygon([p0,p1,p2,p3,p4, p5, p6, p7], fill=None, outline=(255,0,0))
		#~ draw.rectangle([xminl,yminl,xmaxl,ymaxl], outline=color[0],width=2)
	img.save(os.path.join(outpath, imgfile[:-4]+'-res.jpg'))
	
	
	
		
if __name__ == '__main__':
	url = "http://192.168.30.218:12345/predict/ocr_rec"
	#~ url = "http://192.168.50.73:9999/ocr/prediction"
	test_img_dir = "/home/mao/github_repo/PaddleOCR/doc/imgs_words/ch"
	outpath = "/home/mao/github_repo/PaddleOCR/hubserving_result"
	#~ test_img_dir = "../python/vat/5/"
	files = os.listdir(test_img_dir)
	files.sort()
	for idx, img_file in enumerate(files):
		print(os.path.join(test_img_dir, img_file))
		with open(os.path.join(test_img_dir, img_file), "rb") as file:
			image_data1 = file.read()
			image = cv2_to_base64(image_data1)
			recogRstList = til_paddleocr_recog(image, url)
			# draw_area(test_img_dir, img_file, outpath, recogRstList)
			
			#~ img_n = Image.new
			# write_recog_rst(img_file, recogRstList, "./paddleocr_rst.txt")


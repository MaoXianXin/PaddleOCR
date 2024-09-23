#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

# 安装必要的模块
hub install deploy/hubserving/ocr_system
hub install deploy/hubserving/ocr_rec_vis
hub install deploy/hubserving/ocr_rec_vis_gray
hub install deploy/hubserving/ocr_rec_mrz

# 启动服务
nohup hub serving start -c deploy/hubserving/ocr_system/config.json > ocr_system_log.out 2>&1 &
nohup hub serving start -c deploy/hubserving/ocr_rec_vis/config.json > vis_log.out 2>&1 &
nohup hub serving start -c deploy/hubserving/ocr_rec_vis_gray/config.json > vis_gray_log.out 2>&1 &
nohup hub serving start -c deploy/hubserving/ocr_rec_mrz/config.json > mrz_log.out 2>&1 &

echo "所有服务已启动"
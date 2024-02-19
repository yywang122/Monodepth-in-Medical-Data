#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 09:16:25 2024

@author: cluster
"""

import cv2
import pytesseract
import pandas as pd
import numpy as np
import os
from paddleocr import PaddleOCR
import argparse
import re
import time
'''
用ocr 設定 R1=ocr(frame,25,1050,570,30)讀特定位置抓取資訊 item[1][0]
用ocr2必須用 item[2][1]抓資料

'''
def ocr(frame,roi_x,roi_y,roi_width,roi_height):
	roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
	ocr=PaddleOCR(lang='en')
	result = ocr.ocr(roi)
	return result
def ocr2(frame):
	ocr=PaddleOCR(lang='en')
	result = ocr.ocr(frame)
	return result
def mkfile(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path

def split_frame(frame):
    height, width, _ = frame.shape
    split_height = height // 2
    top_half = frame[0:split_height, :]
    bottom_half = frame[split_height:height, :]
    return top_half, bottom_half



path='/home/cluster/Desktop/3d_eye/data/stream1_20230712_170517'
cap = cv2.VideoCapture(path+'.mp4')
frame_count=0
split_frame_count=0
current_frame_labels=[]
#如果沒有上述資料夾就建立資料夾 If no output_dir floder than create one
#mkfile(path)

while(cap.isOpened()):
	
	ret, frame = cap.read()
	
	if not ret:
		break
	if frame_count % 60 == 0:
		mkfile(path)
		
		#所有資訊
		R1=ocr(frame,25,1050,570,30)


	
		# 檢查標籤是否包含 "ANTERIOR"
		if any('ANTERIOR' in item[1][0] for item in R1[0]):
			top_half, bottom_half = split_frame(frame)
			left_dir=mkfile(path+'/ANTERIOR/image02/data')
			right_dir=mkfile(path+'/ANTERIOR/image03/data')
			cv2.imwrite(os.path.join(left_dir, f"{split_frame_count:09d}.jpg"), top_half)
			cv2.imwrite(os.path.join(right_dir, f"{split_frame_count:09d}.jpg"), bottom_half)
			split_frame_count+=1
		
		elif any('POSTERIOR.' in item[1][0] or 'POSTERIOR..' in item[1][0] or 'POSTERIOR...' in item[1][0] for item in R1[0]):
			top_half, bottom_half = split_frame(frame)
			left_dir=mkfile(path+'/POSTERIOR_context/image02/data')
			right_dir=mkfile(path+'/POSTERIOR_context/image03/data')
			cv2.imwrite(os.path.join(left_dir, f"{split_frame_count:09d}.jpg"), top_half)
			cv2.imwrite(os.path.join(right_dir, f"{split_frame_count:09d}.jpg"), bottom_half)
			split_frame_count+=1
		elif any('POSTERIOR' in item[1][0] for item in R1[0]):
			top_half, bottom_half = split_frame(frame)
			left_dir=mkfile(path+'/POSTERIOR/image02/data')
			right_dir=mkfile(path+'/POSTERIOR/image03/data')
			cv2.imwrite(os.path.join(left_dir, f"{split_frame_count:09d}.jpg"), top_half)
			cv2.imwrite(os.path.join(right_dir, f"{split_frame_count:09d}.jpg"), bottom_half)
			split_frame_count+=1
		else:
			top_half, bottom_half = split_frame(frame)
			left_dir=mkfile(path+'/else/image02/data')
			right_dir=mkfile(path+'/else/image03/data')
			cv2.imwrite(os.path.join(left_dir, f"{split_frame_count:09d}.jpg"), top_half)
			cv2.imwrite(os.path.join(right_dir, f"{split_frame_count:09d}.jpg"), bottom_half)
			split_frame_count+=1
	frame_count+=1
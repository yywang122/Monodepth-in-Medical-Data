import cv2
from paddleocr import PaddleOCR
import os
import time

def ocr(frame, roi_x, roi_y, roi_width, roi_height):
    roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    ocr = PaddleOCR(lang='en')
    start_time = time.time()
    result = ocr.ocr(roi)
    end_time = time.time()
    processing_time = end_time - start_time
    print(processing_time)
    return result, processing_time

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

def process_video(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    split_frame_count = 0
    total_ocr_time = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % 60 == 0:
            R1, ocr_time = ocr(frame, 25, 1050, 570, 30)
            total_ocr_time += ocr_time
            if any('ANTERIOR' in item[1][0] for item in R1[0]):
                dir_name = 'ANTERIOR'
            elif any('POSTERIOR.' in item[1][0] or 'POSTERIOR..' in item[1][0] or 'POSTERIOR...' in item[1][0] for item in R1[0]):
                dir_name = 'POSTERIOR_context'
            elif any('POSTERIOR' in item[1][0] for item in R1[0]):
                dir_name = 'POSTERIOR'
            else:
                dir_name = 'else'

            top_half, bottom_half = split_frame(frame)
            left_dir = mkfile(os.path.join(output_dir, dir_name, 'image_02', 'data'))
            right_dir = mkfile(os.path.join(output_dir, dir_name, 'image_03', 'data'))
            cv2.imwrite(os.path.join(left_dir, f"{split_frame_count:010d}.jpg"), top_half)
            cv2.imwrite(os.path.join(right_dir, f"{split_frame_count:010d}.jpg"), bottom_half)
            split_frame_count += 1

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total OCR processing time for {video_path}: {total_ocr_time} seconds")

# 輸入目錄和輸出目錄
input_directory = '/home/cluster/Desktop/3d_eye/test/'
output_directory = '/home/cluster/Desktop/3d_eye/process_data/'

# 遍歷輸入目錄下的所有影片
for root, dirs, files in os.walk(input_directory):
    for filename in files:
        if filename.endswith('.mp4'):
            video_path = os.path.join(root, filename)
            relative_path = os.path.relpath(video_path, input_directory)
            output_path = os.path.join(output_directory, relative_path)
            process_video(video_path, output_path)

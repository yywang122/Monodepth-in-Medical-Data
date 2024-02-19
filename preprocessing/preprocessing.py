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
    return result,processing_time

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

path = '/home/cluster/Desktop/3d_eye/test/stream1_20220727_174248'
cap = cv2.VideoCapture(path + '.mp4')
frame_count = 0
split_frame_count = 0
total_ocr_time=0
mkfile(path)

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % 60 == 0:
        R1, ocr_time = ocr(frame, 25, 1050, 570, 30)
        total_ocr_time+=ocr_time
        if any('ANTERIOR' in item[1][0] for item in R1[0]):
            dir_name = 'ANTERIOR'
        elif any('POSTERIOR.' in item[1][0] or 'POSTERIOR..' in item[1][0] or 'POSTERIOR...' in item[1][0] for item in R1[0]):
            dir_name = 'POSTERIOR_context'
        elif any('POSTERIOR' in item[1][0] for item in R1[0]):
            dir_name = 'POSTERIOR'
        else:
            dir_name = 'else'

        top_half, bottom_half = split_frame(frame)
        left_dir = mkfile(os.path.join(path, dir_name, 'image02', 'data'))
        right_dir = mkfile(os.path.join(path, dir_name, 'image03', 'data'))
        cv2.imwrite(os.path.join(left_dir, f"{split_frame_count:09d}.jpg"), top_half)
        cv2.imwrite(os.path.join(right_dir, f"{split_frame_count:09d}.jpg"), bottom_half)
        split_frame_count += 1

    frame_count += 1

cap.release()
cv2.destroyAllWindows()
print(f"Total OCR processing time: {total_ocr_time} seconds")

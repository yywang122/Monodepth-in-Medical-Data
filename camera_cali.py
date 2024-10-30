import cv2
import numpy as np
import glob


dir_li=['0.4']

name_li=['05','1','2','3']
for dir in dir_li:
    
    print(dir)
    for name in  name_li:
        print('focal')
        print(name)
        objp = np.zeros((5 * 5, 3), np.float32)
        objp[:, :2] = np.mgrid[0:5, 0:5].T.reshape(-1, 2)  
        objp = float(dir) * objp  
        obj_points = []     # 存3D點
        img_points = []     # 存2D點
        images=glob.glob("C:/Users/User/Desktop/camera/1117/ch_y%s/%sx/*.JPEG"%(dir,name))  #黑白棋盘的图片路径
        
        for fname in images:
            print(fname)
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            size = gray.shape[::-1]
            ret, corners = cv2.findChessboardCorners(gray, (5, 5), None)
            if ret:
                obj_points.append(objp)
                corners2 = cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), (cv2.TERM_CRITERIA_MAX_ITER | cv2.TERM_CRITERIA_EPS, 30, 0.001))  
                if [corners2]:
                    img_points.append(corners2)
                else:
                    img_points.append(corners)
                cv2.drawChessboardCorners(img, (5,5), corners, ret) 
                cv2.waitKey(1)
        _, mtx, dist, rotation,translation = cv2.calibrateCamera(obj_points, img_points, size, None, None)
        
        # 内参数矩阵
        Camera_intrinsic = {"mtx": mtx,"dist": dist,"rotation": rotation,"translation": translation,}
        print(Camera_intrinsic)

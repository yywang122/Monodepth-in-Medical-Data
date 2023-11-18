import cv2
import numpy as np
import glob
'''camera = cv2.VideoCapture(0)
i = 1
while i <15:
    _, frame = camera.read()
    cv2.imshow('frame', frame)
    if ord('q'):
        cv2.imwrite("C:/Users/User/Desktop/camera/"+"IMG_40%s"%str(100+i)+'.jpg', frame, [int(cv2.IMWRITE_PNG_COMPRESSION), 0]) 
        
        i += 1
    elif 0xFF == 27: # 按ESC键退出
        break
cv2.destroyAllWindows()
'''


dir_li=['0.4']

name_li=['05','1','2','3']
for dir in dir_li:
    print('=====================================================')
    print(dir)
    for name in  name_li:
        print('~~~~focal~~~')
        print(name)
        objp = np.zeros((5 * 5, 3), np.float32)
        objp[:, :2] = np.mgrid[0:5, 0:5].T.reshape(-1, 2)  # 将世界坐标系建在标定板上，所有点的Z坐标全部为0，所以只需要赋值x和y
        objp = float(dir) * objp   # 打印棋盘格一格的边长为3cm
        obj_points = []     # 存储3D点
        img_points = []     # 存储2D点
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
                cv2.drawChessboardCorners(img, (5,5), corners, ret)  # 记住，OpenCV的绘制函数一般无返回值
                cv2.waitKey(1)
        _, mtx, dist, rotation,translation = cv2.calibrateCamera(obj_points, img_points, size, None, None)
        
        # 内参数矩阵
        Camera_intrinsic = {"mtx": mtx,"dist": dist,"rotation": rotation,"translation": translation,}
        print(Camera_intrinsic)
import numpy as np
import cv2 as cv


def blackScale(image):
    image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    allSize = 1
    # print(image.shape)
    for i in image.shape:
        allSize *= i

    black = len(np.where(image < 150)[0])
    return black / allSize


def get_y(point_list):
    ymin, ymax = 2 ** 30, -2 ** 30
    for i in point_list:
        ymin = min(ymin, i[1])
        ymax = max(ymax, i[1])

    return ymin, ymax


def countBlack(img):
    count = 0
    x1, y1, d1 = img.shape
    for x in range(x1):
        for y in range(y1):
            temp = 0
            for d in range(d1):
                if img.item(x, y, d) < 50:
                    temp += 1
            if temp == 3:
                count += 1
    return count


def getMaxRec(image):
    # 灰度图
    img = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, thresh = cv.threshold(img, 230, 255, cv.THRESH_BINARY_INV)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    dot = []  # 用来保存所有轮廓返回的坐标点。
    for c in contours:
        # 找到边界坐标
        min_list = []  # 保存单个轮廓的信息，x,y,w,h,area。 x,y 为起始点坐标
        x, y, w, h = cv.boundingRect(c)  # 计算点集最外面的矩形边界
        min_list.append(x)
        min_list.append(y)
        min_list.append(w)
        min_list.append(h)
        min_list.append(w * h)  # 把轮廓面积也添加到 dot 中
        dot.append(min_list)

    # 找出最大矩形的 x,y,w,h,area
    max_area = dot[0][4]  # 把第一个矩形面积当作最大矩形面积
    for inlist in dot:
        area = inlist[4]
        if area >= max_area:
            x = inlist[0]
            y = inlist[1]
            w = inlist[2]
            h = inlist[3]
            max_area = area

    return x, y, x + w, y + h


if __name__ == "__main__":
    m = cv.imread('..\\pic\\black.jpg')
    print(countBlack(m))
    # 2695

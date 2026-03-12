import cv2
import numpy as np
import os
from cellpose_based_method import use_cellpose

def devide3(image_path):
    # 读图、灰度化、阈值化
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # 读取图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 将图像转换为灰度
    _, binary_image = cv2.threshold(gray_image, 225, 255, cv2.THRESH_BINARY)  # 阈值化图像，根据实际情况调整阈值
    # cv2.imshow('binary_image', binary_image)
    # cv2.waitKey(0)

    # 预膨胀一次，用于避免大面积细胞间隙联通。
    inverted_image = cv2.bitwise_not(binary_image)  # 将图像黑白反转
    # cv2.imshow('inverted_image', inverted_image)
    # cv2.waitKey(0)
    dilated_image = cv2.dilate(inverted_image, None, iterations=1)  # 膨胀操作
    # cv2.imshow('dilate1', dilated_image)
    # cv2.waitKey(0)
    inverted_image = cv2.bitwise_not(dilated_image)  # 将图像黑白反转
    # cv2.imshow('inverted_image', inverted_image)
    # cv2.waitKey(0)

    # 过滤多余的染料以免膨胀后连通
    contours, _ = cv2.findContours(inverted_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 查找轮廓
    blank_image = np.zeros_like(image)  # 创建空白图像
    for contour in contours:  # 过滤轮廓
        if cv2.contourArea(contour) > 500:
            cv2.fillPoly(blank_image, [contour], (255, 255, 255))  # 绘制填充轮廓
            # cv2.drawContours(blank_image, contour, -1, (0, 255, 0), thickness=2)#绘制轮廓
    # cv2.imshow('devide', blank_image)
    # cv2.waitKey(0)

    # 经行第二次高倍膨胀并收缩
    inverted_image = cv2.bitwise_not(blank_image)  # 将图像黑白反转
    # cv2.imshow('inverted_image', inverted_image)
    # cv2.waitKey(0)
    dilated_image = cv2.dilate(inverted_image, None, iterations=30)  # 膨胀操作，消除小的细胞间隙
    # cv2.imshow('dilate2', dilated_image)
    # cv2.waitKey(0)
    eroded_image = cv2.erode(dilated_image, None, iterations=30)  # 收缩
    # cv2.imshow('erode', eroded_image)
    # cv2.waitKey(0)



    #将原图中的肌束膜掩盖
    gray_image = cv2.cvtColor(eroded_image, cv2.COLOR_BGR2GRAY)  # 将图像转换为灰度
    _, binary_image = cv2.threshold(gray_image, 225, 255, cv2.THRESH_BINARY)
    result_image = cv2.bitwise_and(image, image, mask=binary_image)

    #计算肌束膜面积
    black_pixels = cv2.countNonZero(binary_image)
    cv2.imwrite(r"D:/Users/YFENG/Desktop/test.jpg",result_image)
    cv2.imshow('result_image', result_image)
    cv2.waitKey(0)

    #计算等效半径
    resultar, cell_area, img_area = use_cellpose(result_image)
    eqr = cell_area/resultar
    eqR = (img_area-black_pixels)/resultar
    d = eqR - eqr
    return eqr,eqR,d


if __name__ == '__main__':
    # 示例用法
    image_path = r"D:/Users/YFENG/Desktop/test/080ebfdc193240705ebb48b926bca6e.jpg"
    print(devide3(image_path))


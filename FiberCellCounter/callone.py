# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 22:02:26 2021

@author: Lenovo
"""
import numpy as np
import cv2
import os


def watershed(imgpath, resfilepath, thresholdmode=0, wttype=0, opiter=2, bgiter=3, dis=0, default=30, binary_thresh=127,
              pixel=0.273810):
    np.set_printoptions(threshold=np.inf)
    imgpath = imgpath.replace('\\', os.sep)
    imgpath = imgpath.replace('/', os.sep)
    resfilepath = resfilepath.replace('\\', os.sep)
    resfilepath = resfilepath.replace('/', os.sep)

    # 获得原图像,带后缀名
    img = cv2.imread(imgpath, 1)
    # print(img.shape[0])
    # print(img.shape[1])
    img_area = img.shape[0] * img.shape[1]
    img_heigt = img.shape[0]
    img_width = img.shape[1]
    print(img_area)

    # 将图像转换成灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gray',gray)
    # 通过阈值函数将图像二值化处理
    # 模式0，默认阈值
    if thresholdmode == 0:
        thresh, binary_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # 模式1，自定义阈值
    elif thresholdmode == 1:
        thresh, binary_img = cv2.threshold(gray, binary_thresh, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('binary', binary_img)

    # 形态学开运算（对于空洞采取形态学闭运算）
    kernel = np.ones((10, 10), np.uint8)
    opening = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel, iterations=opiter)
    # 由于细胞图像空洞较多，上面迭代数量不要太大,保证和原图像接近，
    # cv2.imshow('opening', opening)
    # sure background area   膨胀后确保背景
    sure_bg = cv2.dilate(opening, kernel, iterations=bgiter)

    # 腐蚀操作，去除边缘像素，确定前景
    # 第二个参数0,1,2 分别表示CV_DIST_L1, CV_DIST_L2 , CV_DIST_C
    dist_transform = cv2.distanceTransform(opening, 2, 5)  # 距离变换函数
    # 阈值函数确定哪些保留源二值化处理，即确定前景
    ret, sure_fg = cv2.threshold(dist_transform, dis * dist_transform.max(), 255, 0)
    # cv2.imshow('fushi', sure_fg)
    # 通过背景个前景交接处找到边界unknown的区域
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 标记区域
    # 求取连通域
    ret, markers1 = cv2.connectedComponents(sure_fg)
    # 将所有标记加1，以确保背景是1不是0（分水岭处理方法色特征）
    markers = markers1 + 1
    # 未知区域标记为0
    markers[unknown == 255] = 0

    # 修改标签图像，边界区域的标记将变为 -1
    markers3 = cv2.watershed(img, markers)
    img[markers3 == -1] = [255, 255, 0]

    # 根据分水岭结果求取轮廓
    img2 = img.copy()
    # img2 = cv2.imread('Adenanthera_pavonina.jpg',1)
    # 将markers（边界值为-1）数组转换成markers2(边界值为255的数组)
    markers2 = markers3.astype(np.uint8)
    ret, m2 = cv2.threshold(markers2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow('m2', m2)z
    contours, hierarchy = cv2.findContours(m2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # 用加粗标记画出分水岭求取出的边界
    for c in contours:
        cv2.drawContours(img2, c, -1, (0, 255, 0), 2)

    # cv2.imshow('markers2', markers2)
    # cv2.imshow('contours', img2)

    # 根据轮廓结果得出面积和中心坐标
    # 建立空数组，放连通域面积
    # 打开文件，设置为写模式，若没有则直接创建txt文件
    # 判断resfilepath是存储路径还是存储文件名
    name1 = imgpath.split(os.sep)[-1]
    print('name1---->', name1)
    name = name1.split('.')[0]
    print('name--->', name)
    saveFileName = None
    if resfilepath == None:
        resfilepath = imgpath.replace(name1, os.sep + 'results')
    if os.path.isdir(resfilepath):
        saveFileName = resfilepath + os.sep + name
    elif os.path.isfile(resfilepath):
        saveFileName = resfilepath.split('.')[0]
    else:
        # print('存储路径或存储文件名非法，使用result文件名替代')
        # saveFileName = imgpath.replace(name1,'results'+os.sep+'result')
        saveFileName = resfilepath

    file = open(saveFileName + '.txt', mode='w')
    # 检测结果对象名称
    file.write('细胞图像文件名称:' + imgpath + '\n')
    # 检测结果项名
    file.write('纤维细胞id' + '\t' + '横坐标' + '\t' + '纵坐标' + '\t' + '面积um^2' + '\n')

    # 建立空列表，收集结果
    resultar = []
    # 建立空数组，放连通域面积
    area = []
    # 建立空数组，放减去最小面积的数
    contours1 = []
    for i in contours:
        # area.append(cv2.contourArea(i))
        # print(area)
        # 计算面积 去除面积小的 连通域
        if cv2.contourArea(i) > 30 and cv2.contourArea(i) < 0.5 * img.shape[0] * img.shape[1]:
            contours1.append(i)
            area.append(cv2.contourArea(i))
    # 计算连通域个数
    # print(len(contours1)-1)
    # 描绘连通域
    draw = cv2.drawContours(img, contours1, -1, (0, 255, 0), 2)
    # 求连通域重心 以及 在重心坐标点描绘数字
    # 细胞个数
    number = 0
    # 细胞总面积
    total = 0

    # 标注的结果图片
    result = None
    for i, j in zip(contours1, range(len(contours1))):
        M = cv2.moments(i)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # 在中心坐标点上描绘数字
        result = cv2.putText(draw, str(j), (cX, cY), 1, 1, (255, 0, 255), 1)
        # 检测结果以数元组的形式存入列表中
        resultar.append((str(j), str(cX), str(cY), area[j] * pixel))
        number = number + 1
        total = total + area[j]

    # 列表以面积大小排序
    resultar = sorted(resultar, key=lambda x: x[3])
    for i in range(len(resultar)):
        # 将排序后的结果写入文件中
        file.write(
            str(i) + '\t\t' + resultar[i][1] + '\t' + resultar[i][2] + '\t' + str(round((resultar[i][3]), 2)) + '\n')
        # 展示图片
    # cv2.imshow("draw.jpg",result)
    # ave result

    result_ratio = total / img_area * 100
    print(result_ratio)
    cv2.imwrite(saveFileName + '.jpg', result)
    # cv2.imshow('res.jpg',result)
    # cv2.waitKey()
    return thresh, opening, sure_bg, sure_fg, unknown, img, img2, result, number, round(total*pixel*pixel,2), result_ratio, round(img_width*pixel,2), round(img_heigt*pixel,2), round(img_area*pixel*pixel,2)


if __name__ == '__main__':
    imgpath1 = r'D:\testfiles\022 HE_26.1x.jpg'

    wttype = 1
    opiter = 2
    bgiter = 3
    dis = 0
    # usr provide, if not or illegal, give a default value
    resfilepath1 = r'D:\testfilesresult'
    watershed(imgpath1, resfilepath1, 0, 1, 2, 3, 0, 100, 190)

# def watershed(imgpath, resfilepath, thresholdmode=0, wttype=0, opiter=2, bgiter=3, dis=0, default=30, binary_thresh=127):

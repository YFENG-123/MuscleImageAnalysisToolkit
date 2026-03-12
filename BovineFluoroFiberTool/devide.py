import cv2
import numpy as np
import os

from cellpose_based_method import use_cellpose


def devide(image_path, save_folder):
    np.set_printoptions(threshold=np.inf)
    image_path = image_path.replace('\\', os.sep)
    image_path = image_path.replace('/', os.sep)
    save_folder = save_folder.replace('\\', os.sep)
    save_folder = save_folder.replace('/', os.sep)

    rp = os.path.dirname(image_path) + '\\' + os.path.basename(image_path).split('.')[0] + '_r.jpg'
    gp = os.path.dirname(image_path) + '\\' + os.path.basename(image_path).split('.')[0] + '_g.jpg'
    bp = os.path.dirname(image_path) + '\\' + os.path.basename(image_path).split('.')[0] + '_b.jpg'
    pp = os.path.dirname(image_path) + '\\' + os.path.basename(image_path).split('.')[0] + '_p.jpg'

    # 读取图像
    image = cv2.imread(image_path)

    # 转换为HSV颜色空间
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 红色范围
    lower_red1 = np.array([0, 0, 0])
    upper_red1 = np.array([20, 255, 255])
    lower_red2 = np.array([160, 50, 50])
    upper_red2 = np.array([230, 255, 255])

    # 绿色范围
    lower_green = np.array([40, 0, 0])
    upper_green = np.array([80, 255, 255])

    # 蓝色范围
    lower_blue = np.array([110, 45, 45])
    upper_blue = np.array([150, 255, 255])

    # 紫色范围
    lower_purple1 = np.array([130, 0, 0])
    upper_purple1 = np.array([180, 255, 255])
    lower_purple2 = np.array([180, 0, 0])
    upper_purple2 = np.array([255, 255, 255])

    # 提取红色区域
    red_mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # 提取绿色区域
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # 提取蓝色区域
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # 提取紫色区域
    purple_mask1 = cv2.inRange(hsv_image, lower_purple1, upper_purple1)
    purple_mask2 = cv2.inRange(hsv_image, lower_purple2, upper_purple2)
    purple_mask = cv2.bitwise_or(purple_mask1, purple_mask2)




    # 应用红色掩码
    red_result = cv2.bitwise_and(image, image, mask=red_mask)
    #cv2.imshow("red1", red_result)

    # 定义亮度和对比度调整参数
    brightness = 0
    contrast = 3
    # 调整亮度和对比度
    adjusted_image = cv2.convertScaleAbs(red_result, alpha=contrast, beta=brightness)
    #cv2.imshow("red2", adjusted_image)

    gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_RGB2GRAY)
    gray_image += 10
    gray_image[gray_image < 25] = 0
    gray_image[gray_image > 255] = 255

    '''# 定义核（kernel），用于膨胀和收缩操作
    kernel = np.ones((3, 3), np.uint8)
    # 膨胀操作
    dilated_image = cv2.dilate(gray_image, kernel, iterations=3)
    # 收缩操作
    eroded_image = cv2.erode(dilated_image, kernel, iterations=3)
    cv2.imshow("red2.5", eroded_image)'''

    red_result = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
    red_result[:, :, 0] = 255
    red_result[:, :, 1] = 255 - gray_image
    red_result[:, :, 2] = 255
    #cv2.imshow("red3", red_result)




    # 应用绿色掩码
    green_result = cv2.bitwise_and(image, image, mask=green_mask)
    #cv2.imshow("green1", green_result)

    # 定义亮度和对比度调整参数
    brightness = 0
    contrast = 1
    # 调整亮度和对比度
    adjusted_image = cv2.convertScaleAbs(green_result, alpha=contrast, beta=brightness)
    #cv2.imshow("green2", adjusted_image)

    gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_RGB2GRAY)
    gray_image += 50
    gray_image[gray_image < 60] = 0
    gray_image[gray_image > 255] = 255

    # 定义核（kernel），用于膨胀和收缩操作
    kernel = np.ones((3, 3), np.uint8)
    # 膨胀操作
    dilated_image = cv2.dilate(gray_image, kernel, iterations=3)
    # 收缩操作
    eroded_image = cv2.erode(dilated_image, kernel, iterations=3)
    #cv2.imshow("green2.5", eroded_image)

    green_result = cv2.cvtColor(eroded_image, cv2.COLOR_GRAY2RGB)
    green_result[:, :, 0] = 255
    green_result[:, :, 1] = 255 - gray_image
    green_result[:, :, 2] = 255
    #cv2.imshow("green3", green_result)




    # 应用蓝色掩码
    blue_result = cv2.bitwise_and(image, image, mask=blue_mask)
    #cv2.imshow("blue1", blue_result)

    # 定义亮度和对比度调整参数
    brightness = 0
    contrast = 1
    # 调整亮度和对比度
    adjusted_image = cv2.convertScaleAbs(blue_result, alpha=contrast, beta=brightness)
    #cv2.imshow("blue2", adjusted_image)

    gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_RGB2GRAY)
    gray_image += 25
    gray_image[gray_image < 50] = 0
    gray_image[gray_image > 255] = 255

    # 定义核（kernel），用于膨胀和收缩操作
    kernel = np.ones((3, 3), np.uint8)
    # 膨胀操作
    dilated_image = cv2.dilate(gray_image, kernel, iterations=3)
    # 收缩操作
    eroded_image = cv2.erode(dilated_image, kernel, iterations=3)
    #cv2.imshow("blue2.5", eroded_image)

    blue_result = cv2.cvtColor(dilated_image, cv2.COLOR_GRAY2RGB)
    blue_result[:, :, 0] = 255
    blue_result[:, :, 1] = 255 - gray_image
    blue_result[:, :, 2] = 255
    #cv2.imshow("blue3", blue_result)





    # 应用紫色掩码
    purple_result = cv2.bitwise_and(image, image, mask=purple_mask)
    #cv2.imshow("purple1", purple_result)

    # 定义亮度和对比度调整参数
    brightness = 0
    contrast = 2
    # 调整亮度和对比度
    adjusted_image = cv2.convertScaleAbs(purple_result, alpha=contrast, beta=brightness)
    #cv2.imshow("purple2", adjusted_image)

    gray_image = cv2.cvtColor(adjusted_image, cv2.COLOR_RGB2GRAY)

    #cv2.imshow("purple3", gray_image)


    # 定义核（kernel），用于膨胀和收缩操作
    kernel = np.ones((3, 3), np.uint8)

    # 收缩操作
    eroded_image = cv2.erode(gray_image, kernel, iterations=3)
    # 膨胀操作
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=3)
    # cv2.imshow("purple2.5", dilated_image)

    purple_result = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
    purple_result[:, :, 0] = 255
    purple_result[:, :, 1] = 255 - gray_image
    purple_result[:, :, 2] = 255
    cv2.imshow("purple3", purple_result)

    return red_result, rp, green_result, gp, blue_result, bp, purple_result, pp




if __name__ == '__main__':
    # 示例用法
    image_path = r"D:\Users\YFENG\Desktop\1.png"
    save_folder = r"D:\Users\YFENG\Desktop"
    red_result, rp, green_result, gp, blue_result, bp, purple_result, pp = devide(image_path, save_folder)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    use_cellpose(image_path, save_folder, img=purple_result, pixel_size=1)

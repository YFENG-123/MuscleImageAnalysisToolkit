# -*- coding: utf-8 -*-
import numpy as np
import cv2
import os
from cellpose import models
import matplotlib as mpl
from scipy.ndimage import find_objects


def getResults(img0, masks, pixel_size,color=[1, 0, 0]):
    if len(img0.shape) < 3:
        #         img0 = image_to_rgb(img0) broken, transposing some images...
        img0 = np.stack([img0] * 3, axis=-1)

    if masks.ndim > 3 or masks.ndim < 2:
        raise ValueError('masks_to_outlines takes 2D or 3D array, not %dD array' % masks.ndim)
    outlines = np.zeros(masks.shape, bool)
    # 面积，周长，等效半径
    resultar = []
    slices = find_objects(masks.astype(int))
    area = 0
    for i, si in enumerate(slices):
        if si is not None:
            sr, sc = si
            mask = (masks[sr, sc] == (i + 1)).astype(np.uint8)
            contour = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            pvc, pvr = np.concatenate(contour[-2], axis=0).squeeze().T
            vr, vc = pvr + sr.start, pvc + sc.start
            outlines[vr, vc] = 1
            mask_list = np.array(mask).flatten().tolist()
            for j in mask_list:
                if j == 1:
                    area = area + 1
            # 面积，周长，等效半径
            area = round(area * pixel_size * pixel_size, 2)
            length = round(np.size(vr) * pixel_size, 2)
            r = np.sqrt(float(area) / 3.1415)
            r = round(r, 2)
            resultar.append((area, length, r))
            resultar = sorted(resultar, key=lambda x: x[0])
            area = 0
    outY, outX = np.nonzero(outlines)
    imag_with_boundaries = img0.copy()
    #     imgout[outY, outX] = np.array([255,0,0]) #pure red
    imag_with_boundaries[outY, outX] = np.array(color)

    return imag_with_boundaries, resultar


def use_cellpose(img, pixel_size=10.0):
    print(img.shape[0])
    print(img.shape[1])
    img_area = img.shape[0] * img.shape[1]
    img_area = round(img_area * pixel_size * pixel_size, 2)
    img_heigt = img.shape[0]
    img_width = img.shape[1]
    print(img_area)

    # 调用model
    mpl.rcParams['figure.dpi'] = 96
    # set model
    model = models.Cellpose(gpu=True, model_type='cyto2')
    # define CHANNELS to run segementation on
    # grayscale=0, R=1, G=2, B=3
    # channels = [cytoplasm, nucleus]
    chan = [2, 0]
    # segment image
    markers3, flows, styles, diams = model.eval(img, diameter=None, channels=chan)
    cell_boundary, resultar = getResults(img, markers3, pixel_size)

    cell_area = 0
    for i in range(len(resultar)):
        # 将排序后的结果写入文件中
        cell_area += resultar[i][0]

    return len(resultar), cell_area, img_area


if __name__ == '__main__':
    imgpath1 = r"D:/Users/YFENG/Desktop/test/cb173d6a55f726a67afc7fde7d85a17.jpg"
    # usr provide, if not or illegal, give a default value
    resfilepath1 = r"D:/Users/YFENG/Desktop/test"
    _,_,_,_,_,marker3=use_cellpose(imgpath1, resfilepath1)
    cv2.imshow("test",marker3)
    cv2.waitKey(0)

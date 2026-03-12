from callone import watershed
import os
def batch_watershed(image_dir,save_dir,thresholdmode=1,wttype=1,opiter=2,bgiter=3,dis=0,default=30,defaulthreshold=127,pixel = 0.273810):
    fileList = os.listdir(image_dir)
    n=0
    for i in fileList:
        imgName = image_dir + os.sep +fileList[n]
        # print(fileList)
        thresh, opening, sure_bg, sure_fg, unknown, img, img2, result, number, total, result_ratio, img_width, img_heigt, img_area = watershed(imgName,save_dir,thresholdmode,wttype,opiter,bgiter,dis,default,defaulthreshold,pixel)
        n=n+1
    print('finish!  the results are saved in filepath-->',save_dir)
    return n

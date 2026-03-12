import tkinter as tk
from tkinter import scrolledtext, END
from tkinter import ttk
from tkinter import IntVar
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import tkinter.filedialog
import numpy as np
import cv2
import re
from callone import watershed  # 分水岭算法函数
from batch import batch_watershed


class basedesk():
    def __init__(self, master):
        self.root = master
        self.root.title('肌肉组织切片扫描图像纤维细胞计量')
        self.root.geometry('1000x600')
        initwin(self.root)


class initwin():  # 主窗口
    def __init__(self, master):
        global im
        global image
        self.master = master
        self.master.config(bg='Magenta')
        self.initwin = tk.Frame(self.master, )
        self.initwin.pack()
        self.canvas = tk.Canvas(self.initwin,
                                width=1920,
                                height=1080,
                                bg='green')

        image = Image.open('background.jpg')
        im = ImageTk.PhotoImage(image)
        self.img_copy = image.copy()

        self.canvas.create_image(0, 0, anchor='nw', image=im)  # 使用create_image将图片添加到Canvas组件中
        self.canvas.bind("<Configure>", self.resize_image)

        self.canvas.pack()  # 将Canvas添加到主窗口
        btn_single = ttk.Button(self.initwin, text="单张图像处理", command=self.single)
        btn_batch = ttk.Button(self.initwin, text="批量图片处理", command=self.batch)
        btn_function = ttk.Button(self.initwin, text="功能介绍", command=self.function)

        self.canvas.create_window(200, 550, width=150, height=40, window=btn_single)
        self.canvas.create_window(500, 550, width=150, height=40, window=btn_batch)
        self.canvas.create_window(800, 550, width=150, height=40, window=btn_function)

        self.title = tk.Label(self.initwin, text="肌肉组织切片扫描图像纤维细胞计量", font=("微软雅黑", 30))
        self.author1 = tk.Label(self.initwin, text="中国农业科学院北京畜牧兽医研究所", font=("微软雅黑", 25))
        self.author2 = tk.Label(self.initwin, text="安徽省农业科学院畜牧兽医研究所", font=("微软雅黑", 25))
        self.author3 = tk.Label(self.initwin, text="北京林业大学", font=("微软雅黑", 25))
        self.canvas.create_window(190, 100, anchor="nw", width=700, height=50, window=self.title)
        self.canvas.create_window(330, 220, anchor="nw", window=self.author1)
        self.canvas.create_window(340, 320, anchor="nw", window=self.author2)
        self.canvas.create_window(415, 420, anchor="nw", window=self.author3)

    # 窗口自适应
    def resize_image(self, event):
        # 适应窗口大小比例缩放图片
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.background, anchor='nw')

    def single(self):
        self.initwin.destroy()
        singlewin(self.master)

    def batch(self):
        self.initwin.destroy()
        batchwin(self.master)

    def function(self):
        message = "本系统用于计量肌肉组织切片扫描图像纤维细胞，可以高效、精准地识别肌肉组织切片扫描图像，并生成标识了纤维细胞位置、序号的图像和储存细胞序号、细胞中心坐标、面积等结果信息保存到txt文件中。"
        a = tkinter.messagebox.showinfo("功能说明", message)
        print(a)


# 单张图像处理页面
class singlewin():
    def __init__(self, master):
        global im
        global image
        global e
        global e1
        global color
        global open_num
        global bgiter_num
        global dis_num
        global min_area
        global threshold_value
        global thresholdmode_value
        self.master = master
        self.master.config(bg='GhostWhite')
        self.str = "此处输出结果信息"
        self.singlewin = tk.Frame(self.master, )
        self.singlewin.pack()
        self.canvas = tk.Canvas(self.singlewin,
                                width=1920,
                                height=1080,
                                bg='white')

        image = Image.open('background.png')
        im = ImageTk.PhotoImage(image)
        self.img_copy = image.copy()

        self.canvas.create_image(0, 0, anchor='nw', image=im)  # 使用create_image将图片添加到Canvas组件中
        self.canvas.bind("<Configure>", self.resize_image)

        self.canvas.pack()  # 将Canvas添加到窗口
        self.img_copy = image.copy()

        self.canvas.create_image(0, 0, anchor='nw', image=im)  # 使用create_image将图片添加到Canvas组件中
        self.canvas.bind("<Configure>", self.resize_image)
        self.btn_back = ttk.Button(self.singlewin, text="返回主菜单", command=self.back)
        self.canvas.create_window(125, 500, width=150, height=30, window=self.btn_back)

        self.style_label = ttk.Style()
        self.style_label.configure("label.TLabel", font=("微软雅黑", 14))
        self.s_title = ttk.Label(self.singlewin, text="结果信息", style="label.TLabel", width=30, anchor="center")
        self.state = tk.Message(self.singlewin, text=self.str, width=300, font=("微软雅黑", 12))
        self.canvas.create_window(800, 100, height=50, window=self.s_title)
        self.canvas.create_window(650, 150, anchor="nw", width=300, window=self.state)

        self.choose_pic = ttk.Label(self.singlewin, text="选择图片", anchor="center", style="label.TLabel", width=100)
        self.save_pic = ttk.Label(self.singlewin, text="保存路径", anchor="center", style="label.TLabel", width=100)
        # self.color_label = ttk.Label(self.singlewin, text="细胞颜色", anchor="center", style="label.TLabel", width=100)
        self.open_label = ttk.Label(self.singlewin, text="开运算次数", anchor="center", style="label.TLabel", width=100)
        self.open_label_info = ttk.Label(self.singlewin, text="参考范围：1-5", anchor="center", style="label.TLabel",
                                         width=200)
        self.bgiter_label = ttk.Label(self.singlewin, text="膨胀次数", anchor="center", style="label.TLabel", width=100)
        self.bgiter_label_info = ttk.Label(self.singlewin, text="参考范围：1-10", anchor="center", style="label.TLabel",
                                           width=200)
        self.dis_label = ttk.Label(self.singlewin, text="腐蚀倍数", anchor="center", style="label.TLabel", width=100)
        self.dis_label_info = ttk.Label(self.singlewin, text="参考范围：0-1", anchor="center", style="label.TLabel",
                                        width=200)
        self.area_label = ttk.Label(self.singlewin, text="最小面积", anchor="center", style="label.TLabel", width=100)
        self.area_label_info = ttk.Label(self.singlewin, text="参考范围：10-100", anchor="center", style="label.TLabel",
                                         width=200)
        self.thresholdmode_label = ttk.Label(self.singlewin, text="阈值模式", anchor="center", style="label.TLabel",
                                             width=100)
        self.thresholdmode_label_info = ttk.Label(self.singlewin, text="0-255", anchor="center",
                                                  style="label.TLabel", width=100)
        self.threshold_label = ttk.Label(self.singlewin, text="阈值", anchor="center", style="label.TLabel", width=100)
        self.pixel_label = ttk.Label(self.singlewin, text="像素物理尺寸", anchor="center", style="label.TLabel",
                                     width=120)
        self.pixel_label_info = ttk.Label(self.singlewin, text="参考值：0.273810", anchor="center",
                                          style="label.TLabel", width=100)
        self.choose_file = ttk.Button(self.singlewin, text="...", command=self.choose_file)
        self.choose_save = ttk.Button(self.singlewin, text="...", command=self.save_file)
        self.btn_count = ttk.Button(self.singlewin, text="计量", command=self.count)
        self.btn_save = ttk.Button(self.singlewin, text="保存", command=self.save)
        # 选择框，用户选择处理导管细胞黑色或白色的图片
        color = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        # self.choose_color = ttk.Combobox(self.singlewin, font=("微软雅黑", 14), textvariable=color)  # 初始化
        # self.choose_color["values"] = ("导管细胞黑色", "导管细胞白色")
        # self.choose_color.current(0)  # 选择第一个
        # 选择开运算迭代次数
        open_num = tkinter.IntVar(value=2)
        self.choose_open = ttk.Entry(self.singlewin, show=None, font=("微软雅黑", 14), width=20, textvariable=open_num)
        # 选择膨胀迭代次数
        bgiter_num = tkinter.IntVar(value=3)
        self.choose_bgiter = ttk.Entry(self.singlewin, show=None, font=("微软雅黑", 14), width=20,
                                       textvariable=bgiter_num)
        # 选择腐蚀距离倍数,小数
        dis_num = tkinter.StringVar(value=0)
        self.choose_dis = ttk.Entry(self.singlewin, show=None, font=("微软雅黑", 14), width=20, textvariable=dis_num)
        # 选择保留的最小面积
        min_area = tkinter.StringVar(value=30)
        self.choose_area = ttk.Entry(self.singlewin, show=None, font=("微软雅黑", 14), width=20, textvariable=min_area)
        # 选择阈值模式
        thresholdmode_value = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        self.choose_thresholdmode = ttk.Combobox(self.singlewin, font=("微软雅黑", 14),
                                                 textvariable=thresholdmode_value)  # 初始化
        self.choose_thresholdmode["values"] = ("默认", "自定义")
        self.choose_thresholdmode.current(0)  # 选择第一个
        # 选择阈值
        threshold_value = tkinter.IntVar(value=160)
        self.choose_threshold = ttk.Entry(self.singlewin, show=None, font=("微软雅黑", 14), width=20,
                                          textvariable=threshold_value)
        # 像素物理尺寸
        pixel_pixel = tkinter.DoubleVar(value=0.273810)
        self.choose_pixel = ttk.Entry(self.singlewin, show=None, font=("微软雅黑", 14), width=20, textvariable=pixel_pixel)

        # 选择路径
        e = tkinter.StringVar()
        e1 = tkinter.StringVar()
        self.choose_bar = tk.Entry(self.singlewin, show=None, font=("微软雅黑", 14), width=20, textvariable=e)
        self.save_bar = tk.Entry(self.singlewin, show=None, font=("微软雅黑", 14), width=20, textvariable=e1)
        # 标记一下上面的东西都被创立了，下面要把它们放在画布上
        self.canvas.create_window(100, 100, width=100, window=self.choose_pic)
        self.canvas.create_window(280, 100, height=30, window=self.choose_bar)
        self.canvas.create_window(420, 100, width=50, height=30, window=self.choose_file)
        self.canvas.create_window(100, 150, width=100, window=self.save_pic)
        self.canvas.create_window(280, 150, height=30, window=self.save_bar)
        self.canvas.create_window(420, 150, width=50, height=30, window=self.choose_save)
        # 20240102添加
        # ---------------------------------------------------------------------------------------------
        self.canvas.create_window(500, 200, width=200, height=30, window=self.open_label_info)
        self.canvas.create_window(500, 250, width=200, height=30, window=self.bgiter_label_info)
        self.canvas.create_window(500, 300, width=200, height=30, window=self.dis_label_info)
        self.canvas.create_window(500, 350, width=200, height=30, window=self.area_label_info)
        self.canvas.create_window(750, 400, width=100, height=30, window=self.thresholdmode_label_info)
        self.canvas.create_window(450, 450, width=200, height=30, window=self.pixel_label_info)
        # ---------------------------------------------------------------------------------------------
        # 按键
        self.canvas.create_window(400, 500, width=150, height=30, window=self.btn_count)
        # self.canvas.create_window(450, 500, window=self.btn_save)
        # 选框
        # self.canvas.create_window(250, 200, width=100, window=self.color_label)
        # self.canvas.create_window(430, 200, height=30, window=self.choose_color)
        self.canvas.create_window(100, 200, width=100, window=self.open_label)
        self.canvas.create_window(280, 200, height=30, window=self.choose_open)
        self.canvas.create_window(100, 250, width=100, window=self.bgiter_label)
        self.canvas.create_window(280, 250, height=30, window=self.choose_bgiter)
        self.canvas.create_window(100, 300, width=100, window=self.dis_label)
        self.canvas.create_window(280, 300, height=30, window=self.choose_dis)
        self.canvas.create_window(100, 350, width=100, window=self.area_label)
        self.canvas.create_window(280, 350, height=30, window=self.choose_area)
        self.canvas.create_window(100, 400, width=100, window=self.thresholdmode_label)
        self.canvas.create_window(280, 400, height=30, window=self.choose_thresholdmode)
        self.canvas.create_window(480, 400, width=100, window=self.threshold_label)
        self.canvas.create_window(110, 450, width=120, window=self.pixel_label)

        self.canvas.create_window(600, 400, height=30, width=100, window=self.choose_threshold)
        self.canvas.create_window(260, 450, height=30, width=150, window=self.choose_pixel)

    def resize_image(self, event):
        # 适应窗口大小比例缩放图片
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.background, anchor='nw')

    def choose_file(self, ):
        self.select_file = tkinter.filedialog.askopenfilename(title='选择图片')  # 文件路径
        e.set(self.select_file)

    def save_file(self, ):
        self.save_file = tkinter.filedialog.asksaveasfilename(title='选择路径')  # 保存路径
        e1.set(self.save_file)

    def count(self, ):
        bgiter = None
        try:
            imgpath = self.select_file
            print(imgpath)
            resfilepath = self.save_file
            # 可调参数
            # 阈值模式
            # thresholdmode = 0
            if thresholdmode_value.get() == "默认":
                thresholdmode = 0
            else:
                thresholdmode = 1
            if color.get() == "导管细胞黑色":
                wttype = 0
            else:
                wttype = 1
            # 最小面积
            default = eval(self.choose_area.get())
            # 开运算迭代次数
            opiter = eval(self.choose_open.get())
            # 膨胀迭代次数
            bgiter = eval(self.choose_bgiter.get())
            # 阈值乘积因子
            dis = eval(self.choose_dis.get())
            # 自定义阈值
            defaulthreshold = eval(self.choose_threshold.get())
            # 像素物理尺寸
            pixel = eval(self.choose_pixel.get())
        except:
            message = "请输入正确的数据类型"
            a = tkinter.messagebox.showinfo("输入错误", message)
            print(a)
            return
        else:
            print('bgiter-->', bgiter)
            print('defaulthreshold-->', defaulthreshold)
            print('dis-->', dis)
            print('imgpath-->', imgpath)
            print('resfilepath-->', resfilepath)
            print('wttype-->', wttype)
            print('opiter-->', opiter)
            print('default-->', default)
            # call
            thresh, opening, sure_bg, sure_fg, unknown, img, img2, result, number, total, result_ratio, img_width, img_heigt, img_area = watershed(
                imgpath,
                resfilepath,
                thresholdmode,
                1,
                opiter, bgiter,
                dis,
                default,
                defaulthreshold,
                pixel
                )
            # 显示结果信息
            self.str = "图像总面积:%dum^2(%d*%d)\n细胞数量:%d\n细胞总面积:%dum^2\n细胞总面积占比:%.2f%%" % (
            img_area, img_width, img_heigt, number, total, result_ratio)
            self.state = tk.Message(self.singlewin, text=self.str, width=300, font=("微软雅黑", 12))
            self.canvas.create_window(650, 150, anchor="nw", width=300, window=self.state)

            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def save(self, ):
        pass

    def back(self, ):
        self.singlewin.destroy()
        initwin(self.master)

    # 批量图片处理页面


class batchwin():
    def __init__(self, master):
        global im
        global image
        global e
        global e1
        global color
        global open_num
        global bgiter_num
        global dis_num
        global min_area
        global threshold_value
        global thresholdmode_value
        self.master = master
        self.master.config(bg='GhostWhite')
        self.str = "此处输出结果信息"
        self.batchwin = tk.Frame(self.master, )
        self.batchwin.pack()
        self.canvas = tk.Canvas(self.batchwin,
                                width=1920,
                                height=1080,
                                bg='white')

        image = Image.open('background.png')
        im = ImageTk.PhotoImage(image)
        self.img_copy = image.copy()

        self.canvas.create_image(0, 0, anchor='nw', image=im)  # 使用create_image将图片添加到Canvas组件中
        self.canvas.bind("<Configure>", self.resize_image)

        self.canvas.pack()  # 将Canvas添加到窗口

        self.btn_back = ttk.Button(self.batchwin, text="返回主菜单", command=self.back)
        self.canvas.create_window(125, 500, width=150, height=30, window=self.btn_back)

        self.style_label = ttk.Style()
        self.style_label.configure("label.TLabel", font=("微软雅黑", 14))
        self.s_title = ttk.Label(self.batchwin, text="结果信息", style="label.TLabel", width=30, anchor="center")
        self.state = tk.Message(self.batchwin, text=self.str, width=300, font=("微软雅黑", 12))
        self.canvas.create_window(800, 100, height=50, window=self.s_title)
        self.canvas.create_window(650, 150, anchor="nw", width=300, window=self.state)

        self.choose_pic = ttk.Label(self.batchwin, text="选择图片", anchor="center", style="label.TLabel", width=100)
        self.save_pic = ttk.Label(self.batchwin, text="保存路径", anchor="center", style="label.TLabel", width=100)
        # self.color_label = ttk.Label(self.batchwin, text="细胞颜色", anchor="center", style="label.TLabel", width=100)
        self.open_label = ttk.Label(self.batchwin, text="开运算次数", anchor="center", style="label.TLabel", width=100)
        self.open_label_info = ttk.Label(self.batchwin, text="参考范围：1-5", anchor="center", style="label.TLabel",
                                         width=200)
        self.bgiter_label = ttk.Label(self.batchwin, text="膨胀次数", anchor="center", style="label.TLabel", width=100)
        self.bgiter_label_info = ttk.Label(self.batchwin, text="参考范围：1-10", anchor="center", style="label.TLabel",
                                           width=200)
        self.dis_label = ttk.Label(self.batchwin, text="腐蚀倍数", anchor="center", style="label.TLabel", width=100)
        self.dis_label_info = ttk.Label(self.batchwin, text="参考范围：0-1", anchor="center", style="label.TLabel",
                                        width=200)
        self.area_label = ttk.Label(self.batchwin, text="最小面积", anchor="center", style="label.TLabel", width=100)
        self.area_label_info = ttk.Label(self.batchwin, text="参考范围：10-100", anchor="center", style="label.TLabel",
                                         width=200)
        self.thresholdmode_label = ttk.Label(self.batchwin, text="阈值模式", anchor="center", style="label.TLabel",
                                             width=100)
        self.thresholdmode_label_info = ttk.Label(self.batchwin, text="0-255", anchor="center",
                                                  style="label.TLabel", width=100)
        self.threshold_label = ttk.Label(self.batchwin, text="阈值", anchor="center", style="label.TLabel", width=100)
        self.pixel_label = ttk.Label(self.batchwin, text="像素物理尺寸", anchor="center", style="label.TLabel",
                                     width=120)
        self.pixel_label_info = ttk.Label(self.batchwin, text="参考值：0.273810", anchor="center",
                                          style="label.TLabel", width=100)
        self.choose_file = ttk.Button(self.batchwin, text="...", command=self.choose_file)
        self.choose_save = ttk.Button(self.batchwin, text="...", command=self.save_file)
        self.btn_count = ttk.Button(self.batchwin, text="计量", command=self.count)
        self.btn_save = ttk.Button(self.batchwin, text="保存", command=self.save)
        # 选择框，用户选择处理导管细胞黑色或白色的图片
        color = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        # self.choose_color = ttk.Combobox(self.batchwin, font=("微软雅黑", 14), textvariable=color)  # 初始化
        # self.choose_color["values"] = ("导管细胞黑色", "导管细胞白色")
        # self.choose_color.current(0)  # 选择第一个
        # 选择开运算迭代次数
        open_num = tkinter.IntVar(value=2)
        self.choose_open = ttk.Entry(self.batchwin, show=None, font=("微软雅黑", 14), width=20, textvariable=open_num)
        # 选择膨胀迭代次数
        bgiter_num = tkinter.IntVar(value=3)
        self.choose_bgiter = ttk.Entry(self.batchwin, show=None, font=("微软雅黑", 14), width=20,
                                       textvariable=bgiter_num)
        # 选择腐蚀距离倍数
        dis_num = tkinter.IntVar(value=0)
        self.choose_dis = ttk.Entry(self.batchwin, show=None, font=("微软雅黑", 14), width=20, textvariable=dis_num)
        # 选择保留的最小面积
        min_area = tkinter.StringVar(value=30)
        self.choose_area = ttk.Entry(self.batchwin, show=None, font=("微软雅黑", 14), width=20, textvariable=min_area)
        # 选择阈值模式
        thresholdmode_value = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        self.choose_thresholdmode = ttk.Combobox(self.batchwin, font=("微软雅黑", 14),
                                                 textvariable=thresholdmode_value)  # 初始化
        self.choose_thresholdmode["values"] = ("默认", "自定义")
        self.choose_thresholdmode.current(0)  # 选择第一个
        # 选择阈值
        threshold_value = tkinter.StringVar(value=160)
        self.choose_threshold = ttk.Entry(self.batchwin, show=None, font=("微软雅黑", 14), width=20,
                                          textvariable=threshold_value)

        pixel_pixel = tkinter.DoubleVar(value=0.273810)
        self.choose_pixel = ttk.Entry(self.batchwin, show=None, font=("微软雅黑", 14), width=20, textvariable=pixel_pixel)
        # 选择路径
        e = tkinter.StringVar()
        e1 = tkinter.StringVar()
        self.choose_bar = tk.Entry(self.batchwin, show=None, font=("微软雅黑", 14), width=20, textvariable=e)
        self.save_bar = tk.Entry(self.batchwin, show=None, font=("微软雅黑", 14), width=20, textvariable=e1)
        # 标记一下上面的东西都被创立了，下面要把它们放在画布上
        self.canvas.create_window(100, 100, width=100, window=self.choose_pic)
        self.canvas.create_window(280, 100, height=30, window=self.choose_bar)
        self.canvas.create_window(420, 100, width=50, height=30, window=self.choose_file)
        self.canvas.create_window(100, 150, width=100, window=self.save_pic)
        self.canvas.create_window(280, 150, height=30, window=self.save_bar)
        self.canvas.create_window(420, 150, width=50, height=30, window=self.choose_save)
        # 20240102添加
        # ---------------------------------------------------------------------------------------------
        self.canvas.create_window(500, 200, width=200, height=30, window=self.open_label_info)
        self.canvas.create_window(500, 250, width=200, height=30, window=self.bgiter_label_info)
        self.canvas.create_window(500, 300, width=200, height=30, window=self.dis_label_info)
        self.canvas.create_window(500, 350, width=200, height=30, window=self.area_label_info)
        self.canvas.create_window(750, 400, width=100, height=30, window=self.thresholdmode_label_info)
        self.canvas.create_window(450, 450, width=200, height=30, window=self.pixel_label_info)
        # ---------------------------------------------------------------------------------------------
        # 按键
        self.canvas.create_window(400, 500, width=150, height=30, window=self.btn_count)
        # self.canvas.create_window(450, 500, window=self.btn_save)
        # 选框
        # self.canvas.create_window(250, 200, width=100, window=self.color_label)
        # self.canvas.create_window(430, 200, height=30, window=self.choose_color)
        self.canvas.create_window(100, 200, width=100, window=self.open_label)
        self.canvas.create_window(280, 200, height=30, window=self.choose_open)
        self.canvas.create_window(100, 250, width=100, window=self.bgiter_label)
        self.canvas.create_window(280, 250, height=30, window=self.choose_bgiter)
        self.canvas.create_window(100, 300, width=100, window=self.dis_label)
        self.canvas.create_window(280, 300, height=30, window=self.choose_dis)
        self.canvas.create_window(100, 350, width=100, window=self.area_label)
        self.canvas.create_window(280, 350, height=30, window=self.choose_area)
        self.canvas.create_window(100, 400, width=100, window=self.thresholdmode_label)
        self.canvas.create_window(280, 400, height=30, window=self.choose_thresholdmode)
        self.canvas.create_window(480, 400, width=100, window=self.threshold_label)
        self.canvas.create_window(110, 450, width=120, window=self.pixel_label)

        self.canvas.create_window(600, 400, height=30, width=100, window=self.choose_threshold)
        self.canvas.create_window(260, 450, height=30, width=150, window=self.choose_pixel)

    def resize_image(self, event):
        # 适应窗口大小比例缩放图片
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.background, anchor='nw')

    def choose_file(self, ):
        self.select_file = tkinter.filedialog.askdirectory(title='选择图片')  # 文件路径
        e.set(self.select_file)

    def save_file(self, ):
        self.save_file = tkinter.filedialog.askdirectory(title='选择路径')  # 保存路径
        e1.set(self.save_file)

    def open_file(self, ):
        start_directory = self.save_file
        os.startfile(start_directory)

    def count(self, ):
        bgiter = None
        try:
            imgpath = self.select_file
            print(imgpath)
            resfilepath = self.save_file
            # 可调参数
            # 阈值模式
            # thresholdmode = 0
            if thresholdmode_value.get() == "默认":
                thresholdmode = 0
            else:
                thresholdmode = 1
            if color.get() == "导管细胞黑色":
                wttype = 1
            else:
                wttype = 0
            # 最小面积
            default = eval(self.choose_area.get())
            # 开运算迭代次数
            opiter = eval(self.choose_open.get())
            # 膨胀迭代次数
            bgiter = eval(self.choose_bgiter.get())
            # 阈值乘积因子
            dis = eval(self.choose_dis.get())
            # 自定义阈值
            defaulthreshold = eval(self.choose_threshold.get())
            # 像素物理尺寸
            pixel = eval(self.choose_pixel.get())

        except:
            message = "请输入正确的数据类型"
            a = tkinter.messagebox.showinfo("输入错误", message)
            print(a)
            return
        else:
            print('bgiter-->', bgiter)
            print('defaulthreshold-->', defaulthreshold)
            print('dis-->', dis)
            print('imgpath-->', imgpath)
            print('resfilepath-->', resfilepath)
            print('wttype-->', wttype)
            print('opiter-->', opiter)
            print('default-->', default)
        num = batch_watershed(imgpath, resfilepath, thresholdmode, wttype, opiter, bgiter, dis, default,defaulthreshold,pixel)
        # num = batch_watershed(imgpath,resfilepath,wttype,opiter,bgiter,dis,default)
        # 显示结果信息
        self.str = "处理图像数量:%d\n" % (num)
        self.state = tk.Message(self.batchwin, text=self.str, width=300, font=("微软雅黑", 12))
        self.canvas.create_window(650, 150, anchor="nw", width=300, window=self.state)
        self.open_file = tk.Button(self.batchwin, text="打开保存文件夹", command=self.open_file)
        self.canvas.create_window(650, 485, anchor="nw", width=150, height=30, window=self.open_file)

    def save(self, ):
        pass

    def back(self, ):
        self.batchwin.destroy()
        initwin(self.master)


def StartGui():
    root = tk.Tk()
    basedesk(root)
    # 禁止用户调整窗口尺寸
    root.resizable(0, 0)
    root.mainloop()


if __name__ == "__main__":
    image = None
    im = None
    e = None
    e1 = None
    color = None
    open_num = None
    bgiter_num = None
    dis_num = None
    min_area = None
    threshhold_value = None
    thresholdmode_value = None

    StartGui()

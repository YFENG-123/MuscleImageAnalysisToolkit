import os
import tkinter as tk

import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog, ttk
from cellpose_based_method import use_cellpose
from tkinter import messagebox

from devide import devide3


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("主窗口")
        self.root.geometry("1080x720")
        for i in range(11):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(11):
            self.root.grid_columnconfigure(i, weight=1)

        # 创建按钮1，点击后切换到子窗口1
        self.button1 = tk.Button(self.root, text="开始计量", command=self.open_window1, width=13, height=0, bg="#4472C4",
                                 fg="white", font=("微软雅黑", 16))
        self.button1.grid(row=8, column=5, columnspan=1, ipady=0, pady=0)  # 使用 grid 布局

        # 创建按钮2，点击后切换到子窗口2
        self.button2 = tk.Button(self.root, text="使用说明", command=self.open_window2, width=13, height=0, bg="#4472C4",
                                 fg="white", font=("微软雅黑", 16))
        self.button2.grid(row=8, column=6, columnspan=1, ipady=0, pady=0)  # 使用 grid 布局

        # 在主窗口添加标签，显示文字
        self.label = tk.Label(self.root, text="基于深度模型的肌肉组织切片扫描图像\n肌内膜厚度计量软件",
                              font=("微软雅黑", 34))
        self.label.grid(row=1, column=3, columnspan=7)

        self.label = tk.Label(self.root, text="北京林业大学", font=("微软雅黑", 18), relief="groove", width=30, height=0)
        self.label.grid(row=6, column=5, columnspan=2, ipady=0, pady=1)

        self.label = tk.Label(self.root, text="中国农业科学院北京畜牧兽医研究所", font=("微软雅黑", 18), relief="groove",
                              width=30, height=0)
        self.label.grid(row=5, column=5, columnspan=2, ipady=0, pady=1)

        self.label = tk.Label(self.root, text="安徽省农业科学院畜牧兽医研究所", font=("微软雅黑", 18), relief="groove",
                              width=30, height=0)
        self.label.grid(row=4, column=5, columnspan=2, ipady=0, pady=1)

        self.image_path1 = r"bjfuicon.png"
        self.image_path2 = r"bjicon.png"
        self.image_path3 = r"anhuiicon.png"
        self.img1 = Image.open(self.image_path1)
        self.img2 = Image.open(self.image_path2)
        self.img3 = Image.open(self.image_path3)
        self.img1 = self.img1.resize((150, 150))  # 调整图像大小
        self.img2 = self.img2.resize((150, 150))  # 调整图像大小
        self.img3 = self.img3.resize((150, 150))  # 调整图像大小
        self.photo1 = ImageTk.PhotoImage(self.img1)
        self.photo2 = ImageTk.PhotoImage(self.img2)
        self.photo3 = ImageTk.PhotoImage(self.img3)

        self.img_label1 = tk.Label(self.root, image=self.photo1)
        self.img_label1.grid(row=2, column=7)
        self.img_label2 = tk.Label(self.root, image=self.photo2)
        self.img_label2.grid(row=2, column=5, columnspan=2)
        self.img_label3 = tk.Label(self.root, image=self.photo3)
        self.img_label3.grid(row=2, column=4)

        self.root.mainloop()

    def open_window1(self):
        self.root.destroy()

        # 创建子窗口1
        SubWindow1()

    def open_window2(self):
        self.root.destroy()

        # 创建子窗口2
        SubWindow2()


class SubWindow1:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("开始计量")
        self.root.geometry("1080x720")

        for i in range(11):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(11):
            self.root.grid_columnconfigure(i, weight=1)

        label = tk.Label(self.root, text="基于深度模型的肌肉组织切片扫描图像肌内膜厚度计量软件", font=("微软雅黑", 20))
        label.grid(row=0, column=0, columnspan=10)
        label = tk.Label(self.root, text="单幅图像处理", font=("微软雅黑", 14))
        label.grid(row=1, column=0, columnspan=1)

        label = tk.Label(self.root, text="结果信息显示框", font=("微软雅黑", 14))
        label.grid(row=1, column=8, columnspan=1)

        # 创建路径选择框
        self.file_var = tk.StringVar()
        self.file_entry = tk.Entry(self.root, textvariable=self.file_var, width=30, font=("微软雅黑", 16))
        self.file_entry.grid(row=2, column=1, columnspan=1, padx=0, ipadx=0, pady=0, ipady=0, sticky='nw')

        # 创建浏览按钮
        self.browse_button = tk.Button(self.root, text="选择图片", command=self.browse_file, width=10, height=0,
                                       bg="#4472C4", fg="white", font=("微软雅黑", 12))
        self.browse_button.grid(row=2, column=0, columnspan=1, sticky='n')

        # 创建路径选择框
        self.path_var1 = tk.StringVar()
        self.path_entry1 = tk.Entry(self.root, textvariable=self.path_var1, width=30, font=("微软雅黑", 16))
        self.path_entry1.grid(row=3, column=1, columnspan=1, padx=0, ipadx=0, pady=0, ipady=0, sticky='nw')

        # 创建浏览按钮
        self.browse_button1 = tk.Button(self.root, text="保存路径", command=self.browse_path1, width=10, height=0,
                                        bg="#4472C4", fg="white", font=("微软雅黑", 12))
        self.browse_button1.grid(row=3, column=0, columnspan=1, sticky='n')

        button1 = tk.Button(self.root, text="单幅计量", width=10, height=0, bg="#4472C4", fg="white", font=("微软雅黑", 12),
                            command=lambda: self.use_cellpose_s(self.selected_file, self.selected_path1))
        button1.grid(row=4, column=0, columnspan=1, sticky='n')

        label = tk.Label(self.root, text="\t像素物理尺寸", font=("微软雅黑", 12))
        label.grid(row=4, column=1, columnspan=1, sticky='wn')

        # 创建数字输入框
        self.numeric_var1 = tk.StringVar()
        self.numeric_entry1 = tk.Entry(self.root, textvariable=self.numeric_var1, validate="key",font=("微软雅黑", 14), width=18)
        self.numeric_entry1.grid(row=4, column=1, columnspan=1, sticky='ne')

        label = tk.Label(self.root, text="um/pixel    ", font=("微软雅黑", 14))
        label.grid(row=4, column=1, columnspan=1, sticky='en')

        label = tk.Label(self.root, text="多幅图像处理", font=("微软雅黑", 14))
        label.grid(row=5, column=0, columnspan=1, sticky='n')

        # 创建路径选择框
        self.path_var2 = tk.StringVar()
        self.path_entry2 = tk.Entry(self.root, textvariable=self.path_var2, width=30, font=("微软雅黑", 16))
        self.path_entry2.grid(row=6, column=1, columnspan=1, padx=0, ipadx=0, pady=0, ipady=0, sticky='nw')

        # 创建浏览按钮
        self.browse_button2 = tk.Button(self.root, text="选择路径", command=self.browse_path2, width=10, height=0,
                                        bg="#4472C4", fg="white", font=("微软雅黑", 12))
        self.browse_button2.grid(row=6, column=0, columnspan=1, sticky='n')

        # 创建路径选择框
        self.path_var3 = tk.StringVar()
        self.path_entry3 = tk.Entry(self.root, textvariable=self.path_var3, width=30, font=("微软雅黑", 16))
        self.path_entry3.grid(row=7, column=1, columnspan=1, padx=0, ipadx=0, pady=0, ipady=0, sticky='nw')

        # 创建浏览按钮
        self.browse_button3 = tk.Button(self.root, text="保存路径", command=self.browse_path3, width=10, height=0,
                                        bg="#4472C4", fg="white", font=("微软雅黑", 12))
        self.browse_button3.grid(row=7, column=0, columnspan=1, sticky='n')

        button2 = tk.Button(self.root, text="多幅计量", width=10, height=0, bg="#4472C4", fg="white", font=("微软雅黑", 12),
                            command=lambda: self.use_cellpose_m(self.selected_path2, self.selected_path3))
        button2.grid(row=8, column=0, columnspan=1, sticky='n')

        label = tk.Label(self.root, text="\t像素物理尺寸", font=("微软雅黑", 12))
        label.grid(row=8, column=1, columnspan=1, sticky='wn')

        # 创建数字输入框
        self.numeric_var2 = tk.StringVar()
        self.numeric_entry2 = tk.Entry(self.root, textvariable=self.numeric_var2, validate="key",font=("微软雅黑", 14), width=18)
        self.numeric_entry2.grid(row=8, column=1, columnspan=1, sticky='ne')

        label = tk.Label(self.root, text="um/pixel    ", font=("微软雅黑", 14))
        label.grid(row=8, column=1, columnspan=1, sticky='en')

        # 创建按钮，用于清空所有输入框
        self.clear_button = tk.Button(self.root, text="清空", command=self.clear_all_entries, width=13, height=0,
                                      bg="#4472C4", fg="white", font=("微软雅黑", 12))
        self.clear_button.grid(row=8, column=7, sticky='wn')  # 设置 sticky 为 "ew" 表示居中对齐

        # 创建返回按钮，点击后回到主窗口
        back_button = tk.Button(self.root, text="返回主页", command=self.close_window, width=13, height=0, bg="#4472C4",
                                fg="white", font=("微软雅黑", 12))
        back_button.grid(row=8, column=9, sticky='en')

        self.res_label = tk.Label(self.root, text="", font=("微软雅黑", 12),
                         relief="groove")
        self.res_label.grid(row=2, column=4, columnspan=7,rowspan = 6,sticky='wens')

        self.root.mainloop()



    def use_cellpose_s(self,file,path1):
        try:
            pixel_size = float(self.numeric_var1.get())
            if pixel_size <= 0:
                raise ValueError("这是一个手动抛出的 ValueError 异常")
        except ValueError as e:
            print(f"捕获到异常: {e}")
            self.res_label.config(text="无效的数字输入\n")

        np.set_printoptions(threshold=np.inf)
        image_path = file.replace('\\', os.sep)
        image_path = file.replace('/', os.sep)
        save_folder = path1.replace('\\', os.sep)
        save_folder = path1.replace('/', os.sep)
        save_folder = save_folder + '\\' + os.path.basename(image_path).split('.')[0] + '.txt'

        eqr,eqR,d = devide3(file)
        img = cv2.imread(image_path, 1)
        num,cell_area,_=use_cellpose(img)

        file = open(save_folder,"w")
        file.write('细胞图像文件名称:' + image_path + '\n')
        file.write("肌细胞的数量\t" + format(round(num, 2), ".2e") + "\t个\n")
        file.write("平均直径   \t" + format(round(2*eqr*pixel_size, 2), ".2e") + "\tum\n")
        file.write("平均面积   \t" + format(round(cell_area, 2), ".2e") + "\tum^2\n")
        file.write("肌内膜    \t" + format(round(d*pixel_size, 2), ".2e") + "\tum\n")

        file.close()
        current_text = self.res_label.cget("text")
        # 新的文本内容
        new_text = os.path.basename(image_path) + "  肌内膜厚度值： " + format(round(d*pixel_size, 2), ".2e") + "um\n"
        # 拼接原有文本和新文本
        result_text = current_text + new_text
        # 将拼接后的文本设置为标签的新文本内容
        self.res_label.config(text=result_text)




    def use_cellpose_m(self,path2,path3):
        try:
            pixel_size = float(self.numeric_var2.get())
            if pixel_size <= 0:
                raise ValueError("这是一个手动抛出的 ValueError 异常")

        except ValueError as e:
            print(f"捕获到异常: {e}")

            self.res_label.config(text="无效的数字输入\n")

        np.set_printoptions(threshold=np.inf)
        image_path = path2.replace('\\', os.sep)
        image_path = path2.replace('/', os.sep)
        save_folder = path3.replace('\\', os.sep)
        save_folder = path3.replace('/', os.sep)
        for foldername, subfolders, filenames in os.walk(image_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                save_folder1 = save_folder + '\\' + os.path.basename(file_path).split('.')[0] + '.txt'

                eqr, eqR, d = devide3(file_path)
                img = cv2.imread(file_path, 1)
                num, cell_area, _ = use_cellpose(img)

                file = open(save_folder1, "w")
                file.write('细胞图像文件名称:' + image_path + '\n')
                file.write("肌细胞的数量\t" + format(round(num, 2), ".2e") + "\t个\n")
                file.write("平均直径   \t" + format(round(2 * eqr * pixel_size, 2), ".2e") + "\tum\n")
                file.write("平均面积   \t" + format(round(cell_area, 2), ".2e") + "\tum^2\n")
                file.write("肌内膜    \t" + format(round(d * pixel_size, 2), ".2e") + "\tum\n")
                current_text = self.res_label.cget("text")
                # 新的文本内容
                new_text = os.path.basename(image_path) + "  肌内膜厚度值： " + format(round(d * pixel_size, 2), ".2e") + "um\n"
                # 拼接原有文本和新文本
                result_text = current_text + new_text
                # 将拼接后的文本设置为标签的新文本内容
                self.res_label.config(text=result_text)




    def clear_all_entries(self):
        # 清空所有输入框中的内容
        self.numeric_var1.set("")
        self.file_var.set("")
        self.path_var1.set("")
        self.path_var2.set("")
        self.path_var3.set("")
        self.numeric_var1.set("")
        self.numeric_var2.set("")
        for row in self.tree.get_children():
            self.tree.delete(row)

    def browse_file(self):
        # 根据选择框编号选择对应的变量和输入框
        current_var = self.file_var
        current_entry = self.file_entry

        # 打开文件对话框，获取用户选择的文件路径
        self.selected_file = filedialog.askopenfilename()

        # 更新路径选择框中的内容
        current_var.set(self.selected_file)

    def browse_path1(self):
        # 根据选择框编号选择对应的变量和输入框
        current_var = self.path_var1
        current_entry = self.path_entry1
        # 打开文件对话框，获取用户选择的文件路径
        self.selected_path1 = filedialog.askdirectory()
        # 更新路径选择框中的内容
        current_var.set(self.selected_path1)

    def browse_path2(self):
        # 根据选择框编号选择对应的变量和输入框
        current_var = self.path_var2
        current_entry = self.path_entry2
        # 打开文件对话框，获取用户选择的文件路径
        self.selected_path2 = filedialog.askdirectory()
        # 更新路径选择框中的内容
        current_var.set(self.selected_path2)

    def browse_path3(self):
        # 根据选择框编号选择对应的变量和输入框
        current_var = self.path_var3
        current_entry = self.path_entry3
        # 打开文件对话框，获取用户选择的文件路径
        self.selected_path3 = filedialog.askdirectory()
        # 更新路径选择框中的内容
        current_var.set(self.selected_path3)

    def validate_numeric_input1(self, input_text):
        # 验证用户输入，只允许输入数字和空格
        return input_text.isdigit() or input_text == ""

    def read_numeric_input1(self):
        # 读取输入框中的数字并显示
        numeric_value = self.numeric_var1.get()
        try:
            numeric_value = float(numeric_value)
            tk.messagebox.showinfo("读取结果", f"您输入的数字是: {numeric_value}")
        except ValueError:
            tk.messagebox.showerror("错误", "无效的数字输入")
        return numeric_value

    def validate_numeric_input2(self, input_text):
        # 验证用户输入，只允许输入数字和空格
        return input_text.isdigit() or input_text == ""

    def read_numeric_input2(self):
        # 读取输入框中的数字并显示
        numeric_value = self.numeric_var2.get()
        try:
            numeric_value = float(numeric_value)
            tk.messagebox.showinfo("读取结果", f"您输入的数字是: {numeric_value}")
        except ValueError:
            tk.messagebox.showerror("错误", "无效的数字输入")

    def close_window(self):
        # 销毁子窗口
        self.root.destroy()
        # 显示主窗口
        MainWindow()



class SubWindow2:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("使用说明")
        self.root.geometry("1080x720")

        for i in range(11):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(11):
            self.root.grid_columnconfigure(i, weight=1)

        label = tk.Label(self.root, text="基于深度模型的肌肉组织切片扫描图像肌内膜厚度计量软件", font=("微软雅黑", 20))
        label.grid(row=0, column=2, columnspan=7)

        label = tk.Label(self.root, text="软件使用说明", font=("微软雅黑", 14))
        label.grid(row=1, column=2, columnspan=7, sticky='')

        label = tk.Label(self.root, text="//软件简介\n"
                                    "    本软件主要应用于肌肉组织切片扫描图像肌纤维及肌内膜的专项识别，可以高效、精准\n"
                                    "地识别出肌肉组织切片扫描图像中的纤维细胞并输出肌纤维的数量、平均直径、平均面积、\n"
                                    "肌内膜等信息。此外本系统还具有多幅图像处理等功能，操作简便，用户体验优越。\n"
                                    "//软件简单使用步骤说明\n" 
                                    "单幅图像处理：\n"
                                    "    1.点击“开始计量”按钮；\n"
                                    "    2.点击“选择图片”按钮选择要处理的图片（图片路径不能包含中文）；\n"
                                    "    3.点击页面左上“单幅图像处理”部分的“保存路径”按钮选择保存路径；\n"
                                    "    4.输入像素物理尺寸；\n"
                                    "    5.点击“单幅计量”按钮。\n"
                                    "多幅图像处理\n"
                                    "    1.点击“开始计量”按钮；\n"
                                    "    2.点击“选择路径”按钮选择要处理的图片所在的文件夹（不能包含中文路径）；\n"
                                    "    3.点击页面左下“多幅图像处理”部分的“保存路径”按钮选择保存路径；\n"
                                    "    4.输入像素物理尺寸；\n"
                                    "    5.点击“多幅计量”按钮。\n"
                                    "//算法基本思想\n"
                                    "    该算法首先使用细胞模型分析肌纤维，获取其面积、个数和平均直径。随后，对RGB\n"
                                    "图像进行预处理，包括灰度化、二值化、膨胀和收缩操作，以还原肌束膜的初始状态。通\n"
                                    "过差异处理提取肌束膜的图像掩膜，从原图中去除，最后统计剩余部分的肌纤维和肌内膜\n"
                                    "面积之和，计算肌内膜厚度。", font=("微软雅黑", 14),
                         justify="left",relief="groove")
        label.grid(row=2, column=3, columnspan=5, sticky='n')

        # 创建返回按钮，点击后回到主窗口
        back_button = tk.Button(self.root, text="返回主页", command=self.close_window, width=13, height=0, bg="#4472C4",
                                fg="white", font=("微软雅黑", 14))
        back_button.grid(row=8, column=8, sticky='en')

        self.root.mainloop()

    def close_window(self):
        # 销毁子窗口
        self.root.destroy()
        # 显示主窗口
        MainWindow()



if __name__ == "__main__":
    MainWindow()


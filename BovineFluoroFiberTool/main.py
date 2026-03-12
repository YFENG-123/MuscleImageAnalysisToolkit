import os
import tkinter as tk

import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog, ttk


from cellpose_based_method import use_cellpose
from tkinter import messagebox

from devide import devide
selected_options = ["Type IIX", "Type IIA", "Type I", "Type IIA + IIX"]

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
        self.button1.grid(row=5, column=5, columnspan=2, ipady=0, pady=0)  # 使用 grid 布局

        # 创建按钮2，点击后切换到子窗口2
        self.button2 = tk.Button(self.root, text="使用说明", command=self.open_window2, width=13, height=0, bg="#4472C4",
                                 fg="white", font=("微软雅黑", 16))
        self.button2.grid(row=5, column=4, columnspan=4, ipady=0, pady=0, sticky="e")  # 使用 grid 布局

        # 创建按钮3，点击后切换到子窗口3
        self.button3 = tk.Button(self.root, text="颜色设置", command=self.open_window3, width=13, height=0, bg="#4472C4",
                                 fg="white", font=("微软雅黑", 16))
        self.button3.grid(row=5, column=4, columnspan=4, ipady=0, pady=0, sticky="w")  # 使用 grid 布局

        # 在主窗口添加标签，显示文字
        self.label = tk.Label(self.root, text="一种面向荧光染色牛肌肉组织切片扫描\n图像的肌纤维信息提取系统",
                              font=("微软雅黑", 34))
        self.label.grid(row=1, column=4, columnspan=5)

        self.label = tk.Label(self.root, text="北京林业大学", font=("微软雅黑", 18), relief="groove", width=30, height=0)
        self.label.grid(row=2, column=5, columnspan=2, ipady=0, pady=1)

        self.label = tk.Label(self.root, text="中国农业科学院北京畜牧兽医研究所", font=("微软雅黑", 18), relief="groove",
                              width=30, height=0)
        self.label.grid(row=3, column=5, columnspan=2, ipady=0, pady=1)

        self.label = tk.Label(self.root, text="安徽省农业科学院畜牧兽医研究所", font=("微软雅黑", 18), relief="groove",
                              width=30, height=0)
        self.label.grid(row=4, column=5, columnspan=2, ipady=0, pady=1)

        self.image_path1 = r".\bjfuicon.png"
        self.image_path2 = r".\bjicon.png"
        self.image_path3 = r".\anhuiicon.png"
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
        self.img_label1.grid(row=6, column=4, columnspan=1, sticky="e")
        self.img_label2 = tk.Label(self.root, image=self.photo2)
        self.img_label2.grid(row=6, column=5, columnspan=2, sticky="")
        self.img_label3 = tk.Label(self.root, image=self.photo3)
        self.img_label3.grid(row=6, column=7, columnspan=1, sticky="w")

        self.root.mainloop()

    def open_window1(self):
        self.root.destroy()
        # 创建子窗口1
        SubWindow1()

    def open_window2(self):
        self.root.destroy()
        # 创建子窗口2
        SubWindow2()

    def open_window3(self):
        self.root.destroy()
        # 创建子窗口3
        SubWindow3()


class SubWindow1:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("开始计量")
        self.root.geometry("1080x720")

        for i in range(11):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(11):
            self.root.grid_columnconfigure(i, weight=1)

        label = tk.Label(self.root, text="一种面向荧光染色牛肌肉组织切片扫描图像的肌纤维信息提取系统", font=("微软雅黑", 20))
        label.grid(row=0, column=0, columnspan=10)

        label = tk.Label(self.root, text="单幅图像处理", font=("微软雅黑", 14))
        label.grid(row=1, column=0, columnspan=1)

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

        label = tk.Label(self.root, text="        像素物理尺寸", font=("微软雅黑", 12))
        label.grid(row=4, column=1, columnspan=1, sticky='wn')

        # 创建数字输入框
        self.numeric_var1 = tk.StringVar()
        self.numeric_entry1 = tk.Entry(self.root, textvariable=self.numeric_var1, validate="key", font=("微软雅黑", 14),
                                       width=19)
        self.numeric_entry1.grid(row=4, column=1, columnspan=1, sticky='ne')

        label = tk.Label(self.root, text="um/pixel    ", font=("微软雅黑", 14))
        label.grid(row=4, column=1, columnspan=1, sticky='en')

        label = tk.Label(self.root, text="多幅图像处理", font=("微软雅黑", 14))
        label.grid(row=1, column=5, columnspan=1, sticky='')

        # 创建路径选择框
        self.path_var2 = tk.StringVar()
        self.path_entry2 = tk.Entry(self.root, textvariable=self.path_var2, width=30, font=("微软雅黑", 16))
        self.path_entry2.grid(row=2, column=6, columnspan=1, padx=0, ipadx=0, pady=0, ipady=0, sticky='nw')

        # 创建浏览按钮
        self.browse_button2 = tk.Button(self.root, text="选择路径", command=self.browse_path2, width=10, height=0,
                                        bg="#4472C4", fg="white", font=("微软雅黑", 12))
        self.browse_button2.grid(row=2, column=5, columnspan=1, sticky='n')

        # 创建路径选择框
        self.path_var3 = tk.StringVar()
        self.path_entry3 = tk.Entry(self.root, textvariable=self.path_var3, width=30, font=("微软雅黑", 16))
        self.path_entry3.grid(row=3, column=6, columnspan=1, padx=0, ipadx=0, pady=0, ipady=0, sticky='nw')

        # 创建浏览按钮
        self.browse_button3 = tk.Button(self.root, text="保存路径", command=self.browse_path3, width=10, height=0,
                                        bg="#4472C4", fg="white", font=("微软雅黑", 12))
        self.browse_button3.grid(row=3, column=5, columnspan=1, sticky='n')

        button2 = tk.Button(self.root, text="多幅计量", width=10, height=0, bg="#4472C4", fg="white", font=("微软雅黑", 12),
                            command=lambda: self.use_cellpose_m(self.selected_path2, self.selected_path3))
        button2.grid(row=4, column=5, columnspan=1, sticky='n')

        label = tk.Label(self.root, text="        像素物理尺寸", font=("微软雅黑", 12))
        label.grid(row=4, column=6, columnspan=1, sticky='wn')

        # 创建数字输入框
        self.numeric_var2 = tk.StringVar()
        self.numeric_entry2 = tk.Entry(self.root, textvariable=self.numeric_var2, validate="key", font=("微软雅黑", 14),
                                       width=19)
        self.numeric_entry2.grid(row=4, column=6, columnspan=1, sticky='ne')

        label = tk.Label(self.root, text="um/pixel    ", font=("微软雅黑", 14))
        label.grid(row=4, column=6, columnspan=1, sticky='en')

        label = tk.Label(self.root, text="计算结果", font=("微软雅黑", 14))
        label.grid(row=5, column=0, columnspan=2, sticky='ws')
        # 创建一个Frame作为表格容器
        self.table_frame = tk.Frame(self.root, borderwidth=1, relief="solid")
        self.table_frame.grid(row=6, column=0, columnspan=7, rowspan=2, sticky='w')

        # 创建表头
        label_header = tk.Label(self.table_frame, text="项名", width=19, height=2,
                                bg="#4472C4", font=("等线", 12, "bold"))
        label_header.grid(row=0, column=0)
        for j in range(1, 5):
            match (j):
                case 1:
                    label = tk.Label(self.table_frame, text=f"Type I", width=19, height=2,bg="#4472C4", font=("等线", 12, "bold"))
                    label.grid(row=0, column=j)
                case 2:
                    label = tk.Label(self.table_frame, text=f"Type IIA", width=19, height=2,bg="#4472C4", font=("等线", 12, "bold"))
                    label.grid(row=0, column=j)
                case 3:
                    label = tk.Label(self.table_frame, text=f"Type IIX", width=19, height=2,bg="#4472C4", font=("等线", 12, "bold"))
                    label.grid(row=0, column=j)
                case 4:
                    label = tk.Label(self.table_frame, text=f"Type IIA+IIX", width=19, height=2,bg="#4472C4", font=("等线", 12, "bold"))
                    label.grid(row=0, column=j)

        # 创建行标题和表格内容
        for i in range(1, 5):
            match (i):
                case 1:
                    label_row = tk.Label(self.table_frame, text=f"数量%", width=19, height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                    label_row.grid(row=i, column=0)

                    for j in range(1, 5):
                        Label = tk.Label(self.table_frame, text="", width=19, height=2, bg="#E9EBF5",font=("等线", 12, "bold"))
                        Label.grid(row=i, column=j)

                case 2:
                    label_row = tk.Label(self.table_frame, text=f"面积%", width=19, height=2,bg="#CFD5EA", font=("等线", 12, "bold"))
                    label_row.grid(row=i, column=0)
                    for j in range(1, 5):
                        Label = tk.Label(self.table_frame, text="", width=19, height=2, bg="#CFD5EA",font=("等线", 12, "bold"))
                        Label.grid(row=i, column=j)

                case 3:
                    label_row = tk.Label(self.table_frame, text=f"平均直径um", width=19, height=2,bg="#E9EBF5", font=("等线", 12, "bold"))
                    label_row.grid(row=i, column=0)
                    for j in range(1, 5):
                        Label = tk.Label(self.table_frame, text="", width=19, height=2, bg="#E9EBF5",font=("等线", 12, "bold"))
                        Label.grid(row=i, column=j)

                case 4:
                    label_row = tk.Label(self.table_frame, text=f"平均面积um^2", width=19, height=2, bg="#CFD5EA", font=("等线", 12, "bold"))
                    label_row.grid(row=i, column=0)
                    for j in range(1, 5):
                        Label = tk.Label(self.table_frame, text="", width=19, height=2, bg="#CFD5EA",font=("等线", 12, "bold"))
                        Label.grid(row=i, column=j)

        # 创建按钮，用于清空所有输入框
        self.clear_button = tk.Button(self.root, text="清空信息", command=self.clear_all_entries, width=10, height=0,
                                      bg="#4472C4", fg="white", font=("微软雅黑", 12))
        self.clear_button.grid(row=6, column=5, columnspan=2, sticky='e')  # 设置 sticky 为 "ew" 表示居中对齐

        # 创建返回按钮，点击后回到主窗口
        back_button = tk.Button(self.root, text="返回主页", command=self.close_window, width=10, height=0,
                                bg="#4472C4",
                                fg="white", font=("微软雅黑", 12))
        back_button.grid(row=7, column=5, columnspan=2, sticky='en')

        self.root.mainloop()



    def use_cellpose_s(self, file, path1,mod=1):
        try:
            if mod:
                self.pixel_size = float(self.numeric_var1.get())
                if self.pixel_size <= 0:
                    raise ValueError("这是一个手动抛出的 ValueError 异常")

            resultar=[]
            cell_area=[]
            img_area=[]
            diameter=[]
            r,rp,g,gp,b,bp,p,pp=devide(file,path1)
            resultarr, cell_arear, img_arear,diameterr, pr1, pr2 = use_cellpose(rp,path1,img=r, pixel_size=self.pixel_size)
            resultarg, cell_areag, img_areag,diameterg, pg1, pg2 = use_cellpose(gp,path1,img=g, pixel_size=self.pixel_size)
            resultarb, cell_areab, img_areab,diameterb, pb1, pb2 = use_cellpose(bp,path1,img=b, pixel_size=self.pixel_size)
            resultarp, cell_areap, img_areap,diameterp, pp1, pp2 = use_cellpose(pp,path1,img=p, pixel_size=self.pixel_size)


            resultar.append(float(resultarr))
            resultar.append(float(resultarg))
            resultar.append(float(resultarb))
            resultar.append(float(resultarp))
            cell_area.append(float(cell_arear))
            cell_area.append(float(cell_areag))
            cell_area.append(float(cell_areab))
            cell_area.append(float(cell_areap))
            img_area.append(float(img_arear))
            img_area.append(float(img_areag))
            img_area.append(float(img_areab))
            img_area.append(float(img_areap))
            diameter.append(float(diameterr))
            diameter.append(float(diameterg))
            diameter.append(float(diameterb))
            diameter.append(float(diameterp))
            resultar_all = resultar[0]+resultar[1]+resultar[2]+resultar[3]


            filer = open(pr2, mode='a')
            fileg = open(pg2, mode='a')
            fileb = open(pb2, mode='a')
            filep = open(pp2, mode='a')
            try:
                filer.write('数量占比%' + '\t' + '面积占比%' + '\t\t' + '平均直径um' + '\t\t' + '平均面积um^2' + '\n')
                filer.write(f'{round(resultarr/resultar_all,2)}' + '%\t\t' + f'{round(cell_arear/img_arear,2)}' + '%\t\t\t' + f'{round(diameterr/resultar[0],2)}' + 'um\t\t' + f'{round(cell_arear,2)}' + 'um^2\n')
            except:
                filer.write('数量占比%' + '\t' + '面积占比%' + '\t\t' + '平均直径um' + '\t\t' + '平均面积um^2' + '\n')
                filer.write(f'{round(resultarr / resultar_all, 2)}' + '%\t\t' + f'{round(cell_arear / img_arear, 2)}' + '%\t\t\t' + f'{round(diameterr / 9999, 2)}' + 'um\t\t' + f'{round(cell_arear, 2)}' + 'um^2\n')

            try:
                fileg.write('数量占比%' + '\t' + '面积占比%' + '\t\t' + '平均直径um' + '\t\t' + '平均面积um^2' + '\n')
                fileg.write(f'{round(resultarg/resultar_all,2)}' + '%\t\t' + f'{round(cell_areag/img_areag,2)}' + '%\t\t\t' + f'{round(diameterg/resultar[1],2)}' + 'um\t\t' + f'{round(cell_areag,2)}' + 'um^2\n')
            except:
                fileg.write('数量占比%' + '\t' + '面积占比%' + '\t\t' + '平均直径um' + '\t\t' + '平均面积um^2' + '\n')
                fileg.write(f'{round(resultarg / resultar_all, 2)}' + '%\t\t' + f'{round(cell_areag / img_areag, 2)}' + '%\t\t\t' + f'{round(diameterg / 9999, 2)}' + 'um\t\t' + f'{round(cell_areag, 2)}' + 'um^2\n')

            try:
                fileb.write('数量占比%' + '\t' + '面积占比%' + '\t\t' + '平均直径um' + '\t\t' + '平均面积um^2' + '\n')
                fileb.write(f'{round(resultarb/resultar_all,2)}' + '%\t\t' + f'{round(cell_areab/img_areab,2)}' + '%\t\t\t' + f'{round(diameterb/resultar[2],2)}' + 'um\t\t' + f'{round(cell_areab,2)}' + 'um^2\n')
            except:
                fileb.write('数量占比%' + '\t' + '面积占比%' + '\t\t' + '平均直径um' + '\t\t' + '平均面积um^2' + '\n')
                fileb.write( f'{round(resultarb / resultar_all, 2)}' + '%\t\t' + f'{round(cell_areab / img_areab, 2)}' + '%\t\t\t' + f'{round(diameterb / 9999, 2)}' + 'um\t\t' + f'{round(cell_areab, 2)}' + 'um^2\n')

            try:
                filep.write('数量占比%' + '\t' + '面积占比%' + '\t\t' + '平均直径um' + '\t\t' + '平均面积um^2' + '\n')
                filep.write(f'{round(resultarp/resultar_all,2)}' + '%\t\t' + f'{round(cell_areap/img_areap,2)}' + '%t\t\t\t' + f'{round(diameterp/resultar[3],2)}' + 'um\t\t' + f'{round(cell_areap,2)}' + 'um^2\n')
            except:
                filep.write('数量占比%' + '\t' + '面积占比%' + '\t\t' + '平均直径um' + '\t\t' + '平均面积um^2' + '\n')
                filep.write(f'{round(resultarp / resultar_all, 2)}' + '%\t\t' + f'{round(cell_areap / img_areap, 2)}' + '%t\t\t\t' + f'{round(diameterp / 9999, 2)}' + 'um\t\t' + f'{round(cell_areap, 2)}' + 'um^2\n')


            i=0
            # 创建行标题和表格内容
            for option in selected_options:
                match option:
                    case "Type I":
                        Label = tk.Label(self.table_frame, text=f"{round((resultar[i]/resultar_all)*100,2)}", width=19 , height=2, bg="#E9EBF5",font=("等线", 12, "bold"))
                        Label.grid(row=1, column=1)
                        Label = tk.Label(self.table_frame,text=f"{round((cell_area[i] / img_area[i]) * 100, 2)}", width=19 ,height=2, bg="#CFD5EA", font=("等线", 12, "bold"))
                        Label.grid(row=2, column=1)
                        try:
                            y = round(diameter[i] / resultar[i], 2)
                            Label = tk.Label(self.table_frame, text=f"{y}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                            Label.grid(row=3, column=1)
                        except:
                            y = round(diameter[i] / 9999, 2)
                            Label = tk.Label(self.table_frame, text=f"{y}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                            Label.grid(row=3, column=1)
                        try:
                            x = round(cell_area[i] / resultar[i], 2)
                            Label = tk.Label(self.table_frame, text=f"{x}", width=19, height=2, bg="#CFD5EA",
                                             font=("等线", 12, "bold"))
                            Label.grid(row=4, column=1)
                        except:
                            x = round(cell_area[i] / 9999, 2)
                            Label = tk.Label(self.table_frame, text=f"{x}", width=19, height=2, bg="#CFD5EA",
                                             font=("等线", 12, "bold"))
                            Label.grid(row=4, column=1)

                    case "Type IIA":
                        Label = tk.Label(self.table_frame,text=f"{round((resultar[i] / resultar_all) * 100, 2)}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                        Label.grid(row=1, column=2)
                        Label = tk.Label(self.table_frame,text=f"{round((cell_area[i] / img_area[i]) * 100, 2)}", width=19,height=2, bg="#CFD5EA", font=("等线", 12, "bold"))
                        Label.grid(row=2, column=2)
                        try:
                            y = round(diameter[i] / resultar[i], 2)
                            Label = tk.Label(self.table_frame, text=f"{y}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                            Label.grid(row=3, column=2)
                        except:
                            y = round(diameter[i] / 9999, 2)
                            Label = tk.Label(self.table_frame, text=f"{y}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                            Label.grid(row=3, column=2)
                        try:
                            x = round(cell_area[i]/resultar[i], 2)
                            Label = tk.Label(self.table_frame, text=f"{x}", width=19, height=2, bg="#CFD5EA",
                                             font=("等线", 12, "bold"))
                            Label.grid(row=4, column=2)
                        except:
                            x = round(cell_area[i] / 9999, 2)
                            Label = tk.Label(self.table_frame, text=f"{x}", width=19, height=2, bg="#CFD5EA",
                                             font=("等线", 12, "bold"))
                            Label.grid(row=4, column=2)



                    case "Type IIX":
                        Label = tk.Label(self.table_frame,text=f"{round((resultar[i] / resultar_all) * 100, 2)}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                        Label.grid(row=1, column=3)
                        Label = tk.Label(self.table_frame,text=f"{round((cell_area[i] / img_area[i]) * 100, 2)}", width=19,height=2, bg="#CFD5EA", font=("等线", 12, "bold"))
                        Label.grid(row=2, column=3)
                        try:
                            y = round(diameter[i] / resultar[i], 2)
                            Label = tk.Label(self.table_frame, text=f"{y}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                            Label.grid(row=3, column=3)
                        except:
                            y = round(diameter[i] / 9999, 2)
                            Label = tk.Label(self.table_frame, text=f"{y}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                            Label.grid(row=3, column=3)
                        try:
                            x = round(cell_area[i] / resultar[i], 2)
                            Label = tk.Label(self.table_frame, text=f"{x}", width=19, height=2, bg="#CFD5EA",
                                             font=("等线", 12, "bold"))
                            Label.grid(row=4, column=3)
                        except:
                            x = round(cell_area[i] / 9999, 2)
                            Label = tk.Label(self.table_frame, text=f"{x}", width=19, height=2, bg="#CFD5EA",
                                             font=("等线", 12, "bold"))
                            Label.grid(row=4, column=3)

                    case "Type IIA + IIX":
                        Label = tk.Label(self.table_frame,text=f"{round((resultar[i] / resultar_all) * 100, 2)}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                        Label.grid(row=1, column=4)
                        Label = tk.Label(self.table_frame,text=f"{round((cell_area[i] / img_area[i]) * 100, 2)}", width=19,height=2, bg="#CFD5EA", font=("等线", 12, "bold"))
                        Label.grid(row=2, column=4)
                        try:
                            y = round(diameter[i] / resultar[i], 2)
                            Label = tk.Label(self.table_frame, text=f"{y}",width=19, height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                            Label.grid(row=3, column=4)
                        except:
                            y = round(diameter[i] / 9999, 2)
                            Label = tk.Label(self.table_frame, text=f"{y}", width=19,height=2, bg="#E9EBF5", font=("等线", 12, "bold"))
                            Label.grid(row=3, column=4)
                        try:
                            x = round(cell_area[i] / resultar[i], 2)
                            Label = tk.Label(self.table_frame, text=f"{x}", width=19, height=2, bg="#CFD5EA",
                                             font=("等线", 12, "bold"))
                            Label.grid(row=4, column=4)
                        except:
                            x = round(cell_area[i] / 9999, 2)
                            Label = tk.Label(self.table_frame, text=f"{x}", width=19, height=2, bg="#CFD5EA",
                                             font=("等线", 12, "bold"))
                            Label.grid(row=4, column=4)
                i+=1


            if mod:
                tk.messagebox.showinfo("提示", f"测量成功，已保存至\n{pr1}\n{pr2}\n{pg1}\n{pg2}\n{pb1}\n{pb2}\n{pp1}\n{pp2}")
        except ValueError as e:
            print(f"捕获到异常: {e}")
            tk.messagebox.showerror("提示","无效的数字输入")


    def use_cellpose_m(self, path2, path3):

        try:
            self.pixel_size = float(self.numeric_var2.get())
            if self.pixel_size <= 0:
                raise ValueError("这是一个手动抛出的 ValueError 异常")
            for foldername, subfolders, filenames in os.walk(path2):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    self.use_cellpose_s(file_path,path3,0)
                tk.messagebox.showinfo("提示",f"测量成功，已保存至\n{path3}")


        except ValueError as e:
            print(f"捕获到异常: {e}")
            tk.messagebox.showerror("提示","无效的数字输入")


    def clear_all_entries(self):
        # 清空所有输入框中的内容
        self.numeric_var1.set("")
        self.file_var.set("")
        self.path_var1.set("")
        self.path_var2.set("")
        self.path_var3.set("")
        self.numeric_var1.set("")
        self.numeric_var2.set("")
        # 创建一个Frame作为表格容器
        self.table_frame = tk.Frame(self.root, borderwidth=1, relief="solid")
        self.table_frame.grid(row=6, column=0, columnspan=7, rowspan=2, sticky='w')

        # 创建表头
        label_header = tk.Label(self.table_frame, text="项名", width=19, height=2,
                                bg="#4472C4", font=("等线", 12, "bold"))
        label_header.grid(row=0, column=0)
        for j in range(1, 5):
            match (j):
                case 1:
                    label = tk.Label(self.table_frame, text=f"Type I", width=19, height=2, bg="#4472C4",
                                     font=("等线", 12, "bold"))
                    label.grid(row=0, column=j)
                case 2:
                    label = tk.Label(self.table_frame, text=f"Type IIA", width=19, height=2, bg="#4472C4",
                                     font=("等线", 12, "bold"))
                    label.grid(row=0, column=j)
                case 3:
                    label = tk.Label(self.table_frame, text=f"Type IIX", width=19, height=2, bg="#4472C4",
                                     font=("等线", 12, "bold"))
                    label.grid(row=0, column=j)
                case 4:
                    label = tk.Label(self.table_frame, text=f"Type IIA+IIX", width=19, height=2, bg="#4472C4",
                                     font=("等线", 12, "bold"))
                    label.grid(row=0, column=j)

        # 创建行标题和表格内容
        for i in range(1, 5):
            match (i):
                case 1:
                    label_row = tk.Label(self.table_frame, text=f"数量%", width=19, height=2, bg="#E9EBF5",
                                         font=("等线", 12, "bold"))
                    label_row.grid(row=i, column=0)

                    for j in range(1, 5):
                        Label = tk.Label(self.table_frame, text="", width=19, height=2, bg="#E9EBF5",
                                         font=("等线", 12, "bold"))
                        Label.grid(row=i, column=j)

                case 2:
                    label_row = tk.Label(self.table_frame, text=f"面积%", width=19, height=2, bg="#CFD5EA",
                                         font=("等线", 12, "bold"))
                    label_row.grid(row=i, column=0)
                    for j in range(1, 5):
                        Label = tk.Label(self.table_frame, text="", width=19, height=2, bg="#CFD5EA",
                                         font=("等线", 12, "bold"))
                        Label.grid(row=i, column=j)

                case 3:
                    label_row = tk.Label(self.table_frame, text=f"平均直径um", width=19, height=2, bg="#E9EBF5",
                                         font=("等线", 12, "bold"))
                    label_row.grid(row=i, column=0)
                    for j in range(1, 5):
                        Label = tk.Label(self.table_frame, text="", width=19, height=2, bg="#E9EBF5",
                                         font=("等线", 12, "bold"))
                        Label.grid(row=i, column=j)

                case 4:
                    label_row = tk.Label(self.table_frame, text=f"平均面积um^2", width=19, height=2, bg="#CFD5EA",
                                         font=("等线", 12, "bold"))
                    label_row.grid(row=i, column=0)
                    for j in range(1, 5):
                        Label = tk.Label(self.table_frame, text="", width=19, height=2, bg="#CFD5EA",
                                         font=("等线", 12, "bold"))
                        Label.grid(row=i, column=j)


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

        label = tk.Label(self.root, text="一种面向荧光染色牛肌肉组织切片扫描图像的肌纤维信息提取系统", font=("微软雅黑", 20))
        label.grid(row=0, column=2, columnspan=7)

        label = tk.Label(self.root, text="软件使用说明", font=("微软雅黑", 14))
        label.grid(row=2, column=2, columnspan=7)

        label = tk.Label(self.root, text="//软件简介\n    本软件可以高效、精准地识别出荧光牛肌肉组织切片扫描图像中不同颜色的纤维细胞并\n输出各种颜色纤维细胞数量占比、面积占比、平均直径、平均面积等信息并保存到txt文件中。\n//软件简单使用步骤说明\n单幅图像处理：\n    1.点击“颜色设置”按钮进行颜色设置，设置完成后点击“保存”按钮；\n    2.点击“返回主页”按钮回到主页，点击“开始计量”按钮；\n    3.点击“选择图片”按钮选择要处理的图片（图片路径不能包含中文）；\n    4.点击页面左上“单幅图像处理”部分的“保存路径”按钮选择保存路径；\n    5.输入像素物理尺寸（需输入大于0的数）；\n    6.点击“单幅计量”按钮。\n\n多幅图像处理：\n    1.点击“颜色设置”按钮进行颜色设置，设置完成后点击“保存”按钮；\n    2.点击“返回主页”按钮回到主页，点击“开始计量”按钮；\n    3.点击“选择路径”按钮选择要处理的图片所在的文件夹（不能包含中文路径）；\n    4.点击页面右上“多幅图像处理”部分的“保存路径”按钮选择保存路径；\n    5.输入像素物理尺寸（需输入大于0的数）；\n    6.点击“多幅计量”按钮。", font=("微软雅黑", 14),
                         relief="groove" ,justify="left")
        label.grid(row=3, column=2, columnspan=7, sticky='n')

        # 创建返回按钮，点击后回到主窗口
        back_button = tk.Button(self.root, text="返回主页", command=self.close_window, width=13, height=0, bg="#4472C4",
                                fg="white", font=("微软雅黑", 12))
        back_button.grid(row=8, column=8, sticky='en')

        self.root.mainloop()

    def close_window(self):
        # 销毁子窗口
        self.root.destroy()
        # 显示主窗口
        MainWindow()


class SubWindow3:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("颜色设置")
        self.root.geometry("1080x720")

        for i in range(11):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(11):
            self.root.grid_columnconfigure(i, weight=1)

        label = tk.Label(self.root, text="一种面向荧光染色牛肌肉组织切片扫描图像的肌纤维信息提取系统", font=("微软雅黑", 20))
        label.grid(row=0, column=2, columnspan=7)

        label = tk.Label(self.root, text="颜色", font=("微软雅黑", 16))
        label.grid(row=1, column=5, columnspan=1)

        label = tk.Label(self.root, text="肌纤维类别", font=("微软雅黑", 16))
        label.grid(row=1, column=6, columnspan=1)

        def check_options():
            selected_options.clear()
            for combo in combo_boxes:
                selected_option = combo.get()
                if not selected_option:
                    show_error("Error", "Please select an option in all dropdowns.")
                    return

                if selected_option in selected_options:
                    show_error("Error", "Duplicate option found. Please select unique options.")
                    return

                selected_options.append(selected_option)
            show_message("Success", "All options are valid.")

        def show_error(title, message):
            tk.messagebox.showerror(title, message)

        def show_message(title, message):
            tk.messagebox.showinfo(title, message)

        # 创建四个下拉选项框
        combo_boxes = []

        for i in range(4):
            match(i):
                case 0:
                    label = tk.Label(self.root, text=f"红色",bg="red",font=("等线", 16, "bold"),relief="solid",bd=1)
                    label.grid(row=i + 2, column=5, padx=10, pady=10 ,sticky="")
                case 1:
                    label = tk.Label(self.root, text=f"蓝色",bg="blue",font=("等线", 16, "bold"),relief="solid",bd=1)
                    label.grid(row=i + 2, column=5, padx=10, pady=10, sticky="")
                case 2:
                    label = tk.Label(self.root, text=f"绿色",bg="green",font=("等线", 16, "bold"),relief="solid",bd=1)
                    label.grid(row=i+2, column=5, padx=10, pady=10, sticky="")
                case 3:
                    label = tk.Label(self.root, text=f"紫色",bg="purple",font=("等线", 16, "bold"),relief="solid",bd=1)
                    label.grid(row=i + 2, column=5, padx=10, pady=10, sticky="")

            combo_box = ttk.Combobox(self.root, values=["Type I", "Type IIA", "Type IIX", "Type IIA + IIX"],font=("等线", 16, "bold"),width=15,height=20)
            combo_box.grid(row=i+2, column=6, padx=10, pady=15)

            combo_boxes.append(combo_box)

        #
        back_button2 = tk.Button(self.root, text="保存", command=check_options, width=13, height=0, bg="#4472C4",
                                 fg="white", font=("微软雅黑", 12))
        back_button2.grid(row=8, column=5, sticky='en')

        # 创建返回按钮，点击后回到主窗口
        back_button1 = tk.Button(self.root, text="返回主页", command=self.close_window, width=13, height=0, bg="#4472C4",
                                fg="white", font=("微软雅黑", 12))
        back_button1.grid(row=8, column=6, sticky='en')

        self.root.mainloop()



    def close_window(self):
        # 销毁子窗口
        self.root.destroy()
        # 显示主窗口
        MainWindow()


if __name__ == "__main__":
    MainWindow()


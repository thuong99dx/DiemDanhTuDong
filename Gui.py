import datetime
import math
import pickle
import sqlite3
import time
import tkinter as tk  # python 3
from tkinter import font  as tkfont  # python 3
from tkinter import messagebox, PhotoImage, filedialog

import pandas as pd
from PIL import Image, ImageTk
from sklearn.svm import SVC
import tensorflow as tf
import numpy as np
import argparse
import os
import sys

import faceRecognition as fr
from align.align_mtcnn import *
from facenet.face_contrib import *
import facenet
from helpers import no_accent_vietnamese

filePathClass = ""
fileNameClass = ""
listStudentDataFrame = None
icon = "D:/Test/AI (1)/AI/OpenCV/image/icon.ico"


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Điểm danh lớp học")
        self.resizable(False, False)
        p1 = PhotoImage(file="D:/Test/AI (1)/AI/OpenCV/image/icon.ico")
        self.iconphoto(False, p1)
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True, )
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageSV, PageData, PageDiemDanh, PageDanhSach):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def saveExcel(self):
        writer = pd.ExcelWriter(filePathClass, engine='xlsxwriter')
        listStudentDataFrame.to_excel(writer, engine='xlsxwriter', index=False)
        writer.save()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        imageBg = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/OpenCV/image/anh1.jpg').resize((900, 900)))
        backgroundLabel = tk.Label(self, image=imageBg, width=1000, height=900)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100)

        label1 = tk.Label(self, text="BAN CƠ YẾU CHÍNH PHỦ", font=("fontNomal", 30), fg="red")
        label1.grid(row=5, column=0)
        label1 = tk.Label(self, text="HỌC VIỆN KỸ THUẬT MẬT MÃ", font=("fontNomal", 30), fg="red")
        label1.grid(row=6, column=0)

        # imageBg1 = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/matma.jpg').resize((130, 130)))
        # backgroundLabel = tk.Label(self, image=imageBg1, width=100, height=1000)
        # backgroundLabel.image = imageBg1
        # backgroundLabel.grid(row=0, column=1, rowspan=100,sticky="nsew")
        # backgroundLabel.place(x=200, y=350)

        label1 = tk.Label(self, text="Ứng Dụng Điểm Danh Bằng", font=("fontNomal", 20), fg="red")
        label1.grid(row=10, column=0)
        label1 = tk.Label(self, text="Nhận Diện Khuôn Mặt", font=("fontNomal", 20), fg="red")
        label1.grid(row=11, column=0)

        #lable2 = tk.Label(self, text="Username", font=self.controller.title_font)
        #lable2.grid(row=29, column=0)
        #lable2.place(x=300, y=350)
        #self.newId = tk.Entry(self, borderwidth=0, bg="#FFFFCC", font=('Helvetica', 20), width=20, justify="center")
        #self.newId.grid(row=30, column=0, padx=50)
        #self.newId.place(x=450, y=350)
        #lb1 = tk.Label(self, text="Password", font=self.controller.title_font)
        #lb1.grid(row=31, column=0, padx=50)
        #lb1.place(x=300, y=410)
        #self.newPassword = tk.Entry(self, borderwidth=0, bg="#FFFFCC", font=('Helvetica', 20), width=20,justify="center")
        #self.newPassword.grid(row=32, column=0, padx=50)
        #self.newPassword.place(x=450, y=410)

        button1 = tk.Button(self, text="Đăng nhập", command=lambda: controller.show_frame("PageOne"), font="fontNomal",
                            bg="light sky blue", fg="red", height=2, width=15)
        button1.grid(row=33, column=0, columnspan=50, padx=50)
        button1.place(x=310, y=480)
        button1 = tk.Button(self, text="Thoát", command=lambda: self.controller.destroy(), font="fontNomal",
                            bg="light sky blue", fg="red", height=2, width=15)
        button1.grid(row=34, column=0, columnspan=50, padx=50)
        button1.place(x=520, y=480)

    def checkUserName(self):
        if self.newId.get() == "None":
            messagebox.showerror("Có lỗi xảy ra", "Username không được để trống")
            return False
        if self.newPassword.get() == "None":
            messagebox.showerror("Có lỗi xảy ra", "Password không được để trống")
            return False

    def register_data(self):
        if self.checkUserName():
            con = sqlite3.connect("C:/Users/admin/OneDrive/Máy tính/AI (2)/AI/OpenCV/db.db")
            cur = con.cursor()
            sql = "SELECT user_id,password FROM user"
            rows = cur.excute(sql)
            # for row in rows

            con.commit()
            con.close()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        imageBg = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/OpenCV/image/img1.jpg').resize((700, 700)))
        backgroundLabel = tk.Label(self, image=imageBg, width=800, height=800)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100, sticky="nsew")

        imageBg1 = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/matma.jpg').resize((130, 130)))
        backgroundLabel = tk.Label(self, image=imageBg1, width=100, height=1000)
        backgroundLabel.image = imageBg1
        backgroundLabel.grid(row=0, column=1, rowspan=100, sticky="nsew")
        backgroundLabel.place(x=970, y=-420)

        titleApp = tk.Label(self, text="Ứng dụng điểm danh lớp học", font=self.controller.title_font, fg="#263942")
        titleApp.grid(row=40, column=1, sticky="nsew", columnspan=100)

        button2 = tk.Button(self, text="Chọn Danh Sách Lớp ", command=lambda: controller.show_frame("PageTwo"),
                            font="fontNomal", fg="#000000", bg="#33FF00", height=2, width=30)
        button2.grid(row=50, column=1, columnspan=5, sticky="nsew", padx=50)
        button3 = tk.Button(self, text="Thêm Sinh Viên", command=lambda: showFrameAddStudent(), font="fontNomal",
                            fg="#000000", bg="#33FF00", height=2, width=30)
        button3.grid(row=55, column=1, columnspan=5, sticky="nsew", padx=50)
        button4 = tk.Button(self, text="Thêm Dữ Liệu Khuôn Mặt", command=lambda: addDataTrainFace(), font="fontNomal",
                            fg="#000000", bg="#33FF00", height=2, width=30)
        button4.grid(row=60, column=1, columnspan=5, sticky="nsew", padx=50)
        button5 = tk.Button(self, text="Điểm Danh", command=lambda: attendanceStudent(), font="fontNomal", fg="#000000",
                            bg="#33FF00", height=2, width=30)
        button5.grid(row=65, column=1, columnspan=5, sticky="nsew", padx=50)
        # button6 = tk.Button(self, text="Danh Sách Sinh Viên",command=lambda: controller.show_frame("PageDanhSach"), font="fontNomal", fg="#000000", bg="#33FF00",height=2,width=30)
        # button6.grid(row = 70,column = 1,columnspan=5, sticky="nsew", padx=50)
        button6 = tk.Button(self, text="Thoát", command=lambda: controller.show_frame("StartPage"), font="fontNomal",
                            fg="#000000", bg="#AAAAAA", height=2, width=30)
        button6.grid(row=70, column=1, columnspan=5, sticky="nsew", padx=50)

        def showFrameAddStudent():
            if filePathClass != "":
                self.controller.show_frame("PageSV")
            else:
                messagebox.showerror("Có lỗi xảy ra", "Vui lòng chọn danh sách lớp")
                return

        def addDataTrainFace():
            if checkFileClass():
                numberSvTrain = len(listStudentDataFrame.loc[listStudentDataFrame['Trained'] <= 0]);
                if numberSvTrain == 0:
                    messagebox.showerror("Có lỗi xảy ra", "Tất cả sinh viên đã được thêm dữ liệu")
                    return
                self.controller.frames["PageData"].getListStudent()
                self.controller.show_frame("PageData")

        def attendanceStudent():
            if checkFileClass():
                numberSvTrain = len(listStudentDataFrame.loc[listStudentDataFrame['Trained'] > 0]);
                if numberSvTrain == 0:
                    messagebox.showerror("Có lỗi xảy ra", "Chưa sinh viên nào được thêm dữ liệu")
                    return;
                else:
                    # self.controller.frames["PageDiemDanh"].getListStudent()
                    self.controller.show_frame("PageDiemDanh")

        def checkFileClass():
            global filePathClass, fileNameClass, listStudentDataFrame
            if filePathClass == "":
                messagebox.showerror("Có lỗi xảy ra", "Vui lòng chọn danh sách lớp")
                return False
            if len(listStudentDataFrame) <= 0:
                messagebox.showerror("Có lỗi xảy ra", "Chưa có sinh viên trong danh sách")
                return False
            return True


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        imageBg = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/OpenCV/image/trangchu.jpg').resize((700, 700)))
        backgroundLabel = tk.Label(self, image=imageBg, width=800, height=800)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100, sticky="nsew")

        imageBg1 = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/matma.jpg').resize((130, 130)))
        backgroundLabel = tk.Label(self, image=imageBg1, width=100, height=1000)
        backgroundLabel.image = imageBg1
        backgroundLabel.grid(row=0, column=1, rowspan=100, sticky="nsew")```````````````````````````````````````````````````````````````````````````````````````````````
        backgroundLabel.place(x=970, y=-420)

        titleApp = tk.Label(self, text="Ứng dụng điểm danh lớp học", font=self.controller.title_font, fg="#263942")
        titleApp.grid(row=27, column=1, sticky="nsew", columnspan=1000)
        label2 = tk.Label(self, text="Chọn Danh Sách Lớp ", font="fontNomal", fg="#263942")
        label2.grid(row=30, column=1, columnspan=5, sticky="nsew", padx=50)
        fontNomalUnderLine = tkfont.Font(family='Helvetica', size=13)
        fontNomalUnderLine.configure(underline=True)

        nameListStudent = tk.Label(self, text="chưa chọn danh sách", font=fontNomalUnderLine)
        nameListStudent.grid(row=32, column=1, columnspan=10, rowspan=1)

        lable = tk.Label(self, text="Tên môn", font=('Helvetica', 18))
        lable.place(x=800, y=300)
        self.newSubject = tk.Entry(self, borderwidth=0, bg="#FFFFCC", font=('Helvetica', 18), width=20,
                                   justify="center")
        self.newSubject.place(x=910, y=300)
````````````````
        lable1 = tk.Label(self, text="Lớp", font=('Helvetica', 18), justify="center")
        lable1.place(x=820, y=350)
        self.newClass = tk.Entry(self, borderwidth=0, bg="#FFFFCC", font=('Helvetica', 18), width=20, justify="center")
        self.newClass.place(x=910, y=350)

        button2 = tk.Button(self, text="Chọn", command=lambda: chooseFileClass(), font="fontNomal", fg="#000000",
                            bg="#33FF99", height=2, width=30)
        button2.grid(row=57, column=1, columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Trang chủ", command=lambda: controller.show_frame("PageOne"), font="fontNomal",
                            fg="#000000", bg="#33FF99", height=2, width=30)
        button2.grid(row=62, column=1, columnspan=5, sticky="nsew", padx=50)

        def checkClass():
            if self.newClass == "None" or len(self.newClass.get()) == 0:
                messagebox.showerror("Có lỗi xảy ra", "Mã lớp không được để trống")
                return False
            if self.newSubject == "None" or len(self.newSubject.get()) == 0:
                messagebox.showerror("Có lỗi xảy ra", "Tên môn học không được để trống")
                return False

        def chooseFileClass():
            file = filedialog.askopenfile(mode='r', filetypes=[("Excel files", "*.xlsx")])
            if file is not None:
                global filePathClass, fileNameClass, listStudentDataFrame
                self.newClass.delete(0, len(self.newClass.get()))
                self.newSubject.delete(0, len(self.newSubject.get()))
                filePathClass = file.name
                fileNameFolder = file.name.split("/")
                fileName = fileNameFolder[len(fileNameFolder) - 1]
                nameListStudent.config(text=fileName)
                subject = fileName.split(".")[0]
                clas = fileName.split(".")[1]
                self.newSubject.insert(0, subject)
                self.newClass.insert(0, clas)
                fileNameClass = fileName
                listStudentDataFrame = pd.read_excel(filePathClass);
                checkColumnTrainData()
                checkColumnDate()

        def checkColumnTrainData():
            columns = list(listStudentDataFrame.columns)
            checkColumn = "Trained" in columns
            if not checkColumn:
                listStudentDataFrame['Trained'] = None
                if len(listStudentDataFrame) > 0:
                    listStudentDataFrame['Trained'] = 0;
                self.controller.saveExcel()
            else:
                listStudentDataFrame.loc[listStudentDataFrame['Trained'] != 1, ['Trained']] = 0
                self.controller.saveExcel()

        def checkColumnDate():
            global filePathClass, fileNameClass, listStudentDataFrame
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            columnNames = set()
            for col in listStudentDataFrame.columns:
                if isinstance(col, datetime.datetime):
                    columnNames.add(col.strftime('%Y-%m-%d'))
                else:
                    columnNames.add(col)
            isTodayInList = date in columnNames
            if not isTodayInList:
                listStudentDataFrame[date] = None
                self.controller.saveExcel()


class PageSV(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        imageBg = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/OpenCV/image/img4.jpg').resize((500, 500)))
        backgroundLabel = tk.Label(self, image=imageBg, width=800, height=800)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100, sticky="nsew")

        imageBg1 = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/matma.jpg').resize((130, 130)))
        backgroundLabel = tk.Label(self, image=imageBg1, width=100, height=1000)
        backgroundLabel.image = imageBg1
        backgroundLabel.grid(row=0, column=1, rowspan=100, sticky="nsew")
        backgroundLabel.place(x=900, y=-420)

        titleApp = tk.Label(self, text="Ứng dụng điểm danh lớp học", font=self.controller.title_font, fg="#263942")
        titleApp.grid(row=30, column=1, sticky="nsew", columnspan=1000)
        titleApp.place(x=790, y=160)

        lable3 = tk.Label(self, text="Điền thông tin sinh viên", font=self.controller.title_font, fg="#263942")
        # lable3.grid(row=20, column=1, sticky="nsew",columnspan=1000)
        lable3.place(x=830, y=220)

        lable = tk.Label(self, text=" Mã sinh viên", font=('Helvetica', 20))
        lable.place(x=700, y=310)
        self.newId = tk.Entry(self, borderwidth=0, bg="#FFFFCC", font=('Helvetica', 18), width=25, justify="center")
        # self.newId.grid(row=30, column=1,  padx=50)
        self.newId.place(x=890, y=310)

        lable1 = tk.Label(self, text=" Tên sinh viên", font=('Helvetica', 20))
        lable1.place(x=700, y=360)
        self.newUserName = tk.Entry(self, borderwidth=0, bg="#FFFFCC", font=('Helvetica', 18), width=25,
                                    justify="center")
        self.newUserName.grid(row=33, column=1, padx=50)
        self.newUserName.place(x=890, y=360)

        lable2 = tk.Label(self, text="Tên Lớp", font=('Helvetica', 20))
        lable2.place(x=710, y=410)
        self.newClass = tk.Entry(self, borderwidth=0, bg="#FFFFCC", font=('Helvetica', 18), width=25, justify="center")
        self.newClass.grid(row=37, column=1, padx=50)
        self.newClass.place(x=890, y=410)

        button2 = tk.Button(self, text="Thêm sinh viên vào danh sách", command=lambda: self.addStudent(),
                            font="fontNomal", fg="#000000", bg="#33FF99", height=2, width=30)
        button2.grid(row=68, column=1, columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Trang chủ", command=lambda: controller.show_frame("PageOne"), font="fontNomal",
                            fg="#000000", bg="#33FF99", height=2, width=30)
        button2.grid(row=73, column=1, columnspan=5, sticky="nsew", padx=50)

    def checkUserName(self):
        if self.newId.get() == "None" or len(self.newId.get()) == 0:
            messagebox.showerror("Có lỗi xảy ra", "Mã Sinh Viên không được để trống")
            return False
        numberSv = len(listStudentDataFrame.loc[listStudentDataFrame['Mã Sinh Viên'] == self.newId.get()]);
        if numberSv > 0:
            messagebox.showerror("Có lỗi xảy ra", "Mã sinh viên đã tồn tại")
            return False
        if self.newUserName.get() == "None" or len(self.newUserName.get()) == 0:
            messagebox.showerror("Có lỗi xảy ra", "Tên không được để trống")
            return False
        if self.newClass.get() == "None" or len(self.newClass.get()) == 0:
            messagebox.showerror("Có lỗi xảy ra", "Lớp không được để trống")
            return False
        return True

    def addStudent(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        if self.checkUserName():
            listStudentDataFrame.loc[len(listStudentDataFrame), ['Mã Sinh Viên', 'Họ Và Tên', 'Lớp', 'Trained']] = [ self.newId.get(),self.newUserName.get(), self.newClass.get()] + [0]
            self.controller.saveExcel()
            messagebox.showinfo("Thành công", "Thêm mới sinh viên thành công")
            # self.newUserName.delete(0,len(self.newUserName.get()))
            # self.newClass.delete(0,len(self.newClass.get()))
            # self.newId.delete(0,len(self.newId.get()))
            conn = sqlite3.connect("D:/Test/AI (1)/AI/OpenCV/test.db")
            cursor = conn.execute("SELECT * FROM student where msv = ' " + str(self.newId.get()) + "'")
            isRecordExist = 0
            for row in cursor:
                isRecordExist = 1
                break

            if isRecordExist == 1:
                cmd = "UPDATE student SET hoten=' " + str(self.newUserName.get()) + " ' WHERE msv= ' " + str(
                    self.newId.get()) + "'"
            else:
                cmd = "INSERT INTO student(msv,hoten,lop) Values(' " + str(self.newId.get()) + "',' " + str(
                    self.newUserName.get()) + " ' , ' " + str(self.newClass.get()) + " ' )"

            conn.execute(cmd)
            conn.commit()
            conn.close()
            self.newUserName.delete(0, len(self.newUserName.get()))
            self.newClass.delete(0, len(self.newClass.get()))
            self.newId.delete(0, len(self.newId.get()))


class PageData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        imageBg = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/OpenCV/image/img2.jpg').resize((500, 500)))
        backgroundLabel = tk.Label(self, image=imageBg, width=800, height=800)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100, sticky="nsew")

        imageBg1 = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/matma.jpg').resize((130, 130)))
        backgroundLabel = tk.Label(self, image=imageBg1, width=100, height=1000)
        backgroundLabel.image = imageBg1
        backgroundLabel.grid(row=0, column=1, rowspan=100, sticky="nsew")
        backgroundLabel.place(x=970, y=-420)

        titleApp = tk.Label(self, text="Ứng dụng điểm danh lớp học", font=self.controller.title_font, fg="#263942")
        titleApp.grid(row=30, column=1, sticky="nsew", columnspan=1000)

        titleApp = tk.Label(self, text="Thêm dữ liệu khuôn mặt", font=self.controller.title_font, fg="#263942")
        titleApp.grid(row=35, column=1, sticky="nsew", columnspan=1000)
        self.activeNameStudent = tk.StringVar(self)
        # tk.Label(self, text="Chọn sinh viên", font =('Helvetica', 18)).grid(row=38, column=1)
        # self.activeNameStudent = tk.Entry(self, borderwidth=0, bg="#FFFFCC", font =('Helvetica', 18), width=25,justify="center")
        # self.activeNameStudent.grid(row=42, column=1,  padx=50)

        button2 = tk.Button(self, text="Thêm khuôn mặt", command=lambda: self.addCapture(), fg="#000000", bg="#33FF99",height=2, font="fontNomal", width=30)
        button2.grid(row=50, column=1, columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Train dữ liệu", command=lambda: self.trainClassifer(), fg="#000000", bg="#33FF99",height=2, font="fontNomal", width=30)
        button2.grid(row=55, column=1, columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Trang chủ", command=lambda: controller.show_frame("PageOne"), font="fontNomal",fg="#000000", bg="#33FF99", height=2, width=30)
        button2.grid(row=60, column=1, columnspan=5, sticky="nsew", padx=50)

    def getListStudent(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        fontNomal = tkfont.Font(family='Helvetica', size=13)
        menu = tk.Label(self, text=" Chọn sinh viên", font=('Helvetica', 18))
        menu.grid(row=38, column=1, columnspan=1000)
        listStudent = listStudentDataFrame.loc[listStudentDataFrame['Trained'] == 0, ['Mã Sinh Viên']]['Mã Sinh Viên'].tolist()
        self.activeNameStudent.set(listStudent[0])
        self.dropdown = tk.OptionMenu(self, self.activeNameStudent, *listStudent)
        self.dropdown.config(bg="lightgrey", width=20, height=2, font=fontNomal)
        self.dropdown["menu"].config(bg="lightgrey", font=fontNomal)
        self.dropdown.grid(row=40, column=1, columnspan=1000)

    def addCapture(self):
        if self.activeNameStudent.get() == "None" or len(self.activeNameStudent.get()) == 0:
            messagebox.showerror("Lỗi", "Tên không được để trống")
            return
        # nameStudent = no_accent_vietnamese(self.activeNameStudent.get());
        nameStudent = self.activeNameStudent.get();
        # name = listStudentDataFrame.loc[listStudentDataFrame['Mã Sinh Viên']== nameStudent,['STT']]['STT'].tolist()[0]
        conn = sqlite3.connect("D:/Test/AI (1)/AI/OpenCV/test.db")
        query = "SELECT id FROM student where msv =' " + nameStudent + "'"
        cursor = conn.execute(query)
        profile = None
        for row in cursor:
            # print(row)
            profile = row[0]
        conn.close()

        print(profile)

        path = "./path1/" + nameStudent;
        test = "./path1/test"
        sampleNum = 0
        detector = cv2.CascadeClassifier("D:/Test/AI (1)/AI/OpenCV/data/haarcascade_frontalface_alt.xml")
        print(path)
        try:
            os.makedirs(path)
        except:
            print('Directory Already Created')
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = detector.detectMultiScale(gray, 1.3, 5)
            for x, y, w, h in face:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "Face Detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                print()
                cv2.putText(frame, str(str(sampleNum) + " images captured"), (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255))

            cv2.imshow("FaceDetection", frame)
            key = cv2.waitKey(10) & 0xFF
            try:
                cv2.imwrite(str(path + "/" + str(sampleNum) + '_' + nameStudent + ".jpg"),gray[y: y + h, x: x + w])
                #cv2.imwrite(str(path + "/" + str(sampleNum) + '_' + nameStudent + '_' + str(profile) + ".jpg"),frame)
                sampleNum += 1
            except:
                pass
            if (key == ord("q") or sampleNum > 300):
                break
        cv2.destroyAllWindows()
        messagebox.showinfo("Thành công", "Lấy dữ liệu ảnh thành công")

    def trainClassifer(self):     
        global filePathClass, fileNameClass, listStudentDataFrame
        nameStudent = no_accent_vietnamese(self.activeNameStudent.get()).replace(" ", "_");

        # clf = cv2.face.LBPHFaceRecognizer_create()
        # detector = cv2.CascadeClassifier("D:/Test/AI (1)/AI/OpenCV/data/haarcascade_frontalface_alt.xml")

        def train(data_dir,
                  model,
                  classifier_filename,
                  use_split_dataset=None,
                  batch_size=1000,
                  image_size=160,
                  seed=123,
                  min_nrof_images_per_class=20,
                  nrof_train_images_per_class=10):

            with tf.compat.v1.Graph().as_default():
                with tf.compat.v1.Session() as sess:
                    np.random.seed(seed=seed)
                    if not use_split_dataset:
                        dataset = facenet.facenet.get_dataset(data_dir)
                    else:
                        dataset_tmp = facenet.facenet.get_dataset(data_dir)
                        train_set, test_set = split_dataset(dataset_tmp, min_nrof_images_per_class, nrof_train_images_per_class)
                        dataset = train_set

                    # Check that there are at least one training image per class
                    for cls in dataset:
                        assert (len(cls.image_paths) > 0, 'There must be at least one image for each class in the dataset')

                    paths, labels = facenet.facenet.get_image_paths_and_labels(dataset)

                    #print('Number of classes: %d' % len(dataset))
                    #print('Number of images: %d' % len(paths))

                    # Load the model
                    print('Loading feature extraction model')
                    facenet.facenet.load_model(model)

                    # Get input and output tensors
                    images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
                    embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
                    phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
                    embedding_size = embeddings.get_shape()[1]

                    # Run forward pass to calculate embeddings
                    print('Calculating features for images')
                    nrof_images = len(paths)
                    nrof_batches_per_epoch = int(math.ceil(1.0 * nrof_images / batch_size))
                    emb_array = np.zeros((nrof_images, embedding_size))
                    for i in range(nrof_batches_per_epoch):
                        start_index = i * batch_size
                        end_index = min((i + 1) * batch_size, nrof_images)
                        paths_batch = paths[start_index:end_index]
                        images = facenet.facenet.load_data(paths_batch, False, False, image_size)
                        feed_dict = {images_placeholder: images, phase_train_placeholder: False}
                        emb_array[start_index:end_index, :] = sess.run(embeddings, feed_dict=feed_dict)

                    classifier_filename_exp = os.path.expanduser(classifier_filename)

                    # Train classifier
                    print('Training classifier')
                    model = SVC(kernel='linear', probability=True)
                    model.fit(emb_array, labels)

                    # Create a list of class names
                    class_names = [cls.name.replace('_', ' ') for cls in dataset]

                    # Saving classifier model
                    with open(classifier_filename_exp, 'wb') as outfile:
                        pickle.dump((model, class_names), outfile)
                    print('Saved classifier model to file "%s"' % classifier_filename_exp)

        def split_dataset(dataset, min_nrof_images_per_class, nrof_train_images_per_class):
            train_set = []
            test_set = []
            for cls in dataset:
                paths = cls.image_paths
                # Remove classes with less than min_nrof_images_per_class
                if len(paths) >= min_nrof_images_per_class:
                    np.random.shuffle(paths)
                    train_set.append(facenet.facenet.ImageClass(cls.name, paths[:nrof_train_images_per_class]))
                    test_set.append(facenet.facenet.ImageClass(cls.name, paths[nrof_train_images_per_class:]))
            return train_set, test_set

        if __name__ == '__main__':
            align_mtcnn('path1', 'face_align')
            train('face_align/', 'models/20180402-114759.pb', 'models/train_model.pkl')

        # clf.save("./path/train_classifier.yml")
        listStudentDataFrame.loc[listStudentDataFrame['Mã Sinh Viên'] == self.activeNameStudent.get(), ['Trained']] = [1];
        self.controller.saveExcel()
        messagebox.showinfo("Thành công", "Train dữ liệu thành công")
        self.controller.show_frame("PageOne")


class PageDiemDanh(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        imageBg = ImageTk.PhotoImage(Image.open('D:/Test/AI (1)/AI/matma.jpg').resize((500, 500)))
        backgroundLabel = tk.Label(self, image=imageBg, width=800, height=800)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100, sticky="nsew")

        titleApp = tk.Label(self, text="Ứng dụng điểm danh lớp học", font=self.controller.title_font, fg="#263942")
        titleApp.grid(row=15, column=1, sticky="nsew", columnspan=1000)
        # self.activeNameStudent = tk.StringVar(self)
        # tk.Label(self, text="Chọn sinh viên", font =('Helvetica', 18)).grid(row=25, column=1)
        # self.activeNameStudent = tk.Entry(self, borderwidth=0, bg="lightgrey", font =('Helvetica', 18), width=25,justify="center")
        # self.activeNameStudent.grid(row=27, column=1,  padx=50)
        # self.activeNameStudent.place(x =700, y = 150)
        button2 = tk.Button(self, text="Điểm danh", command=lambda: self.attendance(), fg="#000000", bg="#33FF99",
                            height=2, font="fontNomal", width=30, activebackground="white")
        button2.grid(row=40, column=1, columnspan=5, sticky="nsew", padx=50)
        button2 = tk.Button(self, text="Trang chủ", command=lambda: controller.show_frame("PageOne"), font="fontNomal",
                            fg="#000000", bg="#33FF99", height=2, width=30)
        button2.grid(row=45, column=1, columnspan=5, sticky="nsew", padx=50)

    def getListStudent(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        fontNomal = tkfont.Font(family='Helvetica', size=13)
        tk.Label(self, text="Chọn sinh viên", font=('Helvetica', 18)).grid(row=29, column=3)
        listStudent = listStudentDataFrame.loc[listStudentDataFrame['Trained'] == 1, ['Mã Sinh Viên']]['Mã Sinh Viên'].tolist()
        self.activeNameStudent.set(listStudent[0])
        self.dropdown = tk.OptionMenu(self, self.activeNameStudent, *listStudent)
        self.dropdown.config(bg="lightgrey", width=26, height=2, font="fontNomal")
        self.dropdown["menu"].config(bg="lightgrey", font="fontNomal")
        self.dropdown.grid(row=30, column=3)

    def faceDetection(frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(r'D:/Test/AI (1)/AI/OpenCV/data/haarcascade_frontalface_alt.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces, gray

    def attendance(self):
        global filePathClass, fileNameClass, listStudentDataFrame
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        #recognizer.read(f"./path/train_classifier.yml")
        face_cascade = cv2.CascadeClassifier("D:/Test/AI (1)/AI/OpenCV/data/haarcascade_frontalface_alt.xml")
        # cap = cv2.VideoCapture(0)
        pred = 0
        class_id = ' '
        profile = None

        def getProfile(class_id):
            conn = sqlite3.connect("D:/Test/AI (1)/AI/OpenCV/test.db")
            cursor = conn.execute("SELECT * FROM student where msv =' " + class_id +"'")
            profile = None
            for row in cursor:
                profile = row
            conn.close()
            return profile

        cap = cv2.VideoCapture(0)
        def add_overlays(frame, faces, colors, confidence=0.7,name =''):
            if faces is not None:
                for idx, face in enumerate(faces):
                    face_bb = face.bounding_box.astype(int)
                    cv2.rectangle(frame, (face_bb[0], face_bb[1]), (face_bb[2], face_bb[3]), colors[idx], 2)
                    if face.name and face.prob:
                        #print(confidence)
                        if face.prob > 0.7:
                            
                            ids = face.name
                            class_id = no_accent_vietnamese(ids).upper();
                            #profile = getProfile(class_id)
                            #print(profile)
                            name = listStudentDataFrame.loc[listStudentDataFrame['Mã Sinh Viên']== class_id,['Họ Và Tên']]['Họ Và Tên'].tolist()[0]
                            #text = str(profile[1])
                            #name = str(profile[2])
                            #text = text.split(" ")[1]
                            #text = no_accent_vietnamese(text).upper()
                            nameStudent = no_accent_vietnamese(name).upper()
                            cv2.putText(frame, nameStudent, (face_bb[0], face_bb[3] ), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,255,0), thickness=2, lineType=2)
                            cv2.putText(frame, class_id, (face_bb[0], face_bb[3] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0,255,0), thickness=2, lineType=2)
                            cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 40),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), thickness=1, lineType=2)
                            ts = time.time()   
                            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d');
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                           
                            listStudentDataFrame.loc[listStudentDataFrame['Mã Sinh Viên'] == class_id,[date]] = [1];
                        else:
                            class_name = 'Unknown'
                            cv2.putText(frame,class_name, (face_bb[0], face_bb[3]+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), thickness = 2, lineType=2)
                            cv2.putText(frame, '{:.02f}'.format(face.prob * 100), (face_bb[0], face_bb[3] + 40),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), thickness=1, lineType=2)
                        if(face.prob < 0.25):
                            noOfFile = len(os.listdir("ImagesUnknown"))+1
                            cv2.imwrite("ImagesUnknown\Image"+ str(noOfFile) + ".jpg",frame[face_bb[1]:face_bb[3] ,face_bb[0] :face_bb[2]])  
                    
           
        def run(model_checkpoint, classifier, video_file=None, output_file=None):
            frame_interval = 1  # Number of frames after which to run face detection
            fps_display_interval = 5  # seconds
            frame_rate = 0
            frame_count = 0
            if video_file is not None:
                video_capture = cv2.VideoCapture(video_file)
            else:
                # Use internal camera
                video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()
            width = frame.shape[1]
            height = frame.shape[0]
            if output_file is not None:
                video_format = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(output_file, video_format, 20, (width, height))
            face_recognition = Recognition(model_checkpoint, classifier)
            #start_time = time.time()
            colors = np.random.uniform(0, 255, size=(1, 3))
            while True:
                # Capture frame-by-frame
                ret, frame = video_capture.read()

                if (frame_count % frame_interval) == 0:
                    faces = face_recognition.identify(frame)
                    for i in range(len(colors), len(faces)):
                        colors = np.append(colors, np.random.uniform(0, 255, size=(1, 3)), axis=0)
                   

                add_overlays(frame, faces, colors)

                #frame_count += 1
                cv2.imshow('Video', frame)
                if output_file is not None:
                    out.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # When everything is done, release the capture
            if output_file is not None:
                out.release()
            self.controller.saveExcel(); 
            video_capture.release()
            cv2.destroyAllWindows()


        if __name__ == '__main__':
            run('models', 'models/train_model.pkl', video_file=None, output_file='demo.avi')

class PageDanhSach(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        imageBg = ImageTk.PhotoImage(Image.open('D:/AI (2)/AI/OpenCV/image/matma.jpg').resize((500, 500)))
        backgroundLabel = tk.Label(self, image=imageBg, width=800, height=800)
        backgroundLabel.image = imageBg
        backgroundLabel.grid(row=0, column=0, rowspan=100, sticky="nsew")

        titleApp = tk.Label(self, text="Ứng dụng điểm danh lớp học", font=self.controller.title_font, fg="#263942")
        titleApp.grid(row=15, column=1, sticky="nsew", columnspan=1000)
        button6 = tk.Button(self, text="Trang chủ", command=lambda: controller.show_frame("PageOne"), font="fontNomal",
                            fg="#ffffff", bg="#007bff", height=2, width=30)
        button6.grid(row=55, column=1, columnspan=5, sticky="nsew", padx=50)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

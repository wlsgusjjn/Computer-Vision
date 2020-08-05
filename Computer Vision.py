from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np
import math


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(800, 400)

        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, columnspan = 4, row = 1, padx = 20, pady = 20, sticky="ew")

        self.button()

        self.exist = 0
        self.count = 0
        self.pipe = 0
        self.size = 3
        self.order = 0

    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)

    def fileDialog(self):        
        self.filename = filedialog.askopenfilename(initialdir =  "./", title = "Select A File", filetype =
        (("jpeg files","*.jpg"),("png files","*.png"),("all files","*.*")) )
        if self.exist != 0:
            self.resultL.destroy()
            self.label.destroy()
            self.exist = 0
        self.origin = Image.open(self.filename).convert('RGB')            
        self.gray = Image.open(self.filename).convert('LA')

        self.w, self.h = self.origin.size
        
        if self.w > 320:
            self.origin = self.origin.resize((320,int(self.h * 320/self.w)))
            self.gray = self.gray.resize((320,int(self.h * 320/self.w)))
            self.img = ImageTk.PhotoImage(Image.open(self.filename).resize((320,int(self.h * 320/self.w))))
        else:
            self.img = ImageTk.PhotoImage(Image.open(self.filename))
            
        self.label = ttk.Label(self.labelFrame)
        self.label["image"] = self.img
        self.label.grid(row = 2, column = 1)

        if self.count == 0:

            self.button = ttk.Button(self, text = "mean",command = self.mean)
            self.button.grid(column = 0, row = 2)

            self.button = ttk.Button(self, text = "median",command = self.median)
            self.button.grid(column = 1, row = 2)

            self.button = ttk.Button(self, text = "sobel",command = self.sobel)
            self.button.grid(column = 2, row = 2)

            self.button = ttk.Button(self, text = "log",command = self.log)
            self.button.grid(column = 3, row = 2)

            self.labelR = Label(root,text="")
            self.labelR.grid(column = 4, row = 2)

            self.sz = Label(root,text="3x3")
            self.sz.grid(column = 1, row = 3)

            self.ch = Checkbutton(root,text="Pipe",command = self.pipeLine)
            self.ch.grid(column = 0, row = 3)

            self.three = ttk.Button(self, text = "3x3",command = self.three)
            self.three.grid(column = 2, row = 3)

            self.five = ttk.Button(self, text = "5x5",command = self.five)
            self.five.grid(column = 3, row = 3)

            self.seven = ttk.Button(self, text = "7x7",command = self.seven)
            self.seven.grid(column = 4, row = 3)

    def pipeLine(self):
        if self.pipe == 0 :
            self.pipe = 1
        else:
            self.pipe = 0

    def three(self):
        self.size = 3
        self.order = 0
        self.sz['text'] = "3x3"

    def five(self):
        self.size = 5
        self.order = 1
        self.sz['text'] = "5x5"

    def seven(self):
        self.size = 7
        self.order = 2
        self.sz['text'] = "7x7"

    def mean(self):
        self.labelR['text'] = ""
        
        if self.pipe == 0:
            self.pixelMap = self.origin.load()
        else:
            self.pixelMap = self.rimg.load()

        self.rimg = Image.new(self.origin.mode,self.origin.size)
        self.pixelsNew = self.rimg.load()

        a = (self.size - 1) // 2;

        for i in range(self.origin.size[0]):
            for j in range(self.origin.size[1]):
                r = 0
                g = 0
                b = 0
                sum = 0
                for k in range(i-a,i+a+1):
                    for l in range(j-a,j+a+1):
                        if k > -1 and l > -1 and k < self.origin.size[0] and l < self.origin.size[1]:
                            temp = list(self.pixelMap[k,l]) 
                            r += temp[0]
                            g += temp[1]
                            b += temp[2]
                            sum += 1
                r //= sum
                g //= sum
                b //= sum

                self.pixelsNew[i,j] = (r,g,b)
                
        self.result = ImageTk.PhotoImage(self.rimg)
        self.resultL = ttk.Label(self)
        self.resultL["image"] = self.result
        self.resultL.grid(row = 1, column = 6, columnspan = 1)
        self.exist = 1
        self.count += 1

        self.labelR['text'] = "mean"

    def median(self):
        self.labelR['text'] = ""
        
        if self.pipe == 0:
            self.pixelMap = self.origin.load()
        else:
            self.pixelMap = self.rimg.load()

        self.rimg = Image.new(self.origin.mode,self.origin.size)
        self.pixelsNew = self.rimg.load()

        a = (self.size - 1) // 2;

        for i in range(self.origin.size[0]):
            for j in range(self.origin.size[1]):
                list_r = []
                list_g = []
                list_b = []
                sum = 0
                for k in range(i-a,i+a+1):
                    for l in range(j-a,j+a+1):
                        if k > -1 and l > -1 and k < self.origin.size[0] and l < self.origin.size[1]:                    
                            temp = list(self.pixelMap[k,l])
                    
                            if len(list_r) == 0:
                                list_r.append(temp[0])
                                list_g.append(temp[1])
                                list_b.append(temp[2])
                                continue
                    
                            for m in range(len(list_r)):
                                if temp[0] <= list_r[m] :
                                    list_r.insert(m,temp[0])
                                    break
                                else:
                                    if m == len(list_r) - 1:
                                        list_r.append(temp[0])
                                        break
                                    else:
                                        continue
                            for m in range(len(list_g)):
                                if temp[1] <= list_g[m] :
                                    list_g.insert(m,temp[1])
                                    break
                                else:
                                    if m == len(list_g) - 1:
                                        list_g.append(temp[1])
                                        break
                                    else:
                                        continue
        
                            for m in range(len(list_b)):
                                if temp[2] <= list_b[m] :
                                    list_b.insert(m,temp[2])
                                    break
                                else:
                                    if m == len(list_b) - 1:
                                        list_b.append(temp[2])
                                        break
                                    else:
                                        continue

                            sum += 1



                    
                if(sum % 2 ==0):
                    r = (list_r[sum//2] + list_r[sum//2 - 1])//2
                    g = (list_g[sum//2] + list_g[sum//2 - 1])//2
                    b = (list_b[sum//2] + list_b[sum//2 - 1])//2
                else:
                    r = list_r[sum//2]
                    g = list_g[sum//2]
                    b = list_b[sum//2]

                self.pixelsNew[i,j] = (r,g,b)
                
        self.result = ImageTk.PhotoImage(self.rimg)
        self.resultL = ttk.Label(self)
        self.resultL["image"] = self.result
        self.resultL.grid(row = 1, column = 5, columnspan = 4)
        self.exist = 1
        self.count += 1

        self.labelR['text'] = "median"

    def sobel(self):
        self.labelR['text'] = ""
        
        if self.pipe == 0:
            self.pixelMap = self.gray.load()
        else:
            self.pixelMap = self.rimg.load()

        self.rimg = Image.new(self.gray.mode,self.gray.size)
        self.pixelsNew = self.rimg.load()

        xfilter = [[[-1,0,1],
                   [-2,0,2],
                   [-1,0,1]],
                   [[-1,-1,0,1,1],
                    [-1,-1,0,1,1],
                    [-2,-2,0,2,2],
                    [-1,-1,0,1,1],
                    [-1,-1,0,1,1]],
                   [[-1,-1,-1,0,1,1,1],
                    [-1,-1,-1,0,1,1,1],
                    [-1,-1,-1,0,1,1,1],
                    [-2,-2,-2,0,2,2,2],
                    [-1,-1,-1,0,1,1,1],
                    [-1,-1,-1,0,1,1,1],
                    [-1,-1,-1,0,1,1,1]]]

        yfilter = [[[1,2,1],
                   [0,0,0],
                   [-1,-2,-1]],
                   [[1,1,2,1,1],
                    [1,1,2,1,1],
                    [0,0,0,0,0],
                    [-1,-1,-2,-1,-1],
                    [-1,-1,-2,-1,-1]],
                   [[1,1,1,2,1,1,1],
                    [1,1,1,2,1,1,1],
                    [1,1,1,2,1,1,1],
                    [0,0,0,0,0,0,0],
                    [-1,-1,-1,-2,-1,-1,-1],
                    [-1,-1,-1,-2,-1,-1,-1],
                    [-1,-1,-1,-2,-1,-1,-1]]]

        a = (self.size - 1) // 2

        for i in range(self.origin.size[0]):
            for j in range(self.origin.size[1]):
                x = 0
                y = 0
                for k in range(-a,a+1):
                    for l in range(-a,a+1):
                        if i+k > -1 and j+l > -1 and i+k < self.origin.size[0] and j+l < self.origin.size[1]:
                            temp = self.pixelMap[i+k,j+l]

                            x += temp[0]*xfilter[self.order][k+1][l+1]
                            y += temp[0]*yfilter[self.order][k+1][l+1] 
                                    
                grayV = int(abs(x)+abs(y))

                if grayV > 240:
                    grayV = 255
                else:
                    grayV = 0

                self.pixelsNew[i,j] = (grayV,255)
                
        self.result = ImageTk.PhotoImage(self.rimg)
        self.resultL = ttk.Label(self)
        self.resultL["image"] = self.result
        self.resultL.grid(row = 1, column = 5, columnspan = 4)
        self.exist = 1
        self.count += 1

        self.labelR['text'] = "sobel"

    def log(self):
        self.labelR['text'] = ""
        
        if self.pipe == 0:
            self.pixelMap = self.gray.load()
        else:
            self.pixelMap = self.rimg.load()

        self.gau = Image.new(self.gray.mode,self.gray.size)
        self.pixelsGau = self.gau.load()

        self.rimg = Image.new(self.gray.mode,self.gray.size)
        self.pixelsNew = self.rimg.load()

        gaussian = [[[1,2,1],
                    [2,4,2],
                    [1,2,1]],
                    [[1,4,6,4,1],
                    [4,16,24,16,4],
                    [6,24,36,24,6],
                    [4,16,24,16,4],
                    [1,4,6,4,1]]]

        for i in range(len(gaussian)):
            for j in range(len(gaussian[i])):
                for l in range(len(gaussian[i][j])):
                    if i == 0:
                        gaussian[i][j][l] /= 16
                    elif i == 1:
                        gaussian[i][j][l] /= 256
        
        laplacian = [[[1,1,1],
                      [1,-8,1],
                      [1,1,1]],
                     [[0,0,1,0,0],
                      [0,1,2,1,0],
                      [1,2,-16,2,1],
                      [0,1,2,1,0],
                      [0,0,1,0,0]],
                     [[0,1,1,2,2,2,1,1,0],
                      [1,2,4,5,5,5,4,2,1],
                      [1,4,5,3,0,3,5,4,1],
                      [2,5,3,-12,-24,-12,3,5,2],
                      [2,5,0,-24,-40,-24,0,5,2],
                      [2,5,3,-12,-24,-12,3,5,2],
                      [1,4,5,3,0,3,5,4,1],
                      [1,2,4,5,5,5,4,2,1],
                      [0,1,1,2,2,2,1,1,0]]]

        a = (self.size - 1) // 2

        if a == 3:
            a = 2

        y = 0
        if self.order > 0:
            y = 1

        for i in range(self.origin.size[0]):
            for j in range(self.origin.size[1]):
                x = 0
                for k in range(-a,a+1):
                    for l in range(-a,a+1):
                        if i+k > -1 and j+l > -1 and i+k < self.origin.size[0] and j+l < self.origin.size[1]:
                            temp = self.pixelMap[i+k,j+l]
                            x += temp[0]*gaussian[y][k+a][l+a]
                            
                grayV = int(abs(x))

                self.pixelsGau[i,j] = (grayV,255)

        a = (self.size - 1) // 2

        if a == 3:
            a = 4

        for i in range(self.gau.size[0]):
            for j in range(self.gau.size[1]):
                x = 0
                for k in range(-a,a+1):
                    for l in range(-a,a+1):
                        if i+k > -1 and j+l > -1 and i+k < self.gau.size[0] and j+l < self.gau.size[1]:
                            temp = self.pixelsGau[i+k,j+l]
                            x += temp[0]*laplacian[self.order][k+a][l+a]

                grayV = int(abs(x))

                if grayV > 180:
                    grayV = 255
                else:
                    grayV = 0
                
                self.pixelsNew[i,j] = (x,255)
                
        self.result = ImageTk.PhotoImage(self.rimg)
        self.resultL = ttk.Label(self)
        self.resultL["image"] = self.result
        self.resultL.grid(row = 1, column = 5, columnspan = 4)
        self.exist = 1
        self.count += 1

        self.labelR['text'] = "log"

root = Root()
root.mainloop()

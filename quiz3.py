import sys
import cv2
import numpy as np
import math

from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QFileDialog, QPushButton, QLineEdit, QGridLayout , QLayout
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem , QIntValidator
from PIL import Image


class MyApp(QWidget):

    is_resize = False
    is_rotate = False
    is_hfilp = False
    is_vfilp = False

    img_fomat = '(*.jpg , *.png , *.jpeg)'
    img_fomat_extension = ('.jpg' , '.png' , '.jpeg')
    file_paths = ()
    rotate_data = 90

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Resize
        cb = QCheckBox('Resize', self)
        cb.stateChanged.connect(self.ischeckResize)

        self.le_width = QLineEdit(self) # resize img width
        self.le_width.setValidator(QIntValidator(0,9999))

        self.le_height = QLineEdit(self) # resize img height
        self.le_height.setValidator(QIntValidator(0, 9999))

        #Rotate
        cb1 = QCheckBox('Rotate', self)
        cb1.stateChanged.connect(self.ischeckRotate)

        self.le_degree = QLineEdit(self)
        self.le_degree.setValidator(QIntValidator(1, 359))
        self.le_degree.setText('90')


        #hflip
        cb2 = QCheckBox('hflip', self)
        cb2.stateChanged.connect(self.ischeckHfilp)

        #vflip
        cb3 = QCheckBox('vflip', self)
        cb3.stateChanged.connect(self.ischeckVfilp)

        #set path
        btn_path = QPushButton(self)
        btn_path.setText('set file path')
        btn_path.clicked.connect(self.setFilePath)

        btn_path_delete = QPushButton(self)
        btn_path_delete.setText('Delete file path')
        btn_path_delete.clicked.connect(self.deleteFilePath)

        self.listview = QListView(self)
        self.model = QStandardItemModel()

        #run
        btn_run = QPushButton(self)
        btn_run.setText('Run')
        btn_run.clicked.connect(self.file_change)
        btn_run.resize(100,100)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        #line 1
        mainLayout.addWidget(cb, 0, 0, 1, 1)
        mainLayout.addWidget(self.le_width, 0, 1, 1, 1)
        mainLayout.addWidget(self.le_height, 0, 2, 1, 1)
        mainLayout.addWidget(btn_run, 0, 3, 1, 1)

        #line 2
        mainLayout.addWidget(cb1, 1, 0, 1, 1)
        mainLayout.addWidget(self.le_degree, 1, 1, 1, 1)

        #line 3, 4
        mainLayout.addWidget(cb2, 2, 0, 1, 1)
        mainLayout.addWidget(cb3, 3, 0, 1, 1)

        #line 5
        mainLayout.addWidget(btn_path, 4, 1, 1, 1)
        mainLayout.addWidget(btn_path_delete, 4, 2, 1, 1)

        mainLayout.addWidget(self.listview, 5, 0, 4, 4)

        self.setLayout(mainLayout)
        self.setWindowTitle('ImageAug')

        self.show()

    def ischeckResize(self, state):
        if state == Qt.Checked:
            self.is_resize = True
        else:
            self.is_resize = False

    def ischeckRotate(self, state):
        if state == Qt.Checked:
            self.is_rotate = True
        else:
            self.is_rotate = False

    def ischeckHfilp(self, state):
        if state == Qt.Checked:
            self.is_hfilp = True
        else:
            self.is_hfilp = False

    def ischeckVfilp(self, state):
        if state == Qt.Checked:
            self.is_vfilp = True
        else:
            self.is_vfilp = False


    def setFilePath(self):
        #self.textEdit.setText('')
        fname = QFileDialog.getOpenFileNames(self, 'Open file', './',self.img_fomat)
        for a in fname[0] :
            #self.textEdit.setText(self.textEdit.toPlainText()+'\n'+a)
            self.model.appendRow(QStandardItem(a))
        self.listview.setModel(self.model)


    def deleteFilePath(self):
        delete_item = self.listview.currentIndex().row()
        self.model.removeRow(delete_item)


    def file_change(self):
        if self.is_rotate :
            for i in range(self.model.rowCount()):
                path = self.model.index(i, 0, QModelIndex()).data(Qt.DisplayRole)
                self.setImgRotate(path)

        if self.is_resize :
            for i in range(self.model.rowCount()):
                path = self.model.index(i, 0, QModelIndex()).data(Qt.DisplayRole)
                self.setImgResize(path)

        if self.is_vfilp :
            for i in range(self.model.rowCount()):
                path = self.model.index(i, 0, QModelIndex()).data(Qt.DisplayRole)
                self.setImgFlip(path,'v')

        if self.is_hfilp :
            for i in range(self.model.rowCount()):
                path = self.model.index(i, 0, QModelIndex()).data(Qt.DisplayRole)
                self.setImgFlip(path,'h')



    def setImgResize(self , path):
        ## file name
        #print(path)
        name_idx = self.seach_filename(path)
        #print(path[name_idx : len(path)])
        file_name = path[name_idx : len(path)]
        extension_idx = self.seach_extension(file_name)

        resize_file_name = file_name[0:extension_idx] \
                           + '_resize_' \
                           +file_name[extension_idx : len(file_name)]

        ## file resize
        img = Image.open(path)
        w = img.width
        h = img.height

        resize_width = int(self.le_width.text())
        resize_height = int(self.le_height.text())

        cvImage = np.ones((w,h , 3), np.uint8) * 255
        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)
        img_cv = cv2.imread(path) ## open cv read img file
        resizeImage = cv2.resize(img_cv, dsize=(resize_width,resize_height))
        cv2.imwrite(path[0:name_idx] + resize_file_name,resizeImage)


    def setImgRotate(self , path):
        ## file name
        #print(path)
        degree = int(self.le_degree.text())

        name_idx = self.seach_filename(path)
        #print(path[name_idx : len(path)])
        file_name = path[name_idx : len(path)]
        extension_idx = self.seach_extension(file_name)

        rotate_file_name = file_name[0:extension_idx] \
                           + '_rotate_{}'.format(degree) \
                           +file_name[extension_idx : len(file_name)]
        ## file rotate
        img = Image.open(path)
        w = img.width
        h = img.height

        cvImage = np.ones((2*w,2*h , 3), np.uint8) * 255
        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)
        img_cv = cv2.imread(path) ## open cv read img file
        # 2배의 이미지에 1/2이미지를 회전한다.
        resizeImage = cv2.resize(img_cv, dsize=(2*w, 2*h)) # img size X 2
        M = cv2.getRotationMatrix2D((w, h), degree, 0.5) # 0.5 scale rotate
        rotated = cv2.warpAffine(resizeImage, M, (2*w, 2*h))
        # 배경 이미지를 줄이기 위해 좌표 계산후 이미지를 자른다.
        x_min , x_max , y_min , y_max =self.rotate_xy_min_max(w,h,degree)
        rotated2 = rotated[y_min: y_max , x_min: x_max] # img cut
        cv2.imwrite(path[0:name_idx] + rotate_file_name, rotated2)


    def setImgFlip(self , path,mode):
        ## file name
        #print(path)
        name_idx = self.seach_filename(path)
        #print(path[name_idx : len(path)])
        file_name = path[name_idx : len(path)]
        extension_idx = self.seach_extension(file_name)

        resize_file_name = file_name[0:extension_idx] \
                           + '_{}flip_'.format(mode) \
                           +file_name[extension_idx : len(file_name)]

        ## file flip
        img = Image.open(path)
        w = img.width
        h = img.height

        cvImage = np.ones((w,h , 3), np.uint8) * 255
        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)
        img_cv = cv2.imread(path) ## open cv read img file
        if 'v' in mode :
            flipImage = cv2.flip(img_cv,1)
        elif 'h' in mode :
            flipImage = cv2.flip(img_cv, 0)

        cv2.imwrite(path[0:name_idx] + resize_file_name,flipImage)


    def seach_filename(self , path):
        str = path
        result = 0
        while True:
            idx = str.find('/')
            if idx > -1:
                #print(idx)
                str = str[idx+1 : len(str)]
                result += idx + 1
            else :
                break
        return result

    def seach_extension(self, name):
        for extension in self.img_fomat_extension :
            extension_idx = name.find(extension)
            if extension_idx > -1 :
                return extension_idx

    def rotate_xy_min_max(self,w,h,degrees):
        th = math.radians(degrees)
        sin = math.sin(th)
        cos = math.cos(th)

        x1 = (w / 2 * 3 - w) * cos - (h / 2 - h) * sin + w
        x2 = (w / 2 - w) * cos - (h / 2 - h) * sin + w
        x3 = (w / 2 - w) * cos - (h / 2 * 3 - h) * sin + w
        x4 = (w / 2 * 3 - w) * cos - (h / 2 * 3 - h) * sin + w

        y1 = (w / 2 * 3 - w) * sin + (h / 2 - h) * cos + h
        y2 = (w / 2 - w) * sin + (h / 2 - h) * cos + h
        y3 = (w / 2 - w) * sin + (h / 2 * 3- h) * cos + h
        y4 = (w / 2 * 3 - w) * sin + (h / 2 * 3 - h) * cos + h

        x_min = 99999
        x_max = 0
        y_min = 99999
        y_max = 0
        x_range = (x1, x2, x3, x4)
        y_range = (y1, y2, y3, y4)

        for i in range(4):
            if x_max < x_range[i] :
                x_max = x_range[i]
            if x_range[i] < x_min :
                x_min = x_range[i]

            if y_max < y_range[i] :
                y_max = y_range[i]
            if y_range[i] < y_min :
                y_min = y_range[i]
        '''
        print('{} , {} '.format(w,h))
        print(' {} , {} , {} , {} '.format(x_range[0] , x_range[1], x_range[2],  x_range[3]))
        print(' {} , {} , {} , {} '.format(y_range[0] , y_range[1], y_range[2], y_range[3]))
        print(' {} , {} , {} , {} '.format(int(x_min) , int(x_max) , int(y_min) , int(y_max)))
        print(' {} , {} , {} , {} '.format(x1,x2,x3,x4))
        print(' {} , {} , {} , {} '.format(y1, y2, y3, y4))
        '''

        return int(x_min) , int(x_max) , int(y_min) , int(y_max)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
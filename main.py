import sys
import numpy as np
import math
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QSpinBox, QDesktopWidget, QPushButton, QDoubleSpinBox, QFrame, QLineEdit, QComboBox, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from qt_material import apply_stylesheet, QtStyleTools


import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

sys.path.append(".")
class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure(figsize=(100, 100))

        self.axes = fig.add_subplot(323)
        self.axes2 = fig.add_subplot(324)
        self.normal = fig.add_subplot(325)
        self.normal2 = fig.add_subplot(326)
        self.order_num = fig.add_subplot(311)

        fig.tight_layout(pad=70.0)

        self.axes.set_title("Lunch group delivery")
        self.axes2.set_title("Dinner group delivery")
        self.normal.set_title("Normal lunch delivery")
        self.normal2.set_title("Normal dinner delivery")
        self.order_num.set_title("Hourly delivery orders a day")

        self.axes.set_xlabel("Number of delivery robot")
        self.axes.set_ylabel("Average delayed time")
        self.axes2.set_xlabel("Number of delivery robot")
        self.axes2.set_ylabel("Average delayed time")
        self.normal.set_xlabel("Number of delivery robot")
        self.normal.set_ylabel("Average delayed time")
        self.normal2.set_xlabel("Number of delivery robot")
        self.normal2.set_ylabel("Average delayed time")
        self.order_num.set_xlabel("Hour")
        self.order_num.set_ylabel("Count")

        super(MplCanvas, self).__init__(fig)


class MyApp(QWidget, QtStyleTools):

    def __init__(self):
        super().__init__()
        self.initUI()
        apply_stylesheet(app, theme='custom.xml', invert_secondary=True)

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.sc = MplCanvas()
        toolbar = NavigationToolbar(self.sc, self)
        self.spinboxs = [QDoubleSpinBox(), QDoubleSpinBox(), QSpinBox(), QDoubleSpinBox()]
        btn = QPushButton("결과 확인", self)
        btn.clicked.connect(self.get_result)
        for spinbox in self.spinboxs:
            spinbox.setMinimum(1)
        self.spinboxs[0].setMaximum(1400000)
        self.spinboxs[0].setValue(500000)
        self.spinboxs[1].setMaximum(10)
        self.spinboxs[2].setMaximum(10000)
        self.spinboxs[2].setValue(1000)
        self.spinboxs[3].setMaximum(10)
        self.spinboxs[3].setValue(2.5)

        self.spinboxs[0].setSingleStep(1000)

        # 구역 특성 설정 spinbox
        self.checkboxs = [
            QCheckBox('세대 당 구성원 수', self),
            QCheckBox('실거주 세대 비율', self),
            QCheckBox('주요 나이대 설정', self),
            QCheckBox('1일 평균 주문 비율', self)
        ]
        self.type = QComboBox(self)
        txt = ["아파트", "산업 단지", "병원"]
        self.type.addItems(txt)
        self.property_boxs = [QSpinBox(), QSpinBox(), QSpinBox(), QSpinBox()]
        self.property_boxs[0].setMaximum(20)
        self.property_boxs[0].setValue(3)
        self.property_boxs[0].setMinimum(1)
        self.property_boxs[0].setSuffix("명")

        self.property_boxs[1].setMaximum(100)
        self.property_boxs[1].setValue(75)
        self.property_boxs[1].setMinimum(1)
        self.property_boxs[1].setSuffix("%")

        self.property_boxs[2].setMaximum(100)
        self.property_boxs[2].setValue(30)
        self.property_boxs[2].setMinimum(1)
        self.property_boxs[2].setSuffix("세")

        self.property_boxs[3].setMaximum(100)
        self.property_boxs[3].setValue(25)
        self.property_boxs[3].setMinimum(0)
        self.property_boxs[3].setSuffix("%")


        # google map api

        self.lineEdit = QLineEdit(self)
        self.cmb = QComboBox(self)
        txt = [str(i) for i in range(1, 21)]
        self.cmb.addItems(txt)
        self.cmb.setCurrentIndex(15)
        self.mbtn = QPushButton('구역 검색', self)
        self.img = QLabel('', self)
        self.img.setFrameStyle(QFrame.Box)
        self.mbtn.clicked.connect(self.map_search)

        # map alignment
        grid.addWidget(QLabel('구역 검색 '), 0, 0, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.lineEdit, 0, 1, 1, 6)
        grid.addWidget(self.mbtn, 0, 7, 1, 2)
        grid.addWidget(self.img, 1, 0, 7, 9)

        #  구역 특성 설정 섹션
        grid.addWidget(QLabel('구역 특성 설정'), 8, 0, alignment=QtCore.Qt.AlignLeft)

        grid.addWidget(QLabel('구역 종류 : '), 9, 0, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.type, 9, 1, 1, 1)

        grid.addWidget(self.checkboxs[0], 10, 0, 1, 2)
        grid.addWidget(self.property_boxs[0], 10, 2)

        grid.addWidget(self.checkboxs[1], 10, 3, 1, 2)
        grid.addWidget(self.property_boxs[1], 10, 5)

        grid.addWidget(self.checkboxs[2], 11, 0, 1, 2)
        grid.addWidget(self.property_boxs[2], 11, 2)

        grid.addWidget(self.checkboxs[3], 11, 3, 1, 2)
        grid.addWidget(self.property_boxs[3], 11, 5)



        """
        grid.addWidget(QLabel('면적: '), 0, 12, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.spinboxs[0], 0, 13)
        grid.addWidget(QLabel('미터제곱'), 0, 14)
        

        grid.addWidget(QLabel('가로:세로 비율: '), 0, 15, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.spinboxs[1], 0, 16)
        grid.addWidget(QLabel(':1'), 0, 17)

        grid.addWidget(QLabel('세대수: '), 0, 18, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.spinboxs[2], 0, 19)
        grid.addWidget(QLabel('세대'), 0, 20)

        grid.addWidget(QLabel('세대 당 구성원'), 0, 21, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(self.spinboxs[3], 0, 22)
        grid.addWidget(QLabel('명'), 0, 23)
        """

        grid.addWidget(btn, 0, 10)
        grid.addWidget(toolbar, 0, 9)
        grid.addWidget(self.sc, 1, 9, 10, 2)






        self.setWindowTitle('아파트 단지 면적 및 세대수에 따른 필요 배송 로봇 수 계산기')
        self.setWindowIcon(QIcon('logo.png'))
        self.resize(1800, 900)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_result(self):
        velocity = 9
        path = math.sqrt(self.spinboxs[0].value()/self.spinboxs[1].value()) * (1 + self.spinboxs[1].value()) * 1.5
        delivery = path / (velocity * 60)
        family = self.spinboxs[3].value() / 2.5
        order_lunch = family * self.spinboxs[2].value() / 9
        order_dinner = family * self.spinboxs[2].value() / 7
        order_normal = family * self.spinboxs[2].value() / 5.5
        order_normal2 = family * self.spinboxs[2].value() / 4.7

        # take x, y
        xs = np.linspace(1, 300, 3000)
        ys = np.linspace(15, 15, 3000)
        y_lunchs = ((delivery * order_lunch) / xs) - 120
        y_lunchs = np.where(y_lunchs < 0.0, 0.0, y_lunchs)
        y_dinners = ((delivery * order_dinner) / xs) - 120
        y_dinners = np.where(y_dinners < 0.0, 0.0, y_dinners)
        y_normals = ((delivery * order_normal) / xs) - 120
        y_normals = np.where(y_normals < 0.0, 0.0, y_normals)
        y_normals2 = ((delivery * order_normal2) / xs) - 120
        y_normals2 = np.where(y_normals2 < 0.0, 0.0, y_normals2)

        inter_lunch = []
        inter_dinner = []
        inter_normal = []
        inter_normal2 = []
        for x, y_lunch in zip(xs, y_lunchs):
            if 15 - y_lunch >= 0:
                inter_lunch.append((x, y_lunch))
                print(inter_lunch)
                break
        for x, y_dinner in zip(xs, y_dinners):
            if 15 - y_dinner >= 0:
                inter_dinner.append((x, y_dinner))
                print(inter_dinner)
                break
        for x, y_normal in zip(xs, y_normals):
            if 15 - y_normal >= 0:
                inter_normal.append((x, y_normal))
                print(inter_normal)
                break
        for x, y_normal in zip(xs, y_normals2):
            if 15 - y_normal >= 0:
                inter_normal2.append((x, y_normal))
                print(inter_normal2)
                break
        self.sc.axes.cla()
        self.sc.axes.plot(xs, y_lunchs, color='blue', lw=1, label='estimated delay according to the number of robots')
        self.sc.axes.plot(xs, ys, color='red', lw=1, label='required delay time')
        if inter_lunch:
            self.sc.axes.scatter(inter_lunch[0][0], inter_lunch[0][1],  label='optimized number of robots')
            self.sc.axes.text(inter_lunch[0][0]+0.2, inter_lunch[0][1]+1, np.round(inter_lunch[0][0], 2))
            self.sc.axes.set(xlim=[1, int(np.floor(inter_lunch[0][0] + 5))], ylim=[0, 50],
                              xticks=np.linspace(1, int(np.floor(inter_lunch[0][0] + 5)), 15, dtype=int),
                              yticks=np.linspace(0, 50, 5))
        else:
            self.sc.axes.set(xlim=[1, 15], ylim=[0, 50], xticks=np.linspace(1, 15, 15), yticks=np.linspace(0, 50, 5))
        self.sc.axes.set_xlabel("Number of delivery robot")
        self.sc.axes.set_ylabel("Average delayed time")
        self.sc.axes.grid()
        self.sc.axes2.cla()
        self.sc.axes2.plot(xs, y_dinners, color='blue', lw=1, label='estimated delay according to the number of robots')
        self.sc.axes2.plot(xs, ys, color='red', lw=1, label='required delay time')
        if inter_dinner:
            self.sc.axes2.scatter(inter_dinner[0][0], inter_dinner[0][1], label='optimized number of robots')
            self.sc.axes2.text(inter_dinner[0][0]+0.2, inter_dinner[0][1]+1, np.round(inter_dinner[0][0], 2))
            self.sc.axes2.set(xlim=[1, np.floor(inter_dinner[0][0] + 5)], ylim=[0, 50],
                              xticks=np.linspace(1, np.floor(inter_dinner[0][0] + 5), 15, dtype=int),
                              yticks=np.linspace(0, 50, 5))
        else:
            self.sc.axes2.set(xlim=[1, 15], ylim=[0, 50], xticks=np.linspace(1, 15, 15), yticks=np.linspace(0, 50, 5))
        self.sc.normal.cla()
        self.sc.normal.plot(xs, y_normals, color='blue', lw=1, label='estimated delay according to the number of robots')
        self.sc.normal.plot(xs, ys, color='red', lw=1, label='required delay time')
        if inter_normal:
            self.sc.normal.scatter(inter_normal[0][0], inter_normal[0][1], label='optimized number of robots')
            self.sc.normal.text(inter_normal[0][0] + 0.2, inter_normal[0][1] + 1, np.round(inter_normal[0][0], 2))
            self.sc.normal.set(xlim=[1, np.floor(inter_normal[0][0] + 5)], ylim=[0, 50],
                              xticks=np.linspace(1, int(np.floor(inter_normal[0][0] + 5)), 15, dtype=int),
                              yticks=np.linspace(0, 50, 5))
        else:
            self.sc.normal.set(xlim=[1, 15], ylim=[0, 50], xticks=np.linspace(1, 15, 15), yticks=np.linspace(0, 50, 5))
        self.sc.normal2.cla()
        self.sc.normal2.plot(xs, y_normals2, color='blue', lw=1,
                            label='estimated delay according to the number of robots')
        self.sc.normal2.plot(xs, ys, color='red', lw=1, label='required delay time')
        if inter_normal2:
            self.sc.normal2.scatter(inter_normal2[0][0], inter_normal2[0][1], label='optimized number of robots')
            self.sc.normal2.text(inter_normal2[0][0] + 0.2, inter_normal2[0][1] + 1, np.round(inter_normal2[0][0], 2))
            self.sc.normal2.set(xlim=[1, np.floor(inter_normal2[0][0] + 5)], ylim=[0, 50],
                               xticks=np.linspace(1, int(np.floor(inter_normal2[0][0] + 5)), 15, dtype=int),
                               yticks=np.linspace(0, 50, 5))
        else:
            self.sc.normal2.set(xlim=[1, 15], ylim=[0, 50], xticks=np.linspace(1, 15, 15), yticks=np.linspace(0, 50, 5))
        self.sc.order_num.cla()
        hour = np.linspace(0, 23, 24)
        ratio = np.array([0.020, 0.010, 0.004, 0.002, 0.000, 0.000, 0.000, 0.000, 0.002, 0.006, 0.022, 0.054, 0.074,
                          0.056, 0.049, 0.048, 0.052, 0.057, 0.122, 0.130, 0.102, 0.079, 0.071, 0.039])
        order = ratio * self.spinboxs[2].value() / 4
        self.sc.order_num.plot(hour, order, 'bo-', lw=1)
        self.sc.order_num.set(xticks=np.linspace(0, 23, 24, dtype=int))
        self.sc.axes2.set_xlabel("Number of delivery robot")
        self.sc.axes2.set_ylabel("Average delayed time")
        self.sc.normal.set_xlabel("Number of delivery robot")
        self.sc.normal.set_ylabel("Average delayed time")
        self.sc.normal2.set_xlabel("Number of delivery robot")
        self.sc.normal2.set_ylabel("Average delayed time")
        self.sc.axes.legend(fontsize='7')
        self.sc.axes2.legend(fontsize='7')
        self.sc.normal.legend(fontsize='7')
        self.sc.normal2.legend(fontsize='7')
        self.sc.axes.set_title("Lunch group delivery")
        self.sc.axes2.set_title("Dinner group delivery")
        self.sc.normal.set_title("Normal lunch delivery")
        self.sc.normal2.set_title("Normal dinner delivery")
        self.sc.order_num.set_title("Predicted Hourly delivery orders for a day")
        self.sc.order_num.set_xlabel("Hour")
        self.sc.order_num.set_ylabel("Count")
        self.sc.axes2.grid()
        self.sc.normal.grid()
        self.sc.normal2.grid()
        self.sc.order_num.grid()
        self.sc.draw()

    def map_search(self):
        BASE_URL = 'https://maps.googleapis.com/maps/api/staticmap?'
        API_KEY = 'AIzaSyAa3teUmXVM47Z5wzAQ5pmPnFGhKPH-z5o'
        ZOOM = self.cmb.currentIndex() + 1
        CITY = self.lineEdit.text()

        W = self.img.width()
        H = self.img.height()

        URL = (BASE_URL
               + f'center={CITY}'
               + f'&zoom={ZOOM}'
               + f'&size={W}x{H}&scale=2'
               + '&markers=color:red%7Clabel:S%7C' + CITY
               + f'&key={API_KEY}')

        # HTTP request
        response = requests.get(URL)

        # image scaled and draw
        img = QPixmap()
        img.loadFromData(response.content)
        img = img.scaled(img.width() // 2, img.height() // 2, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.img.setPixmap(img)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyApp()
    sys.exit(app.exec_())
import sys
import numpy as np
import math
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QSpinBox, QDesktopWidget, QPushButton, QDoubleSpinBox)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore


import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure(figsize=(100, 100))
        self.axes = fig.add_subplot(211)
        self.axes2 = fig.add_subplot(212)
        fig.tight_layout(pad=80.0)
        self.axes.set_title("Lunch delivery")
        self.axes2.set_title("Dinner delivery")
        self.axes.set_xlabel("Number of delivery robot")
        self.axes.set_ylabel("Average delayed time")
        self.axes2.set_xlabel("Number of delivery robot")
        self.axes2.set_ylabel("Average delayed time")
        super(MplCanvas, self).__init__(fig)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.sc = MplCanvas()
        toolbar = NavigationToolbar(self.sc, self)
        self.spinboxs = [QDoubleSpinBox(), QDoubleSpinBox(), QSpinBox()]
        btn = QPushButton("결과 확인", self)
        btn.clicked.connect(self.get_result)
        for spinbox in self.spinboxs:
            spinbox.setMinimum(1)
        self.spinboxs[0].setMaximum(1400000)
        self.spinboxs[1].setMaximum(10)
        self.spinboxs[2].setMaximum(10000)

        self.spinboxs[0].setSingleStep(1000)

        grid.addWidget(QLabel('면적: '), 0, 0, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(QLabel('가로:세로 비율: '), 1, 0, alignment=QtCore.Qt.AlignRight)
        grid.addWidget(QLabel('세대수: '), 2, 0, alignment=QtCore.Qt.AlignRight)

        grid.addWidget(self.spinboxs[0], 0, 1)
        grid.addWidget(self.spinboxs[1], 1, 1)
        grid.addWidget(self.spinboxs[2], 2, 1)

        grid.addWidget(QLabel('미터제곱'), 0, 2)
        grid.addWidget(QLabel(':1'), 1, 2)
        grid.addWidget(QLabel('세대'), 2, 2)

        grid.addWidget(toolbar, 3, 0)
        grid.addWidget(self.sc, 4, 0)
        grid.addWidget(btn, 4, 2)

        self.setWindowTitle('아파트 단지 면적 및 세대수에 따른 필요 배송 로봇 수 계산기')
        self.setWindowIcon(QIcon('logo.png'))
        self.resize(900, 900)
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
        order_lunch = self.spinboxs[2].value() / 5
        order_dinner = self.spinboxs[2].value() / 3
        max_time = (60 / delivery) * 15 + 120
        # take x, y
        xs = np.linspace(1, 300, 2000)
        ys = np.linspace(15, 15, 2000)
        y_lunchs = ((delivery * order_lunch) / xs) - 120
        y_lunchs = np.where(y_lunchs < 0.0, 0.0, y_lunchs)
        y_dinners = ((delivery * order_dinner) / xs) - 120
        y_dinners = np.where(y_dinners < 0.0, 0.0, y_dinners)
        inter_lunch = []
        inter_dinner = []
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
        self.sc.axes.cla()
        self.sc.axes.plot(xs, y_lunchs, color='blue', lw=1, label='estimated delay according to the number of robots')
        self.sc.axes.plot(xs, ys, color='red', lw=1, label='required delay time')
        if inter_lunch:
            self.sc.axes.scatter(inter_lunch[0][0], inter_lunch[0][1],  label='optimized number of robots')
            self.sc.axes.text(inter_lunch[0][0]+0.2, inter_lunch[0][1]+1, np.round(inter_lunch[0][0], 2))
            self.sc.axes.set(xlim=[1, int(np.floor(inter_lunch[0][0] + 5))], ylim=[0, 50],
                              xticks=np.linspace(1, int(np.floor(inter_lunch[0][0] + 5)), int(np.floor(inter_lunch[0][0] + 5))),
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
                              xticks=np.linspace(1, int(np.floor(inter_dinner[0][0] + 5)), int(np.floor(inter_dinner[0][0] + 5))),
                              yticks=np.linspace(0, 50, 5))
        else:
            self.sc.axes2.set(xlim=[1, 15], ylim=[0, 50], xticks=np.linspace(1, 15, 15), yticks=np.linspace(0, 50, 5))
        self.sc.axes2.set_xlabel("Number of delivery robot")
        self.sc.axes2.set_ylabel("Average delayed time")
        self.sc.axes.legend(fontsize='7')
        self.sc.axes2.legend(fontsize='7')
        self.sc.axes.set_title("Lunch delivery")
        self.sc.axes2.set_title("Dinner delivery")
        self.sc.axes2.grid()
        self.sc.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyApp()
    sys.exit(app.exec_())
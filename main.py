import sys
import numpy as np
import math
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QSpinBox, QDesktopWidget, QPushButton, QDoubleSpinBox)
from PyQt5.QtGui import QIcon

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
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
        self.output = QLabel('현재 설정한 로봇 수로 예상되는 지연시간은 점심에 0분, 저녁에 0분 입니다. \n'
                            '최적의 배송환경(15분 지연)을 위해서 점심에는 0대의 로봇이, 저녁에는 0대의 로봇이 필요합니다.')
        self.spinboxs = [QDoubleSpinBox(), QDoubleSpinBox(), QSpinBox()]
        btn = QPushButton("결과 확인", self)
        btn.clicked.connect(self.get_result)
        for spinbox in self.spinboxs:
            spinbox.setMinimum(1)
        self.spinboxs[0].setMaximum(1400000)
        self.spinboxs[1].setMaximum(10)
        self.spinboxs[2].setMaximum(1000)

        self.spinboxs[0].setSingleStep(1000)

        self.spinboxs[0].valueChanged.connect(self.result)
        self.spinboxs[1].valueChanged.connect(self.result)
        self.spinboxs[2].valueChanged.connect(self.result)

        grid.addWidget(QLabel('면적: '), 0, 0)
        grid.addWidget(QLabel('가로:세로 비율: '), 1, 0)
        grid.addWidget(QLabel('세대수: '), 2, 0)

        grid.addWidget(self.spinboxs[0], 0, 1)
        grid.addWidget(self.spinboxs[1], 1, 1)
        grid.addWidget(self.spinboxs[2], 2, 1)

        grid.addWidget(QLabel('미터제곱'), 0, 2)
        grid.addWidget(QLabel(':1'), 1, 2)
        grid.addWidget(QLabel('세대'), 2, 2)

        grid.addWidget(self.output, 3, 0)
        grid.addWidget(btn, 3, 1)
        grid.addWidget(self.sc, 4, 1)

        self.setWindowTitle('아파트 단지 면적 및 세대수에 따른 필요 배송 로봇 수 계산기')
        self.setWindowIcon(QIcon('logo.png'))
        self.resize(800, 500)
        self.center()
        self.show()

    def result(self):
        if self.spinboxs[0] and self.spinboxs[1] and self.spinboxs[2]:
            velocity = 9
            path = math.sqrt(self.spinboxs[0].value()) * 1.5
            delivery = path/(velocity*60)
            order_lunch = self.spinboxs[1].value()//5
            order_dinner = (self.spinboxs[1].value()*1.5) // 5
            max_time = (60/delivery) * 15 + 120
            required_lunch = math.ceil(order_lunch * (delivery / max_time))
            required_dinner = math.ceil(order_dinner * (delivery / max_time))
            result_lunch = math.floor(delivery * order_lunch / self.spinboxs[2].value())
            if result_lunch > max_time:
                result_lunch = abs(math.floor((required_lunch - max_time)/self.spinboxs[2].value()))
            else:
                result_lunch = 0
            result_dinner = math.floor(delivery * order_dinner / self.spinboxs[2].value())
            if result_dinner > max_time:
                result_dinner = abs(math.floor((result_dinner - max_time)/self.spinboxs[2].value()))
            else:
                result_dinner = 0
            self.output.setText(f'현재 설정한 로봇 수로 예상되는 지연시간은 점심에 {result_lunch}분, 저녁에 {result_dinner}분 입니다. \n'
                                f'최적의 배송환경(15분 지연)을 위해서 점심에는 {required_lunch}대의 로봇이, 저녁에는 {required_dinner}대의 로봇이 필요합니다.')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_result(self):
        velocity = 9
        path = math.sqrt(self.spinboxs[0].value()/self.spinboxs[1].value()) * (1 + self.spinboxs[1].value()) * 1.5
        delivery = path / (velocity * 60)
        order_lunch = self.spinboxs[2].value() // 5
        order_dinner = (self.spinboxs[2].value() * 1.5) // 5
        max_time = (60 / delivery) * 15 + 120
        # take x, y
        x = np.linspace(1, 20, 20)
        y_lunch = ((delivery * order_lunch) / x) - max_time
        y_lunch = np.where(y_lunch < 0.0, 0.0, y_lunch)
        y_dinner = ((delivery * order_dinner) / x) - max_time
        self.sc.axes.cla()
        self.sc.axes.plot(x, y_lunch, color='blue', lw=1)
        self.sc.axes.set_xlabel("x")
        self.sc.axes.set_ylabel("y")
        self.sc.axes.grid()
        self.sc.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyApp()
    sys.exit(app.exec_())
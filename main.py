import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QSpinBox, QDesktopWidget, QPushButton,
                             QDoubleSpinBox, QFrame, QLineEdit, QComboBox, QCheckBox)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from qt_material import apply_stylesheet, QtStyleTools

sys.path.append(".")


class MyApp(QWidget, QtStyleTools):

    def __init__(self):
        super().__init__()
        self.initUI()
        apply_stylesheet(app, theme='custom.xml', invert_secondary=True)

    def initUI(self):
        self.apt = [
            "헬리오시티아파트",
            "LG메트로시티아파트",
            "잠실파크리오",
            "잠실엘스아파트",
            "잠실리센츠",
            "올림픽선수기자촌아파트",
            "수원한일타운아파트",
            "화명롯데캐슬카이저",
            "고덕그라시움아파트",
            "DMC파크뷰자이아파트"
        ]

        self.detail = {
            "헬리오시티아파트": [9510, 84, 97190],
            "LG메트로시티아파트": [7374, 74, 1364307],
            "잠실파크리오": [6864, 66, 1142141],
            "잠실엘스아파트": [5678, 72, 935380],
            "잠실리센츠": [5563, 65, 935053],
            "올림픽선수기자촌아파트": [5540, 122, 854994],
            "수원한일타운아파트": [5282, 58, 744036],
            "화명롯데캐슬카이저": [5239, 48, 1047100],
            "고덕그라시움아파트": [4932, 53, 811620],
            "DMC파크뷰자이아파트": [4300, 61, 712875]
        }

        grid = QGridLayout()
        self.setLayout(grid)
        self.spinboxs = [QDoubleSpinBox(), QDoubleSpinBox(), QSpinBox(), QDoubleSpinBox()]
        btn = QPushButton("결과 확인", self)
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
        self.property_boxs = [QDoubleSpinBox(), QSpinBox(), QSpinBox(), QSpinBox()]
        self.property_boxs[0].setMaximum(20)
        self.property_boxs[0].setValue(3)
        self.property_boxs[0].setMinimum(1)
        self.property_boxs[0].setSuffix("명")

        self.property_boxs[1].setMaximum(100)
        self.property_boxs[1].setValue(75)
        self.property_boxs[1].setMinimum(1)
        self.property_boxs[1].setSuffix("%")

        self.property_boxs[2].setMaximum(60)
        self.property_boxs[2].setValue(30)
        self.property_boxs[2].setMinimum(20)
        self.property_boxs[2].setSuffix("세")

        self.property_boxs[3].setMaximum(100)
        self.property_boxs[3].setValue(25)
        self.property_boxs[3].setMinimum(0)
        self.property_boxs[3].setSuffix("%")


        #  google map api

        # self.lineEdit = QLineEdit(self)
        self.templine = QComboBox(self)
        self.templine.addItems(self.apt)
        self.mbtn = QPushButton('구역 검색', self)
        self.img = QLabel('', self)
        self.img.setFrameStyle(QFrame.Box)

        # map alignment
        grid.addWidget(QLabel('구역 검색 '), 0, 0, alignment=QtCore.Qt.AlignRight)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyApp()
    sys.exit(app.exec_())
import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QLabel, QDesktopWidget, QPushButton,
                             QLineEdit, QComboBox, QFileDialog, QTableView, QProgressDialog, QSpinBox,
                             QMessageBox)
from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSignal, QThread
from qt_material import apply_stylesheet, QtStyleTools
import pandas as pd

from util import get_dataframe, get_colum_name, replace_filename_by_col

sys.path.append(".")


class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, df: pd.DataFrame, code_col: str, subject_col: str, path, index):
        super().__init__()
        self.df = df
        self.code_col = code_col
        self.subject_col = subject_col
        self.path = path
        self.index = index

    def run(self):
        # 긴 작업을 여기서 수행
        replace_filename_by_col(self.df, self.code_col, self.subject_col, self.path, self.index)
        self.finished.emit()  # 작업 완료 시그널 발생


class PandasModel(QAbstractTableModel):
    def __init__(self, data=pd.DataFrame()):
        QAbstractTableModel.__init__(self)
        self._data = data

    def updateData(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            else:
                return str(self._data.index[section])
        return None


class MyApp(QWidget, QtStyleTools):

    def __init__(self):
        super().__init__()
        self.code_col = QComboBox()
        self.sub_col = QComboBox()
        self.initUI()
        apply_stylesheet(app, theme='custom.xml', invert_secondary=True)  # abs path required

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        self.file_sel_text = QLabel(self)
        self.file_sel_text.setText('파일명 :')
        self.file_path = QComboBox(self)
        self.file_path.currentTextChanged.connect(self.show_table)
        self.file_sel_btn = QPushButton(self)
        self.file_sel_btn.setText('파일 선택(.csv, .xlsx)')
        self.file_sel_btn.clicked.connect(self.file_choose)
        # Table view
        self.view = QTableView()
        self.model = PandasModel()
        self.view.setModel(self.model)

        self.dir_sel_text = QLabel(self)
        self.dir_sel_text.setText('폴더명 :')
        self.dir_path = QLineEdit(self)
        self.dir_path.setText("Z:\\윤국연\\2024_DB")
        self.dir_path.setReadOnly(True)
        self.dir_sel_btn = QPushButton(self)
        self.dir_sel_btn.setText('저장 위치 선택')
        self.dir_sel_btn.clicked.connect(lambda: self.folder_choose(self.dir_path))
        self.name_change_btn = QPushButton(self)
        self.name_change_btn.setText('저장하기')
        self.name_change_btn.clicked.connect(self.rename)

        # col selection
        self.spin = QSpinBox(self)
        self.spin.setMinimum(0)
        self.c_col_sel = QLabel(self)
        self.c_col_sel.setText('지문코드 열:')
        self.s_col_sel = QLabel(self)
        self.s_col_sel.setText('지문주제 열 :')

        # file alignment
        grid.addWidget(self.file_sel_text, 0, 0)
        grid.addWidget(self.file_path, 0, 1, 1, 7)
        grid.addWidget(self.file_sel_btn, 0, 8)
        # view alignment
        grid.addWidget(self.view, 1, 0, 7, 9)
        # col selection alignment
        grid.addWidget(self.spin, 8, 1, 1, 2)
        grid.addWidget(self.c_col_sel, 8, 3, 1, 1)
        grid.addWidget(self.code_col, 8, 4, 1, 2)
        grid.addWidget(self.s_col_sel, 8, 6, 1, 1)
        grid.addWidget(self.sub_col, 8, 7, 1, 2)
        # dir alignment
        grid.addWidget(self.dir_sel_text, 9, 0)
        grid.addWidget(self.dir_path, 9, 1, 1, 6)
        grid.addWidget(self.dir_sel_btn, 9, 7)
        grid.addWidget(self.name_change_btn, 9, 8)


        self.setWindowTitle('학생 시험 응답 통계 생성기')
        self.resize(800, 800)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def file_choose(self):
        files, check = QFileDialog.getOpenFileNames(self,
                                                  self.tr("엑셀 파일 선택"),
                                                  "/",
                                                  self.tr("Excel files (*.xls*);;CSV files (*.csv)"))
        if check:
            self.file_path.clear()
            self.file_path.addItems(files)

    def folder_choose(self, x):
        folder = QFileDialog.getExistingDirectory(self,
                                                  self.tr("이름을 바꿀 폴더 선택"),
                                                  "/")
        x.setText(folder)

    def show_table(self):
        path = os.path.join(self.file_path.currentText())
        df = get_dataframe(path)
        cols = get_colum_name(df)
        self.code_col.addItems(cols)
        self.sub_col.addItems(cols)
        self.model.updateData(df)

    def rename(self):
        root = os.path.join(self.dir_path.text())
        # popup
        self.progressDialog = QProgressDialog("이름 변환 진행중...", "Abort", 0, 0, self)
        self.progressDialog.setCancelButton(None)  # 취소 버튼 비활성화
        self.progressDialog.setModal(True)  # 모달 다이얼로그로 설정
        self.progressDialog.setAutoClose(False)  # 작업 완료시 자동으로 닫히지 않도록 설정
        self.progressDialog.show()

        # 작업 스레드 생성 및 시작
        self.thread = WorkerThread(self.model._data, self.code_col.currentText(), self.sub_col.currentText(), root, self.spin.value())
        self.thread.finished.connect(self.taskFinished)
        self.thread.start()

    def taskFinished(self):
        # 작업 완료 시, 프로그레스 다이얼로그 닫기
        self.progressDialog.close()
        QMessageBox.information(self, "완료", "작업이 완료되었습니다.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyApp()
    sys.exit(app.exec_())

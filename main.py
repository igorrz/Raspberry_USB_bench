from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *
from PyQt5.QtWidgets import *

import sys
import time
import subprocess

import re

import matplotlib
matplotlib.use('Qt5Agg')  # source: https://www.learnpyqt.com/courses/graphics-plotting/plotting-matplotlib/
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.w = loadUi('GUI/main_window.ui')
        self.measure_time = 10  # time in seconds
        self.packages_number = 1000
        self.packages_size = 1000  #in bytes

        self.w.StartTest.clicked.connect(self.start_measurment)


    def start_measurment(self):

        # source: https://stackoverflow.com/questions/54856890/running-dd-from-python-and-getting-progress
        self.run_time = int(self.w.TestTime.text())
        self.sleep_time = int(self.w.SleepTime.text())
        self.packages_size = int(self.w.PackageSize.text())
        self.packages_number = int(self.w.PackageNumber.text())

        cmd = ["dd", "if=/Users/igor/PycharmProjects/RaspberryUSB/in/tester.rtf", "of=/Users/igor/PycharmProjects/RaspberryUSB/out/tester.rtf",
               f"bs={self.packages_size}", f"count={self.packages_number}"]

        self.measurment = []

        start_time = time.time()
        for _ in range(self.run_time):
            line = ''
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
            while True:
                out = process.stderr.read(1)
                if out == b'' and process.poll() != None:
                    break
                if out != b'':
                    s = out.decode("utf-8")
                    if s == '\r':
                        print(line)
                        line = ''
                    else:
                        line = line + s
            a = re.findall(r'\b\d+\b', line)  # source: https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python/4289415#4289415
            self.measurment.append(float(a[-1]))
            time.sleep(self.sleep_time)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(self.measurment)
        self.setCentralWidget(sc)

        '''
        temp_fig_path = 'temp/temp_plot.png'
        sc.fig.savefig(temp_fig_path)
        image = QImage(temp_fig_path)
        if image.isNull():
            QMessageBox.information(self, "Image Viewer", "Cannot load %s." % temp_fig_path)
            return
        leftPixelMap = QPixmap(temp_fig_path)
        lable = QLabel(self.w.PlotWindow)
        lable.setPixmap(leftPixelMap)
        #self.w.PlotWindow.fitInView(leftPixelMap)
        lable.show()
        '''

        if self.w.SavePlotBox.isChecked():
            name = f'{self.run_time}_{self.sleep_time}_{self.packages_size}_{self.packages_number}.png'
            sc.fig.savefig('figures/'+name)
        self.show()

class MplCanvas(FigureCanvasQTAgg):
    # source: https://www.learnpyqt.com/courses/graphics-plotting/plotting-matplotlib/

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.w.show()
    sys.exit(app.exec_())

import sys
import AbsoluteLayout.py#用哪个，导入哪个包。
from PyQt5.QtWidgets import QApplication,QMainWindow

if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = AbsoluteLayout.Ui_MainWindow()
    #向窗口上添加控件
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
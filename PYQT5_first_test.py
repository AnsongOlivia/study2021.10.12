from sys import argv,exit
from PyQt5.QtWidgets import QWidget, QApplication  
  
if __name__ == '__main__':  
    #创建QApplication类的实例
    app = QApplication(argv)
    #创建一个窗口  
    w = QWidget()


    #设置窗口的尺寸
    #w.resize(400, 200)
    #设置窗口可移动化
    #w.move(300, 300)
    
    #上述两步不设置也可以执行！！！  
      

    #设置窗口的标题
    w.setWindowTitle("测试用软件")  
    #显示窗口
    w.show()  
    #进入程序主循环、并通过exit函数确保主循环安全结束
    exit(app.exec_())  
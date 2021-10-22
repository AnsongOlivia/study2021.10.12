import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
                # QObject, Signal, Slot

app = QApplication(sys.argv)
#定义一个接受字符串类型的槽
# @Slot(str)
@QtCore.pyqtSlot(str)
def say_some_words(words):
	print(words)

class Communicate(QObject):
	#定义一个信号
  speak = pyqtSignal(str)

someone = Communicate()
someone.speak.connect(say_some_words)  #连接信号和槽
someone.speak.emit('hello world.')       #发送信号

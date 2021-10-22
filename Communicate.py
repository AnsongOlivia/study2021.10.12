import sys                                                                  
from PySide2.QtCore import QObject, Signal  
class Communicate(QObject): 
    speak = Signal()     
            
    def __init__(self): 
        super(Communicate, self).__init__()    
        self.speak.connect(self.say_hello) 

    def speaking_method(self):  
        self.speak.emit()   
    def say_hello(self):
        print("Hello world")  
                            
someone = Communicate()     
someone.speaking_method()

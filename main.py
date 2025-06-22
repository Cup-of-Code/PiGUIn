import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QLabel, QVBoxLayout,QWidget


class menuButton(QPushButton):
    """
    En klass för att skapa återanvändbara knappar till menufunktionaliteten
    """
    def __init__(self, title, width= 300, height=300):
        super().__init__(title)
        self.title = title
        self.setFixedSize(width, height)
        self.setStyleSheet("background-color: #093; color: black; border-radius: 15px; font-size: 30px;")
        self.clicked.connect(self.buttonClick)
        
    def buttonClick(self): #funktionalitet för att se om knappen har klickats
        print("knappen: "+ self.title + " klickades.")
        
        
class timeKeeper(QLabel):
    """
    En klass som skapar en "label" som sedan visar den aktuella tiden på startsidan.
    """
   
    def __init__(self, title, width= 667, height=50):
        super().__init__(title)
        self.setFixedSize(width, height)
        self.setStyleSheet("color: black; font-size: 48px;")
        
    #Kod för att hämta och visa tiden kommer läggas till nedan.



class MainWindow(QMainWindow):
    """ 
    En klass för att skapa huvudfönstret i applikationen. 
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(667, 1000)) #667x1000 är samma ratio som LCD-skärmen (320x480)
        self.setWindowTitle("PiGUIn")
        layout = QVBoxLayout() #med denna layout så läggs de definierade "widget"-sen som på en vertikal stapel.
        
        appButton = menuButton("app1")
        currentTime = timeKeeper("Time now:      XX : XX")
        
        layout.addWidget(currentTime)
        layout.addWidget(appButton)

        containerBox = QWidget()
        containerBox.setLayout(layout)
        self.setCentralWidget(containerBox)
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

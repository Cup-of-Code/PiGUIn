import sys

from PyQt5.QtCore import (
    QSize,
    Qt,
    QTimer, QTime,
    )

from PyQt5.QtWidgets import ( 
    QApplication,
    QMainWindow,
    QPushButton,
    QMenu,
    QLabel,
    QGridLayout,
    QWidget,
    QToolBar,

    )


class menuButton(QPushButton):
    """
    En klass för att skapa återanvändbara knappar till menufunktionaliteten
    """
    def __init__(self, title, width= 300, height=300):
        super().__init__(title)
        self.title = title
        self.setFixedSize(width, height)
        self.setStyleSheet("background-color: #093; color: black; border-radius: 15px;font-family: 'Daily Bubble'; font-size: 45px;")
        self.clicked.connect(self.buttonClick)
        
    def buttonClick(self): #funktionalitet för att se om knappen har klickats
        print("knappen: "+ self.title + " klickades.")
        
        


class timeKeeper(QLabel):
    """
    En klass som skapar en "label" som sedan visar den aktuella tiden på startsidan.
    """
    def __init__(self, width=667, height=90):
        super().__init__()
        self.setFixedSize(int(width), int(height))  # ensure width and height are integers
        self.setStyleSheet("color: black; font-family: 'Super Vibes'; font-size: 60px;") #Super Vibes är en custom font:  dafont.com/super-vibes.font



        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)

        self.updateClock()

    def updateClock(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.setText(current_time)


            



class MainWindow(QMainWindow):
    """ 
    En klass för att skapa huvudfönstret i applikationen. 
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(667, 1000)) #667x1000 är samma ratio som LCD-skärmen (320x480)
        self.setWindowTitle("PiGUIn")
        layout = QGridLayout() #med denna layout så sorteras de tillagda komponenterna i en grid-layout
        
        statsButton = menuButton("System stats")
        statsButton.clicked.connect(self.showstats) #byter till systemstatsfönstret när knappen klickas
        
        fileButton = menuButton("Files")
        currentTime = timeKeeper()
        
        layout.addWidget(currentTime,0,0) #0,1 indikerar rad 0, kolumn 1 i grid-layouten
        layout.addWidget(statsButton, 1,0)
        layout.addWidget(fileButton,1,1)

        containerBox = QWidget()
        containerBox.setLayout(layout)
        self.setCentralWidget(containerBox)
        self.statsPage = statsWindow()
        
        
        
    def showstats(self, checked):
       self.statsWindow = statsWindow()
       self.statsWindow.show()
        
        
        
        
class statsWindow(QWidget):
    """
        En klass för systemstatistik fönstret
    """

    def __init__(self):
        super().__init__()
        self.system_temp = self.systemTemp()
        sysTemp = self.systemTemp()
        tempLabel = QLabel("System temp: "+ str(sysTemp))
        self.setStyleSheet("color: black; font-family: 'Daily Bubble'; font-size: 40px;")
        layout = QGridLayout()
        layout.addWidget(tempLabel)
        self.setLayout(layout)
        
        
        
    def systemTemp(self):
         try:
             with open ('/sys/class/thermal/thermal_zone0/temp') as tempStatFile: #systemStat path här är definierad för mitt specifika OS.
                 tempValue = tempStatFile.read().strip()
                 return float(tempValue) / 1000.0
         except:
             print("could not locate temp info")
             return None
         
    
    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

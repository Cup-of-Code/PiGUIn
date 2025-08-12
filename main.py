#DISCLAIMER: 
    #Några externa fonts kan behöva laddas ner för att köra programmet:
        #    https://www.dafont.com/super-vibes.font
        #    https://www.dafont.com/daily-bubble.font
    # Filsökvägen på rad 125 kan behöva justeras
import sys
from PyQt5.QtGui import QFont, QColor, QIcon
import os, time
from LoRaWAN import LoRa

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
    QStackedWidget,
    QGraphicsDropShadowEffect

   )
from lora_window import LoRaWindow


windowSize  = QSize(320, 480) 

class MainWindow(QMainWindow):
    """ 
    En klass för att skapa huvudfönstret i applikationen. 
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(windowSize)
        self.setWindowTitle("PiGUIn")

        self.statsPage = statsWindow()
        self.filesPage = filesWindow()
        self.loraPage  = LoRaWindow()
        self.homePage  = self.homeWindow()         


        self.stack = QStackedWidget()

        self.stack.addWidget(self.homePage)
        self.stack.addWidget(self.statsPage)    
        self.stack.addWidget(self.filesPage)
        self.stack.addWidget(self.loraPage)

        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.homePage)

        


    def homeWindow(self) -> QWidget:
        self.setStyleSheet("""
        QMainWindow {
            background-image: url('clouds.png');
            background-repeat: no-repeat;
            background-position: center;
            background-color: blue; 
        }
    """)
        page = QWidget()
        layout = QGridLayout(page)


        currentTime = timeKeeper()
        fileButton = menuButton("Files")
        statsButton = menuButton("System stats")
        LoRaButton = menuButton("LoRa") 
        SettingsButton = menuButton("Settings") #settings knappen är inte implementerad än


        #Nedan byter till motsvarande fönstret när knappen klickas
        statsButton.clicked.connect( lambda: self.jumpToPage(self.statsPage)) #uses lambda to not run the function immediately
        fileButton.clicked.connect( lambda: self.jumpToPage(self.filesPage)) 
        LoRaButton.clicked.connect( lambda: self.jumpToPage(self.loraPage))
        self.statsPage.backButton.clicked.connect(lambda: self.jumpToPage(self.homePage)) #byter till hem när "home" knappen i statsPage klickas
        self.filesPage.backButton.clicked.connect(lambda: self.jumpToPage(self.homePage))
        self.loraPage.backButton.clicked.connect(lambda: self.jumpToPage(self.homePage))

        layout.addWidget(self.greetingPhrase(),0,0,1,2) #0,1 indikerar rad 0, kolumn 1 i grid-layouten
        layout.addWidget(currentTime,1,0,1,2) #0,1 indikerar rad 0, kolumn 1 i grid-layouten
        layout.addWidget(statsButton, 2,0)
        layout.addWidget(fileButton,2,1)
        layout.addWidget(LoRaButton,3,0)
        layout.addWidget(SettingsButton,3,1)

        return page
        
    def jumpToPage(self, page: QWidget):
        """ En funktion för knappklick som byter till ny sida
        """
        self.stack.setCurrentWidget(page)


        
    def greetingPhrase(self) -> QLabel:
        """
        En funktion som skapar en label med en hälsningsfras som beror på tid på dygnet.
        """
        currentHour = QTime.currentTime().hour()
        if currentHour < 12:
            greeting = "Good morning!"
        elif currentHour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        
        greetingLabel = QLabel(greeting)
        greetingLabel.setFixedSize(216, 38)  
        greetingLabel.setStyleSheet("color: #cc6699; font-family: 'Super Vibes'; font-size: 21px; ") #Daily Bubble är en custom font: dafont.com/daily-bubble.font

        return greetingLabel     


class menuButton(QPushButton):
    """
    En klass för att skapa återanvändbara knappar till menufunktionaliteten
    """  
    def __init__(self, title, width= 144, height=144):
      
        super().__init__(title)
        self.title = title
        self.setFixedSize(width, height)
        #button styling: 
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #093;
                color: black;
                border-radius: 15px;
                font-family: 'Daily Bubble';
                font-size: 19px;
            }
            QPushButton::hover { /* byter färg när musen är över knappen */
                background-color: #0a5;
            }

            """)
        self.clicked.connect(self.buttonClick)
        
    def buttonClick(self): #funktionalitet för att se om knappen har klickats
        print("knappen: "+ self.title + " klickades.")
        
        


class timeKeeper(QLabel):
    """
    En klass som skapar en "label" som sedan visar den aktuella tiden på startsidan.
    """
    def __init__(self, width=305, height=62):
        super().__init__()
        self.setFixedSize(int(width), int(height))  


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateClock)
        self.timer.start(1000)

        self.updateClock()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
        background-color: #ff9966;   /* ljusgrön bakgrund*/
        border-radius: 10px;         
        padding: 10px;   
        color: white;
        font-family: 'Super Vibes';
        font-size: 28px;            
        """)

    def updateClock(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        self.setText(current_time)




class filesWindow(QWidget):
    """
        En klass för filhanteringsfönstret
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(320, 480))
        self.backButton = QPushButton(" Home")
        self.backButton.setFixedSize(144, 48)
        shadow = QGraphicsDropShadowEffect(self.backButton)
        shadow.setBlurRadius(10)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)
        self.backButton.setStyleSheet("""
            QPushButton {
                color: black;
                font-family: 'Daily Bubble';
                font-size: 14px;
                background-color:  #389392 ;   
                border-radius: 10px;
            }
            QPushButton::hover {
                background-color: #0a5;
            }
      
        """)

        self.filesLabel = QLabel()
        getFiles = self.getFiles() #hämtar filerna från getFiles funktionen
        self.setStyleSheet("color: black; font-family: 'Daily Bubble'; font-size: 14px;")
        layout = QGridLayout()

        layout.addWidget(self.filesLabel,1,0,1,1)
        layout.addWidget(self.backButton, 0, 0, 1, 1)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.setLayout(layout)
        
    def getFiles(self):
        """Läser alla rader och visar dem i labeln."""
        try:
            rows = []
            with open('/home/charlotta/Documents/temp.txt') as filesText:
                for line in filesText:
                    rows.append(f"<p>{line.strip()}</p>")
            self.filesLabel.setText("".join(rows) if rows else "Inga filer hittades")
        except Exception as e:
            print("could not locate files:", e)
            self.filesLabel.setText("Fel: {e}</i>")
            return None


class statsWindow(QWidget):
    """
        En klass för systemstatistik-fönstret
    """

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(320, 480)) 
        sysTemp = self.getSystemTemp()
        tempLabel = QLabel(" System temp: "+ str(sysTemp))
        cpuLoad = self.getCpuLoad()
        self.backButton = QPushButton(" Home")
        cpuLoadLabel = QLabel(" CPU load: " + str(cpuLoad))

        # self.updateTimer = QTimer(self)
        # self.updateTimer.timeout.connect(self.updateStats)
        # self.updateTimer.start(1000)
        shadow = QGraphicsDropShadowEffect(self.backButton)
        shadow.setBlurRadius(10)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)


        cpuLoadLabel.setStyleSheet("""
            color: black;
            font-family: 'Daily Bubble';
            font-size: 14px;
            background-color: #ffcc66;   
            border-radius: 10px;
            padding: 10px;
            """)
     
        tempLabel.setStyleSheet(
            """
            color: black;
            font-family: 'Daily Bubble';
            font-size: 14px;
            background-color: #ffcc66;   
            border-radius: 10px;
            padding: 10px;
         

            """
        )
       
        self.backButton.setStyleSheet("""
                                      
            QPushButton {
                color: black;
                font-family: 'Daily Bubble';
                font-size: 14px;
                background-color:  #389392 ;   
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton::hover {
                background-color: #0a5;
            }
           
            """

        )
        layout = QGridLayout()
        layout.addWidget(tempLabel,1,1, 1,1) 
        layout.addWidget(cpuLoadLabel,2,1, 1,1) 
        layout.addWidget(self.backButton, 0, 0, 1, 2) 
        
      
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
   
        self.setLayout(layout)

    # def updateStats(self):
    #     sysTemp = self.getSystemTemp()
    #     cpuLoad = self.getCpuLoad()
        
    def getSystemTemp(self):
         try:
             with open ('/sys/class/thermal/thermal_zone0/temp') as tempStatFile: #systemStat path här är definierad för mitt specifika OS.
                 tempValue = tempStatFile.read().strip()
                 return float(tempValue) / 1000.0
         except:
             print("could not locate temp info")
             return None
         
    def getCpuLoad(self):
         try:
             with open('/proc/loadavg') as loadAvgFile:
                 loadAvg = loadAvgFile.read().strip()
                 return loadAvg.split()[0] 
         except:
             print("could not locate CPU load info")
             return None
         
    
    

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

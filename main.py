#DISCLAIMER: 
    #Några externa fonts kan behöva laddas ner för att köra programmet:
        #    https://www.dafont.com/super-vibes.font
        #    https://www.dafont.com/daily-bubble.font
    # Filsökvägen på rad 125 kan behöva justeras
import sys
from PyQt5.QtGui import QFont
import os, time
from LoRaWAN import LoRa
from secrets import DEV_EUI, APP_EUI, APP_KEY  
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
   )

USE_SCALE     = False         
SCALE_FACTOR  = 0.48          # skalar ner storleken från 667×1000 --> 320×480 om aktiverad

def S(v: int) -> int:         
    return int(v * SCALE_FACTOR) if USE_SCALE else v


class MainWindow(QMainWindow):
    """ 
    En klass för att skapa huvudfönstret i applikationen. 
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(S(667), S(1000))) #667x1000 är samma ratio som LCD-skärmen (320x480)
        self.setWindowTitle("PiGUIn")
        currentTime = timeKeeper()
        layout = QGridLayout() #med denna layout så sorteras de tillagda komponenterna i en grid-layout
        fileButton = menuButton("Files")
        statsButton = menuButton("System stats")
        LoRaButton = menuButton("LoRa") 
        SettingsButton = menuButton("Settings") #settings knappen är inte implementerad än

        #Nedan byter till motsvarande fönstret när knappen klickas
        statsButton.clicked.connect(self.showstats) 
        fileButton.clicked.connect(self.showfiles) 
        LoRaButton.clicked.connect(self.showLoRa)
        #SettingsButton.clicked.connect(self.showSettings) 
       


        layout.addWidget(self.greetingPhrase(),0,0) #0,1 indikerar rad 0, kolumn 1 i grid-layouten
        layout.addWidget(currentTime,1,0) #0,1 indikerar rad 0, kolumn 1 i grid-layouten
        layout.addWidget(statsButton, 2,0)
        layout.addWidget(fileButton,2,1)
        layout.addWidget(LoRaButton,3,0)
        layout.addWidget(SettingsButton,3,1)

        containerBox = QWidget()
        containerBox.setLayout(layout)
        self.setCentralWidget(containerBox)
        self.fileButton = filesWindow()
        self.statsPage = statsWindow() #kollar om statsknappen klickats och skickar isf vidare till statswindow classen
        self.LoRaPage = LoRaWindow()
    

    def greetingPhrase(self):
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
        greetingLabel.setFixedSize(S(450), S(80))  
        greetingLabel.setStyleSheet("color: #cc6699; font-family: 'Super Vibes'; font-size: S(45)px; ") #Daily Bubble är en custom font: dafont.com/daily-bubble.font

        return greetingLabel        
        
    def showstats(self, checked):
       self.statsWindow = statsWindow()
       self.statsWindow.show()
        
    def showfiles(self, checked):
        self.filesWindow = filesWindow()
        self.filesWindow.show()  

    def showLoRa(self, checked):
        self.LoRaWindow = LoRaWindow()
        self.LoRaWindow.show()  
        
    # def showSettings(self, checked):
    #     self.settingsWindow = settingsWindow()      
    #     self.settingsWindow.show()
        


class menuButton(QPushButton):
    """
    En klass för att skapa återanvändbara knappar till menufunktionaliteten
    """  
    def __init__(self, title, width= S(300), height=S(300)):
        super().__init__(title)
        self.title = title
        self.setFixedSize(width, height)
        self.setStyleSheet(
            """
                background-color: #093; 
                color: black;
                border-radius: 15px;
                font-family: 'Daily Bubble';
                font-size: S(40)px;
            """)
        self.clicked.connect(self.buttonClick)
        
    def buttonClick(self): #funktionalitet för att se om knappen har klickats
        print("knappen: "+ self.title + " klickades.")
        
        


class timeKeeper(QLabel):
    """
    En klass som skapar en "label" som sedan visar den aktuella tiden på startsidan.
    """
    def __init__(self, width=S(637), height=S(130)):
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
        font-size: S(60)px;            
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
        self.setFixedSize(QSize(S(667), S(1000))) #667x1000 är samma ratio som LCD-skärmen (320x480)
        label = QLabel(" Fortfarande i utveckling  ")
        self.setStyleSheet("color: black; font-family: 'Daily Bubble'; font-size: S(30)px;")
        layout = QGridLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        

    
class LoRaWindow(QWidget):
    """
    En klass för LoRa fönstret
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(S(667), S(1000))) #667x1000 är samma ratio som LCD-skärmen (320x480)
        label = QLabel(" Fortfarande i utveckling ")
        self.setStyleSheet("color: black; font-family: 'Daily Bubble'; font-size: S(30)px;")
        layout = QGridLayout()
        self.getLoRaData()  
        layout.addWidget(label)
        self.setLayout(layout)

    def getLoRaData(self):
        label = QLabel("LoRa module is connecting...")
   
        counter = 0
        try: 
            lora = LoRa(debug=True) 
            lora.configure(DEV_EUI, APP_EUI, APP_KEY)
        except Exception as e:
            print("Error configuring LoRa module:", e)
            label.setText("Error configuring LoRa module: " + str(e))
        try:     
            lora.startJoin()
            print("Start Join…")
            label.setText("Start Join…")
        except Exception as e:
            print("Error starting join:", e)
            label.setText("Error starting join: " + str(e))
         
        while not lora.checkJoinStatus():
            print("Joining…")
            label.setText("Joining…")
            counter += 1
            time.sleep(1)
            if counter > 10:  # Timeout after 30 seconds
                label.setText("Timeout, could not connect to LoRa")
                print("Timeout, could not connect to LoRa")

                return
        print("Successfully joined!")
        label.setText("Successfully oined!") 
   

class statsWindow(QWidget):
    """
        En klass för systemstatistik fönstret
    """

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(S(667), S(1000))) #667x1000 är samma ratio som LCD-skärmen (320x480)
        self.system_temp = self.getSystemTemp()
        sysTemp = self.getSystemTemp()
        tempLabel = QLabel(" System temp: "+ str(sysTemp))
        cpuLoad = self.getCpuLoad()
        cpuLoadLabel = QLabel(" CPU load: " + str(cpuLoad))
        cpuLoadLabel.setStyleSheet(
            """
            color: black;
            font-family: 'Daily Bubble';
            font-size: S(30)px;
            background-color: #ffcc66;   /* ljusgrön bakgrund*/
            border-radius: 10px;
            padding: 10px;
            
            """)
 
            
        tempLabel.setStyleSheet(
            """
            color: black;
            font-family: 'Daily Bubble';
            font-size: S(30)px;
            background-color: #ffcc66;   /* ljusgrön bakgrund*/
            border-radius: 10px;
            padding: 10px;
            """
        )
        layout = QGridLayout()
        layout.addWidget(tempLabel,0,1)
        layout.addWidget(cpuLoadLabel,1,1)
      
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setLayout(layout)
        
        
        
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

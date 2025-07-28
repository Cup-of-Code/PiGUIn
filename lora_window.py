from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import QSize
from secrets import  DEV_EUI, APP_EUI, APP_KEY  
from LoRaWAN import LoRa 
import time


USE_SCALE     = False
SCALE_FACTOR  = 0.48          # skalar ner storleken från 667×1000 --> 320×480 om aktiverad
def S(v: int) -> int:         
    return int(v * SCALE_FACTOR) if USE_SCALE else v


class LoRaWindow(QWidget):
    """
    En klass för LoRa fönstret
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(S(667), S(1000))) #667x1000 är samma ratio som LCD-skärmen (320x480)
        self.setStyleSheet("color: black; font-family: 'Daily Bubble'; font-size: S(30)px;")
        self.layout = QGridLayout()
        self.startButton = QPushButton("Start LoRa")
        self.startButton.setFixedSize(S(300), S(100))
        self.startButton.setStyleSheet(
            """
            background-color: #093; 
            color: black;
            border-radius: 15px;
            font-family: 'Daily Bubble';
            font-size: S(40)px;
            """)
        connectionState = False
       
        self.statusLabel = QLabel("LoRa connection status: " + str(connectionState))
        self.startButton.clicked.connect(self.loraButtonClicked)
        self.layout.addWidget(self.startButton, 0, 0)
        self.layout.addWidget(self.statusLabel, 1, 0) 
        self.setLayout(self.layout)


    def loraButtonClicked(self, checked=False):
        print("LoRa button clicked")
        connectionState = self.getLoRaData()  #försöker ansluta till nätverket och spara resultatet som True/False
        print("LoRa connection state:", connectionState)

        self.statusLabel.setText("Connecting to LoRa network...") 
        
        

        if (connectionState == True):        
            self.sendMessageButton = QPushButton("Send Message")
            self.sendMessageButton.setFixedSize(S(300), S(100))
            self.sendMessageButton.setStyleSheet(
                """
                background-color: #093; 
                color: black;               
                border-radius: 15px;
                font-family: 'Daily Bubble';
                font-size: S(40)px;
                """)
                                    
            self.statusLabel.setText("LoRa connection status: " + str(connectionState)) #uppdaterar statusen
            self.statusLabel.setStyleSheet(
                """
                color: green;
                font-family: 'Daily Bubble';
                font-size: S(30)px;
            """)

            self.layout.addWidget(self.startButton, 0, 0)
            self.layout.addWidget(self.sendMessageButton, 2, 0)
        
        else:
            self.statusLabel.setText("LoRa connection status: " + str(connectionState))
            self.statusLabel.setStyleSheet(
                """
                color: red;
                font-family: 'Daily Bubble';
                font-size: S(30)px;
            """)
            print("Failed to connect to LoRa network")  


    def getLoRaData(self):
   
        counter = 0
        try: 
            lora = LoRa(debug=True) 
            lora.configure(DEV_EUI, APP_EUI, APP_KEY)
        except Exception as e:
            print("Error configuring LoRa module:", e)
            return False
        try:     
            lora.startJoin()
            print("Start Join…")
        except Exception as e:
            print("Error starting join:", e)
            return False
         
        while not lora.checkJoinStatus():
            print("Joining…")

            counter += 1
            time.sleep(1)
            if counter > 10:  #timeout funktion
                print("Timeout, could not connect to LoRa")

                return False
        print("Successfully joined!")
      
        return True

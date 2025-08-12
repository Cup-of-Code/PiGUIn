from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import QSize,Qt
from secrets import  DEV_EUI, APP_EUI, APP_KEY  
from LoRaWAN import LoRa 
import time


class LoRaWindow(QWidget):
    """
    En klass för LoRa fönstret
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(320, 480)) 
        self.setStyleSheet("color: black; font-family: 'Daily Bubble'; font-size: 14px;")
        self.layout = QGridLayout()
        self.backButton = QPushButton(" Home")
        self.backButton.setFixedSize(144, 48)
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
        """)

        self.startButton = QPushButton("Start LoRa")
        self.startButton.setFixedSize(144, 48)
        self.startButton.setStyleSheet(
            """
            QPushButton {
                background-color: #093; 
                color: black;
                border-radius: 15px;
                font-family: 'Daily Bubble';
                font-size: 19px;
            }
            QPushButton::hover {
                background-color: #0a5;
            }
            """)
        connectionState = False
       
        self.statusLabel = QLabel("LoRa connection status: " + str(connectionState))
        self.startButton.clicked.connect(self.loraButtonClicked)
        self.layout.addWidget(self.startButton, 1, 0)
        self.layout.addWidget(self.backButton, 0, 0)
        self.layout.addWidget(self.statusLabel, 2, 0) 
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setLayout(self.layout)


    def loraButtonClicked(self, checked=False):
        print("LoRa button clicked")
        connectionState = self.getLoRaData()  #försöker ansluta till nätverket och spara resultatet som True/False
        print("LoRa connection state:", connectionState)

        self.statusLabel.setText("Connecting to LoRa network...") 
        
        

        if (connectionState == True):        
            self.sendMessageButton = QPushButton("Send Message")
            self.sendMessageButton.setFixedSize(144, 48)
            self.sendMessageButton.setStyleSheet(
                """
                QPushButton {
                    background-color: #093; 
                    color: black;               
                    border-radius: 15px;
                    font-family: 'Daily Bubble';
                    font-size: 19px;
                }
                QPushButton::hover {
                    background-color: #0a5;
                }
                """)
            self.startButton.setText("restart LoRa")
                                    
            self.statusLabel.setText("LoRa connection status: " + str(connectionState)) #uppdaterar statusen
            self.statusLabel.setStyleSheet(
                """
                color: green;
                font-family: 'Daily Bubble';
                font-size: 14px;
            """)
            self.layout.addWidget(self.backButton, 0, 0)
            self.layout.addWidget(self.startButton, 1, 0)
            self.layout.addWidget(self.sendMessageButton, 2, 0)
            self.layout.addWidget(self.statusLabel, 3, 0)
            self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        else:
            self.statusLabel.setText("LoRa connection status: " + str(connectionState))
            self.statusLabel.setStyleSheet(
                """
                color: red;
                font-family: 'Daily Bubble';
                font-size: 14px;
            """)
            print("Failed to connect to LoRa network")  


    def getLoRaData(self):
   
        counter = 0
        try: 
            lora = LoRa(debug=True) 
            lora.configure(DEV_EUI, APP_EUI, APP_KEY)
        except Exception as e:
            print("Error configuring LoRa module:", e)
            return True
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

#LoraWAN library adapted from https://github.com/iot-lnu/pico-w/blob/main/network-examples/N4_LoRaWAN_Connection/LoRaWAN.py
#works over USB instead of UART

import time
import binascii
import serial

class LoRa:

    def __init__(self, port="/dev/ttyUSB0", baud=115200, debug=False):
        self._serial = serial.Serial(port, baud, timeout=0)
        self.debug = debug
        self.init()

    def checkDeviceConnect(self):
        self.writeCMD("AT+CGMI?\r\n")
        restr = self.getResponse()
        return "OK" in restr

    def checkJoinStatus(self):
        self.writeCMD("AT+CSTATUS?\r\n")
        restr = self.getResponse()
        return "+CSTATUS:" in restr and "08" in restr

    def waitMsg(self, t):
        restr = b""
        start = time.time()
        while (time.time() - start) * 1000 < t:
            res = self._serial.readline()
            if res:
                restr += res
        return restr.decode(errors="ignore")

    def writeCMD(self, command):
        self._serial.write(command.encode())
        time.sleep(0.1)

    def sendMsg(self, data, confirm=1, nbtrials=1):
        cmd = f"AT+DTRX={confirm},{nbtrials},{len(data)},{data}\r\n"
        if self.debug:
            print("SENT", cmd)
        self.writeCMD(cmd)
        self.getResponse()

    def setSpreadingFactor(self, sf):
        cmd = f"AT+CDATARATE={sf}\r\n"
        self.writeCMD(cmd)
        self.getResponse()

    def receiveMsg(self):
        restr = self.getResponse()
        if "OK+RECV:" in restr and "02,00,00" not in restr:
            data = restr[restr.find("OK+RECV:") + 17:-2]
            return self.decodeMsg(data)
        return ""

    def configOTTA(self, device_eui, app_eui, app_key, ul_dl_mode):
        self.writeCMD("AT+CJOINMODE=0\r\n")
        self.getResponse()
        self.writeCMD("AT+CDEVEUI=" + device_eui + "\r\n")
        self.getResponse()
        self.writeCMD("AT+CAPPEUI=" + app_eui + "\r\n")
        self.getResponse()
        self.writeCMD("AT+CAPPKEY=" + app_key + "\r\n")
        self.getResponse()
        self.writeCMD("AT+CULDLMODE=" + ul_dl_mode + "\r\n")
        self.getResponse()

    def configABP(self, device_addr, app_skey, net_skey, ul_dl_mode):
        self.writeCMD("AT+CJOINMODE=1\r\n")
        self.getResponse()
        self.writeCMD("AT+CDEVADDR=" + device_addr + "\r\n")
        self.getResponse()
        self.writeCMD("AT+CAPPSKEY=" + app_skey + "\r\n")
        self.getResponse()
        self.writeCMD("AT+CNWKSKEY=" + net_skey + "\r\n")
        self.getResponse()
        self.writeCMD("AT+CULDLMODE=" + ul_dl_mode + "\r\n")
        self.getResponse()

    def setClass(self, mode):
        self.writeCMD("AT+CCLASS=" + mode + "\r\n")

    def setRxWindow(self, freq):
        self.writeCMD("AT+CRXP=0,0," + freq + "\r\n")

    def setFreqMask(self, mask):
        self.writeCMD("AT+CFREQBANDMASK=" + mask + "\r\n")

    def startJoin(self):
        self.writeCMD("AT+CJOIN=1,0,10,8\r\n")

    def decodeMsg(self, hexEncoded):
        if len(hexEncoded) % 2 == 0:
            buf = hexEncoded
            tempbuf = []
            for i in range(0, len(buf), 2):
                tempbuf.append(chr(int(buf[i:i+2], 16)))
            return "".join(tempbuf)
        return hexEncoded

    def getResponse(self):
        time.sleep(0.05)
        restr = self.waitMsg(200)
        if self.debug:
            print(restr)
        return restr

    def init(self):
        while not self.checkDeviceConnect():
            time.sleep(0.5)
        if self.debug:
            print("Module Connected")

        self.writeCMD("AT+CRESTORE\r\n")
        self.writeCMD("AT+ILOGLVL=1\r\n")
        self.writeCMD("AT+CSAVE\r\n")
        self.writeCMD("AT+IREBOOT=0\r\n")
        time.sleep(1)

        while not self.checkDeviceConnect():
            time.sleep(0.5)

    def configure(self, devui, appeui, appkey):
        print("Module Config...")
        self.configOTTA(devui, appeui, appkey, "2")
        self.setClass("2")
        self.writeCMD("AT+CWORKMODE=2\r\n")
        self.setSpreadingFactor("5")
        self.setRxWindow("869525000")
        self.setFreqMask("0001")


# Example usage
if __name__ == "__main__":
    lora = LoRa(debug=True)
    # lora.configure("devEUI", "appEUI", "appKey")
    # lora.sendMsg("48656C6C6F")  # Send "Hello" in hex



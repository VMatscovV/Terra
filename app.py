import sys, os
import speech_recognition
from PyQt5.QtWidgets import (QPushButton, QApplication, QMainWindow, QStatusBar, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from playsound import playsound
import webbrowser
import pywifi
from pywifi import const
import psutil


class Window(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setGeometry(800, 200, 400, 500)
        self.setWindowTitle('TERRA')
        self.setWindowIcon(QIcon('icon.png'))

        self.profile = pywifi.Profile()
        self.profile.ssid = "MTS_GPON5_C0B4"
        # 'Bizbi-24'
        self.profile.key = "CKRxkC3f"
        # '94475272'
        self.wifi = pywifi.PyWiFi()
        self.iface = self.wifi.interfaces()[0]
        self.profile = self.iface.add_network_profile(self.profile)

        self.initUI()



    def initUI(self):

        self.centrallab = QLabel()
        if self.iface.status() == const.IFACE_CONNECTED:
            self.mess = "<h2>Hello, I'm ready<h2>"
        else:
            self.mess = "<h2>Please, turn on wi-fi<h2>"
        self.centrallab.setText(self.mess)
        self.centrallab.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centrallab)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("ready")

        self.col = QPushButton("Start", self)
        self.col.resize(50, 50)
        self.col.move(175, 400)
        self.col.setStyleSheet(
            "QPushButton {background-color: rgb(239,205,82); color: rgb(0,0,0); border-radius: 25px;}"
            "QPushButton:pressed {background-color: rgb(230,200,80); color: rgb(0,0,0);}")
        self.col.clicked.connect(self.record_and_recognize_audio)

        self.con = QPushButton("WI-FI", self)
        self.con.resize(40, 40)
        self.con.move(340, 20)
        self.con.setStyleSheet(
            "QPushButton {background-color: rgb(180,180,230); color: rgb(0,0,0); border-radius: 20px;}"
            "QPushButton:pressed {background-color: rgb(180,180,255); color: rgb(0,0,0);}")
        self.con.clicked.connect(self.wifion)

        self.show()



    def wifion(self):
        if self.iface.status() == const.IFACE_DISCONNECTED:
            self.centrallab.setText("<h2>Hello, I'm ready<h2>")
            self.iface.connect(self.profile)



    def record_and_recognize_audio(self):
        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()

        with microphone:
            recognized_data = ""
            recognizer.adjust_for_ambient_noise(microphone, duration=2)

            try:
                playsound('your_name.mp3')
                audio = recognizer.listen(microphone, 5, 5)
                playsound('finish.mp3')

            except speech_recognition.WaitTimeoutError:
                self.statusbar.showMessage("Can you check if your microphone is on, please?")
                return

            try:
                recognized_data = recognizer.recognize_google(audio, language="ru").lower()

            except speech_recognition.UnknownValueError:
                pass

            except speech_recognition.RequestError:
                self.statusbar.showMessage("Turn on wi-fi")

        self.statusbar.showMessage(recognized_data)

        if recognized_data.find("закройся") >= 0:
            self.close()

        elif recognized_data.find("найти в google") >= 0:
            search = recognized_data.replace("найти в google ", "")
            url = 'https://www.google.com/search?q=' + search
            webbrowser.register('chrome', None,
                                webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
            webbrowser.get('chrome').open_new(url)
            self.centrallab.setText("<h2>Hello, I'm ready<h2>")

        elif recognized_data.find("открыть") >= 0:
            if recognized_data.find("диспетчер задач") >= 0:
                os.system("taskmgr.exe")
            elif recognized_data.find("настройки операционной системы") >= 0:
                os.system('control.exe')
            elif recognized_data.find("экранную клавиатуру") >= 0:
                os.system('osk.exe')
            self.centrallab.setText("<h2>Hello, I'm ready<h2>")

        elif recognized_data.find("закрыть") >= 0:
            if recognized_data.find("диспетчер задач") >= 0:
                for process in (process for process in psutil.process_iter() if process.name() == "taskmgr.exe"):
                    process.kill()
            elif recognized_data.find("настройки операционной системы") >= 0:
                for process in (process for process in psutil.process_iter() if process.name() == "control.exe"):
                    process.kill()
            elif recognized_data.find("экранную клавиатуру") >= 0:
                for process in (process for process in psutil.process_iter() if process.name() == "osk.exe"):
                    process.kill()
            self.centrallab.setText("<h2>Hello, I'm ready<h2>")

        elif recognized_data.find("вычислить") >= 0:
            try:
                self.centrallab.setText(str(eval(recognized_data.replace("вычислить ", ""))))
            except:
                self.centrallab.setText("<h2>'Сommand not recognized'<h2>")


        elif recognized_data.find("выключить wi-fi") >= 0:
            if self.iface.status() == const.IFACE_CONNECTED:
                self.centrallab.setText("<h2>Please, turn on wi-fi<h2>")
                self.iface.disconnect()

        else:
            self.centrallab.setText("<h2>'Сommand not recognized'<h2>")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())

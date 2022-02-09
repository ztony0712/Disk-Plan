import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
# import serial
import time

# print("Start")
# port="/dev/tty.HC-06-DevB" #This will be different for various devices and on windows it will probably be a COM port.
# bluetooth=serial.Serial("COM5", 9600)#Start communications with the bluetooth unit
# print("Connected")
# bluetooth.flushInput() #This gives the bluetooth a little kick

class Communicate(QObject):

    updatePB = pyqtSignal(int)
    updateND = pyqtSignal()

class ProgressBar(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setMinimumSize(1, 50)
        self.value = 0
        self.num = [-600, -450, -300, -150, 0, 150, 300, 450, 600]

    def setValue(self, value):

        self.value = value     ##传值


    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):

        font = QFont('Serif', 15, QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / 10.0))

        till = int(((w / 1500.0) * self.value))
        full = int(((w / 1500.0) * 450))

        if self.value >= 450:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(580, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(full+580, 0, till-full, h)

        elif self.value <= -450:

            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(580-full, 0, full, h)
            qp.setPen(QColor(255, 175, 175))
            qp.setBrush(QColor(255, 175, 175))
            qp.drawRect(580-full, 0, till+full, h)

        else:
            qp.setPen(QColor(255, 255, 255))
            qp.setBrush(QColor(255, 255, 184))
            qp.drawRect(580, 0, till, h)

        pen = QPen(QColor(20, 20, 20), 1,
                   Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(Qt.NoBrush)
        qp.drawRect(0, 0, w, h)

        j = 0

        for i in range(step, 10*step, step):

            qp.drawLine(i, 0, i, 5)
            metrics = qp.fontMetrics()
            fw = metrics.width(str(self.num[j]))
            qp.drawText(i-fw/2, h/2, str(self.num[j]))
            j = j + 1


class DiskPanel(QWidget):
    needle = QPolygon([
        QPoint(4, 8),
        QPoint(-4, 8),
        QPoint(0, -90)
    ])
    needleColor = QColor(0, 0, 255)
    diskColor = [QColor(255, 0, 0),    #red
        QColor(255, 192, 0),  #yellow
        QColor(255, 0, 0),    #red
        QColor(112, 173, 71), #green
        QColor(255, 0, 0),    #red
        QColor(112, 173, 71)] #green

    def __init__(self, parent=None):
        super(DiskPanel, self).__init__(parent)

        self.signal = ['Stop', 'Right', 'Stop', 'Left', 'Stop', 'Forward']

        self.c = Communicate()
        self.angle = 60
        self.n = 0
        self.setWindowTitle("Gui for controller")
        self.setFixedSize(1200, 700)
        self.drawText()
        self.initUI()
        self.c.updateND.connect(self.update)


    def setAngle(self, angle):

        self.angle = angle


    def paintEvent(self, e):
        
        painter = QPainter()
        painter.begin(self)
        self.drawBackground(painter)
        painter.end()

    def drawBackground(self, painter):
        side = min(self.width(), self.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 300.0, side / 300.0)

        rect = QRect(-100, -100, 200, 200)
        painter.setPen(QColor(0, 0, 0))

        for x in range(6):
            painter.setBrush(DiskPanel.diskColor[x])
            painter.drawPie(-100, -100, 200, 200, 16*(60*x), 16*60)

        # inner circle
        painter.setPen(QColor(0, 0, 0))
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(-50, -50, 100, 100)


        painter.rotate(self.angle)
        painter.setPen(Qt.NoPen)
        painter.setBrush(DiskPanel.needleColor)
        painter.drawConvexPolygon(DiskPanel.needle)

        # point
        radGradient = QRadialGradient(0,0,10)
        radGradient = QConicalGradient(0, 0, -90)
        radGradient.setColorAt(0.0, Qt.darkGray)
        radGradient.setColorAt(0.5, Qt.white)
        radGradient.setColorAt(1.0, Qt.darkGray)
        painter.setPen(Qt.NoPen)
        painter.setBrush(radGradient)
        painter.drawEllipse(-5,-5,10,10)


    def drawText(self):
        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)
        label4 = QLabel(self)
        label5 = QLabel(self)
        label6 = QLabel(self)

        font = QFont()
        font.setBold(True)
        font.setPointSize(25)
        font.setWeight(6000)

        label1.setFont(font)
        label2.setFont(font)
        label3.setFont(font)
        label4.setFont(font)
        label5.setFont(font)
        label6.setFont(font)

        label1.setText("<font color=%s>%s</font>" % ('white', "Forward"))
        label2.setText("<font color=%s>%s</font>" % ('white', "Stop"))
        label3.setText("<font color=%s>%s</font>" % ('white', "Stop"))
        label4.setText("<font color=%s>%s</font>" % ('white', "Left"))
        label5.setText("<font color=%s>%s</font>" % ('white', "Right"))
        label6.setText("<font color=%s>%s</font>" % ('white', "Stop"))

        label1.move(555, 160)
        label2.move(400, 290)
        label3.move(740, 290)
        label4.move(480, 470)
        label5.move(680, 470)
        label6.move(555, 520)


    def initUI(self):

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setRange(-600, 600)
        sld.setValue(0)
        sld.setGeometry(500, 40, 150, 30)

        self.wid = ProgressBar()
        self.c.updatePB[int].connect(self.wid.setValue)

        sld.valueChanged[int].connect(self.changeValue)
        hbox = QHBoxLayout()
        hbox.addWidget(self.wid)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.sld = sld



    def changeValue(self, value):
        action = 'Stop'
        action_match_dic = {'Stop':0, 'Right':1, 'Left':2, 'Forward':3}

        self.c.updatePB.emit(value)
        self.wid.repaint()

    # logic
        x = ""
        if value == 600:
            self.n += 1
            if self.n >= 6:
                self.n = 0
            value = 0
            self.sld.setValue(0)
            self.angle += 60
            self.c.updateND.emit()
            action = self.signal[self.n]
            x = str(self.n)
            print(action + x)
            
        elif value == -600:
            self.n -= 1
            if self.n <= -1:
                self.n = 5
            value = 0
            self.sld.setValue(0)
            self.angle -= 60
            self.c.updateND.emit()
            action = self.signal[self.n]
            x = str(self.n)
            print(action + x)

        # cmd = action_match_dic.get(action,'0')
        # '''put your bluetooth serial connection here
        #    and use variable cmd as controller as follow:
        #   {'Stop':0, 'Right':1, 'Left':2, 'Forward':3}
        # '''

        # if cmd == 0:
        #     print("Ping")
        #     bluetooth.write(b"BOOP 1")#These need to be bytes not unicode, plus a number
        #     input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
        #     print(input_data.decode())#These are bytes coming in so a decode is needed
        #     time.sleep(0.1) #A pause between bursts

        # elif cmd == 1:
        #     print("Ping")
        #     bluetooth.write(b"BOOP 2")#These need to be bytes not unicode, plus a number
        #     input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
        #     print(input_data.decode())#These are bytes coming in so a decode is needed
        #     time.sleep(0.1) #A pause between bursts

        # elif cmd == 2:
        #     print("Ping")
        #     bluetooth.write(b"BOOP 3")#These need to be bytes not unicode, plus a number
        #     input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
        #     print(input_data.decode())#These are bytes coming in so a decode is needed
        #     time.sleep(0.1) #A pause between bursts

        # elif cmd == 3:
        #     print("Ping")
        #     bluetooth.write(b"BOOP 4")#These need to be bytes not unicode, plus a number
        #     input_data=bluetooth.readline()#This reads the incoming data. In this particular example it will be the "Hello from Blue" line
        #     print(input_data.decode())#These are bytes coming in so a decode is needed
        #     time.sleep(0.1) #A pause between bursts

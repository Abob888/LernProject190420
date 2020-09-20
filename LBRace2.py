import sys, random, time
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (QMainWindow, QFrame, QApplication,
                             QPushButton, QLabel, QAction, qApp)
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QTimer
from PyQt5.QtGui import QPainter, QColor, QIcon, QPixmap, QPalette


class LadyBird(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&Exit')
        self.fileMenu.addAction(self.exitAction)

        self.showResults = QAction(QIcon('show.png'), '&Show results', self)
        self.showResults.setShortcut('Ctrl+S')
        self.showResults.setStatusTip('Show list of results')
        self.showResults.triggered.connect(self.on_displ)
        self.saveMenu = self.menubar.addMenu('&Results')
        self.saveMenu.addAction(self.showResults)

        self.clearResults = QAction(QIcon('clear.png'), '&Clear results', self)
        self.clearResults.setShortcut('Ctrl+C')
        self.clearResults.setStatusTip('Clear list of results')
        self.clearResults.triggered.connect(self.on_del)
        self.saveMenu.addAction(self.clearResults)

        self.lbrace = Race(self)
        self.setCentralWidget(self.lbrace)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage(str('Ready'))

        self.lbrace.msg2Statusbar.connect(self.statusbar.showMessage)

        self.pal = self.palette()
        self.pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QColor(230, 230, 190))
        self.pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor(230, 230, 190))
        self.setPalette(self.pal)

        self.setFixedSize(QtCore.QSize(470, 710))
        self.setWindowTitle("LadyBirds Race")
        self.setWindowIcon(QIcon('lb.png'))

        self.show()

    def on_displ(self):
        global modalWindow
        self.modalWindow = QtWidgets.QWidget(lbrace, QtCore.Qt.Window)



        self.modalWindow.setWindowTitle('The Score')
        self.modalWindow.resize(500, 700)
        self.modalWindow.setWindowModality(QtCore.Qt.WindowModal)
        self.modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.modalWindow.move(20, 20)
        try:
            self.f = open('results.txt', 'r')
        except FileNotFoundError:
            self.statusbar.showMessage(str('No Results yet'))
        self.scores = QLabel(self.modalWindow)
        with open("results.txt", "r") as f:
            self.scores.setText(f.read())
        self.f.close()
        self.scores.show()

        self.modalWindow.show()


    def on_del(self):
        try:
            self.f = open('results.txt', 'w')
            self.statusbar.showMessage(str('No Results any more'))
        except FileNotFoundError:
            self.statusbar.showMessage(str('No Results to delete'))
        self.f.close()



class Race(QFrame):

    msg2Statusbar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.initRace()

    def initRace(self):

        self.fin = 0

        self.startButton = QPushButton("START", self)
        self.startButton.move(150, 20)

        self.saveButton = QPushButton("SAVE", self)
        self.saveButton.move(250, 20)
        self.saveButton.setDisabled(True)

        self.dlb = self.drawLb(609)

        self.ts = QLabel(self)
        self.ts.setText('Time: ')
        self.ts.move(410, 20)

        self.ti = 0
        self.timer = QTimer()

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.c2y = 609
        self.pixmap3 = QPixmap("lb3.png")
        self.lbl2 = QLabel(self)
        self.lbl2.setPixmap(self.pixmap3)
        self.lbl2.move(415 + random.randint(-7, 7), self.c2y)

        if self.c2y < 112:
            self.fin = 1
        self.startButton.clicked.connect(self.startLB)

        self.timer.timeout.connect(self.on_timeout)

        self.saveButton.clicked.connect(self.on_save)




    def paintEvent(self, e):
        lb = QPainter()
        lb.begin(self)
        self.drawRect(lb)
        lb.end()


    def drawRect(self, lb):
        for i in range(5):
            x = i * 100
            col = QColor(0, 0, 0)
            col.setNamedColor('green')
            lb.setPen(col)
            lb.setBrush(QColor(111, 150, 50))
            lb.drawRect(x + 5, 80, 60, 570)



    def drawLb(self, y):
        for a in range(4):
            x = a * 100 + random.randint(-9, 9)
            pixmap = QPixmap("lb3.png")
            lbl = QLabel(self)
            lbl.resize(40, 40)
            lbl.setPixmap(pixmap)
            lbl.move(x + 15, y)
        for b in range(5):
            pixmap2 = QPixmap("finish.png")
            ff = QLabel(self)
            ff.setPixmap(pixmap2)
            ff.move(b * 100 + 5, 80)

    def keyPressEvent(self, e):

        if self.startButton.isEnabled() == False:
            self.c2y -= 15 + random.randint(-7, 7)
            self.c2x = 415 + random.randint(-7, 7)
            self.lbl2.move(self.c2x, self.c2y)
            self.lbl2.show()
            if self.c2y < 112:
                self.timer.stop()
                self.msg2Statusbar.emit('Finished')
                self.startButton.setDisabled(False)
                self.fin = 1
                winner12 = QLabel(self)
                winner12.setText('Winner')
                winner12.move(415, 60)
                winner12.show()
                pixmap2 = QPixmap("finish.png")
                ff = QLabel(self)
                ff.setPixmap(pixmap2)
                ff.move(405, 80)
                ff.show()
        QtWidgets.QFrame.keyPressEvent(self, e)


    def startLB(self, e):
        pixmapsh2 = QPixmap("yl.png")
        shild2 = QLabel(self)
        shild2.resize(469, 20)
        shild2.setPixmap(pixmapsh2)
        shild2.move(1, 55)
        shild2.show()
        self.startButton.setDisabled(True)
        self.msg2Statusbar.emit('Started')
        self.ti = 0
        self.winner1 = 0
        winner12 = None
        self.timer.start(10)
        c = 606
        istap = 0
        koordinate = []
        speed = []
        kori = []
        for k in range(4):
            speed.append(random.randint(1, 6),)
            speedlist = QLabel(self)
            nub = str(k + 1)
            speedlist.setText('# ' + nub)
            speedlist.move(k * 100 + 15, 650)
            speedlist.show()
        for k2 in range(5):
            kori.append(c)
        speedlist5 = QLabel(self)
        speedlist5.setText('# 5')
        speedlist5.move(415, 650)
        speedlist5.show()

        '''finish = Race.keyPressEvent(self)
        if finish:
            break startLB()'''

        while c >= 112:
            QtWidgets.qApp.processEvents()

            for b in range(4):

                cx = b * 100 + random.randint(-7, 7) + 15
                ki = int(kori[b])
                ssp = int(speed[b])
                cy = ki - (ssp + b)

                pixmapsh = QPixmap("green.png")
                shild = QLabel(self)
                shild.resize(55, 540)
                shild.setPixmap(pixmapsh)
                shild.move(b * 100 + 7, 110)
                shild.show()

                pixmap = QPixmap("lb3.png")
                lbl = QLabel(self)
                lbl.resize(40, 40)
                lbl.setPixmap(pixmap)
                lbl.move(cx, cy)
                lbl.show()

                pixmap2 = QPixmap("finish.png")
                ff = QLabel(self)
                ff.setPixmap(pixmap2)
                ff.move(b * 100 + 5, 80)
                ff.show()

                time.sleep(0.007)

                kori.insert(b, cy)

                koordinate.append(cy)
                con = min(koordinate)

                istap += 1

                if kori[b] <= 112:
                    self.winner1 = str(b + 1)
                    winner12 = QLabel(self)
                    winner12.setText('Winner')
                    winner12.move(b * 100 + 15, 60)
                    winner12.show()
                    break

            c = con

        self.timer.stop()

        self.msg2Statusbar.emit('Finished')
        self.startButton.setDisabled(False)
        self.saveButton.setDisabled(False)

        return self.winner1

    def on_timeout(self):
        self.ti += 1
        self.pixmapt = QPixmap("tablo.png")
        self.shild2 = QLabel(self)
        self.shild2.resize(30, 20)
        self.shild2.setPixmap(self.pixmapt)
        self.shild2.move(435, 19)
        self.shild2.show()
        self.tido = QLabel(self)
        self.tido.setText(str(self.ti))
        self.tido.move(440, 20)
        self.tido.show()
        return self.ti
        # self.ti = 0

    def on_save(self):
        self.f = open('results.txt', 'a')
        a1 = time.strftime('%d.%m.%Y')
        a2 = time.strftime('%H.%M.%S')
        self.f.write(a1)
        self.f.write(' ')
        self.f.write(a2)
        self.f.write(' And the Winner is # ')
        self.f.write(str(self.winner1))
        self.f.write(' Time: ')
        self.f.write(str(self.ti))
        self.f.write('\n')
        self.f.close()
        self.msg2Statusbar.emit('Race is saved')
        self.saveButton.setDisabled(True)


if __name__ == '__main__':
    app = QApplication([])
    lbrace = LadyBird()
    desktop = QtWidgets.QApplication.desktop()
    lbrace.move(desktop.availableGeometry().center() -
                lbrace.rect().center())
    sys.exit(app.exec())

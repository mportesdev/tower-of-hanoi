#!/usr/bin/python
# coding: utf-8
import sys
from PySide2 import QtWidgets, QtCore, QtGui

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tower of Hanoi")
        self.resize(640, 500)
        self.setStyleSheet("font-family: Arial; font-size: 20px; font-weight bold")
        menu = self.menuBar()
        menu.setStyleSheet("::item:enabled {color: #404070}")

        menuGame = menu.addMenu("&Game")
        item_G_R = QtWidgets.QAction("&Restart", self)
        item_G_D = QtWidgets.QAction("&Difficulty setting...", self)
        item_G_Q = QtWidgets.QAction("&Quit", self)
        menuGame.addAction(item_G_R)
        menuGame.addAction(item_G_D)
        menuGame.addAction(item_G_Q)
        item_G_R.triggered.connect(self.init_state)
        item_G_D.triggered.connect(self.difficulty_dialog)
        item_G_Q.triggered.connect(self.close)
        item_G_R.setShortcut(QtGui.QKeySequence("Ctrl+R"))
        item_G_D.setShortcut(QtGui.QKeySequence("Ctrl+D"))
        item_G_Q.setShortcut(QtGui.QKeySequence("Ctrl+Q"))

        menuColors = menu.addMenu("&Colors")
        item_C_D = QtWidgets.QAction("&Dark", self)
        item_C_L = QtWidgets.QAction("&Light", self)
        menuColors.addAction(item_C_D)
        menuColors.addAction(item_C_L)
        item_C_D.triggered.connect(lambda: self.content.setStyleSheet("color: #e0e0e0; background-color: #404070"))
        item_C_L.triggered.connect(lambda: self.content.setStyleSheet("color: #404070; background-color: #e0e0e0"))

        menuLanguage = menu.addMenu("&Language")
        item_L_E = QtWidgets.QAction("&English", self)
        # item_L_C = QtWidgets.QAction("&Czech", self)
        menuLanguage.addAction(item_L_E)
        # menuLanguage.addAction(item_L_C)
        # item_L_C.setEnabled(False)
        # item_L_C.triggered.connect(lambda: menuLanguage.setText("&Jazyk"))

        menuHelp = menu.addMenu("&Help")
        item_H_H = QtWidgets.QAction("&How to play", self)
        item_H_A = QtWidgets.QAction("&About", self)
        menuHelp.addAction(item_H_H)
        menuHelp.addAction(item_H_A)

        self.content = QtWidgets.QLabel()
        self.setCentralWidget(self.content)
        self.content.setStyleSheet("color: #e0e0e0; background-color: #404070")

        self.content.button1 = QtWidgets.QPushButton(self)
        self.content.button1.clicked.connect(lambda: self.pick_or_drop(0))
        self.content.button2 = QtWidgets.QPushButton(self)
        self.content.button2.clicked.connect(lambda: self.pick_or_drop(1))
        self.content.button3 = QtWidgets.QPushButton(self)
        self.content.button3.clicked.connect(lambda: self.pick_or_drop(2))

        self.content.labelHand = QtWidgets.QLabel()
        self.content.labelHand.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.content.tower1 = QtWidgets.QLabel()
        self.content.tower1.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.content.tower2 = QtWidgets.QLabel()
        self.content.tower2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.content.tower3 = QtWidgets.QLabel()
        self.content.tower3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.content.button1, 4, 1)
        layout.addWidget(self.content.button2, 4, 2)
        layout.addWidget(self.content.button3, 4, 3)
        layout.addWidget(self.content.labelHand, 6, 2)
        layout.addWidget(self.content.tower1, 8, 1)
        layout.addWidget(self.content.tower2, 8, 2)
        layout.addWidget(self.content.tower3, 8, 3)
        self.content.setLayout(layout)
        self.strPick = "\u2191 Pick"      # alternatively: "\u21e7 Pick" or "\u261d Pick"
        self.strDrop = "\u2193 Drop"      #                "\u21e9 Drop"    "\u261f Drop"
        self.stoneChar = "\u2588"
        self.strPeg = "\u2595\u258f"
        self.numStones = 3 # 1-1 2-3 3-7 4-15 5-31 6-63
        self.init_state()

    def init_state(self):
        self.numMoves = 0
        self.target = list(range(self.numStones, 0, -1))
        self.stacks = [self.target[:], [], []]    # [:] for an independent copy
        self.content.button1.setText(self.strPick)
        self.content.button1.setEnabled(True)
        self.content.button1.setShortcut(QtGui.QKeySequence("1"))
        self.content.button2.setText("")
        self.content.button2.setEnabled(False)
        self.content.button3.setText("")
        self.content.button3.setEnabled(False)
        self.hand = 0
        self.draw_hand()
        for i in range(3):
            self.draw_tower(i)
        self.statusBar().showMessage("")
        self.pick_or_drop = self.pick

    def pick(self, n):
        self.lastPick = n
        stack = self.stacks[n]
        self.hand = stack.pop()
        self.draw_hand()
        self.draw_tower(n)
        for stk, btn, key in zip(self.stacks, [self.content.button1, self.content.button2, self.content.button3], ["1", "2", "3"]):
            if stk == [] or stk[-1] > self.hand:
                btn.setText(self.strDrop)
                btn.setEnabled(True)
                btn.setShortcut(QtGui.QKeySequence(key))
            else:
                btn.setText("")
                btn.setEnabled(False)
        self.pick_or_drop = self.drop

    def drop(self, n):
        stack = self.stacks[n]
        stack.append(self.hand)
        self.draw_tower(n)
        self.hand = 0
        self.draw_hand()
        for stk, btn, key in zip(self.stacks, [self.content.button1, self.content.button2, self.content.button3], ["1", "2", "3"]):
            if stk:
                btn.setText(self.strPick)
                btn.setEnabled(True)
                btn.setShortcut(QtGui.QKeySequence(key))
            else:
                btn.setText("")
                btn.setEnabled(False)
        if n != self.lastPick:    # returning a stone to the same position won't count as a move
            self.numMoves += 1
            self.statusBar().showMessage("Moves: " + str(self.numMoves))
        if n == 2 and stack == self.target:    # when dropping on tower 3, test if we are finished
            self.statusBar().showMessage("Solved in " + str(self.numMoves) + " moves.")
            self.content.button1.setText("\u2714")
            self.content.button2.setText("\u2714")
            self.content.button3.setText("\u2714")
            self.content.button3.setEnabled(False)
        self.pick_or_drop = self.pick

    def draw_tower(self, n):
        reversedStack = self.stacks[n][::-1]
        strVisiblePeg = "<font color=\"#b07000\">" + "<br/>".join([self.strPeg for i in range(8 - len(reversedStack))]) + "</font>"
        strStones = ("<br/>" if reversedStack else "") + "<br/>".join([self.stoneChar*i for i in reversedStack])
        strWoodenBase = "<br/><font color=\"#b07000\">" + "\u2580"*9 + "</font>"
        [self.content.tower1, self.content.tower2, self.content.tower3][n].setText(strVisiblePeg + strStones + strWoodenBase)

    def draw_hand(self):
        self.content.labelHand.setText(self.stoneChar*self.hand)

    def difficulty_dialog(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setStyleSheet("font-family: Arial; font-size: 20px; font-weight bold")
        self.dialog.setWindowTitle("Difficulty setting")
        self.dialog.rbutton3 = QtWidgets.QRadioButton("3 stones")
        self.dialog.rbutton4 = QtWidgets.QRadioButton("4 stones")
        self.dialog.rbutton5 = QtWidgets.QRadioButton("5 stones")
        self.dialog.rbutton6 = QtWidgets.QRadioButton("6 stones")
        self.dialog.rbutton7 = QtWidgets.QRadioButton("7 stones")
        for i, rb in zip(range(3, 8), [self.dialog.rbutton3, self.dialog.rbutton4, self.dialog.rbutton5, self.dialog.rbutton6, self.dialog.rbutton7]):
            if i == self.numStones:
                rb.setChecked(True)
                break
        self.dialog.buttonOK = QtWidgets.QPushButton("OK")
        self.dialog.buttonOK.clicked.connect(self.set_difficulty)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.dialog.rbutton3, 1, 1)
        layout.addWidget(self.dialog.rbutton4, 1, 2)
        layout.addWidget(self.dialog.rbutton5, 2, 1)
        layout.addWidget(self.dialog.rbutton6, 2, 2)
        layout.addWidget(self.dialog.rbutton7, 3, 1)
        layout.addWidget(self.dialog.buttonOK, 5, 1, 1, 2)
        self.dialog.setLayout(layout)
        self.dialog.show()

    def set_difficulty(self):
        for i, rb in zip(range(3, 8), [self.dialog.rbutton3, self.dialog.rbutton4, self.dialog.rbutton5, self.dialog.rbutton6, self.dialog.rbutton7]):
            if rb.isChecked():
                self.numStones = i
                break
        self.init_state()
        self.dialog.close()

    def run(self, app):
        self.show()
        app.exec_()

def main():
    app = QtWidgets.QApplication()
    MainWindow().run(app)

if __name__ == "__main__":
    main()

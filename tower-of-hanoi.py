#!/usr/bin/python
# coding: utf-8
import sys
from PySide2 import QtWidgets, QtCore

class main_window(QtWidgets.QLabel):

    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 20px; color: #e0e0e0; background-color: #404070")
        self.strPick = "\u2191 Pick"      # alternatively: "\u21e7 Pick" or "\u261d Pick"
        self.strDrop = "\u2193 Drop"      #                "\u21e9 Drop"    "\u261f Drop"
        self.stoneChar = "\u2588"
        self.numStones = 7
        self.prepare_gui("Tower of Hanoi", 640, 500)
        self.init_state(self.numStones)

    def init_state(self, nstones):
        self.numMoves = 0
        self.target = list(range(nstones, 0, -1))
        self.stacks = [self.target[:], [], []]    # [:] for an independent copy
        self.button1.setText(self.strPick)
        self.button1.setEnabled(True)
        self.button2.setText("")
        self.button2.setEnabled(False)
        self.button3.setText("")
        self.button3.setEnabled(False)
        self.hand.setText("")
        for i in range(3):
            self.draw_tower(i)
        self.labelMoves.setText("")

    def prepare_gui(self, windowTitle, windowWidth, windowHeight):
        self.setWindowTitle(windowTitle)
        self.resize(windowWidth, windowHeight)

        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setStyleSheet("height: 100px; font-size: 28px; background-color: #505080")
        self.button1.clicked.connect(lambda: (self.pick(0) if self.button1.text() == self.strPick else self.drop(0)))
        self.button2 = QtWidgets.QPushButton(self)
        self.button2.setStyleSheet("height: 100px; font-size: 28px; background-color: #505080")
        self.button2.clicked.connect(lambda: (self.pick(1) if self.button2.text() == self.strPick else self.drop(1)))
        self.button3 = QtWidgets.QPushButton(self)
        self.button3.setStyleSheet("height: 100px; font-size: 28px; background-color: #505080")
        self.button3.clicked.connect(lambda: (self.pick(2) if self.button3.text() == self.strPick else self.drop(2)))

        self.hand = QtWidgets.QLabel()
        self.hand.setStyleSheet("height: 50px; color: #00e0ff")
        self.hand.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.tower1 = QtWidgets.QLabel()
        self.tower1.setStyleSheet("height: 200px; color: #00a0c0")
        self.tower1.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.tower2 = QtWidgets.QLabel()
        self.tower2.setStyleSheet("height: 200px; color: #00a0c0")
        self.tower2.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.tower3 = QtWidgets.QLabel()
        self.tower3.setStyleSheet("height: 200px; color: #00a0c0")
        self.tower3.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)

        self.labelMoves = QtWidgets.QLabel()
        self.labelMoves.setStyleSheet("height: 50px; font-size: 20px")
        self.buttonRestart = QtWidgets.QPushButton("Restart", self)
        self.buttonRestart.setStyleSheet("height: 50px; font-size: 20px; background-color: #806010")
        self.buttonRestart.clicked.connect(lambda: self.init_state(self.numStones))
        self.buttonQuit = QtWidgets.QPushButton("Quit", self)
        self.buttonQuit.setStyleSheet("height: 50px; font-size: 20px; background-color: #806010")
        self.buttonQuit.clicked.connect(self.quit)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.button1, 4, 1)
        layout.addWidget(self.button2, 4, 2)
        layout.addWidget(self.button3, 4, 3)
        layout.addWidget(self.hand, 6, 2)
        layout.addWidget(self.tower1, 8, 1)
        layout.addWidget(self.tower2, 8, 2)
        layout.addWidget(self.tower3, 8, 3)
        layout.addWidget(self.labelMoves, 10, 1)
        layout.addWidget(self.buttonRestart, 10, 2)
        layout.addWidget(self.buttonQuit, 10, 3)
        self.setLayout(layout)

    def pick(self, n):
        self.lastPick = n
        stack = self.stacks[n]
        self.hand.setText(self.stoneChar*stack.pop())
        self.draw_tower(n)
        for stk, btn in zip(self.stacks, [self.button1, self.button2, self.button3]):
            if stk == [] or stk[-1] > len(self.hand.text()):
                btn.setText(self.strDrop)
                btn.setEnabled(True)
            else:
                btn.setText("")
                btn.setEnabled(False)

    def drop(self, n):
        stack = self.stacks[n]
        stack.append(len(self.hand.text()))
        self.draw_tower(n)
        self.hand.setText("")
        for stk, btn in zip(self.stacks, [self.button1, self.button2, self.button3]):
            if stk:
                btn.setText(self.strPick)
                btn.setEnabled(True)
            else:
                btn.setText("")
                btn.setEnabled(False)
        if n != self.lastPick:    # returnig a stone to the same position won't count as a move
            self.numMoves += 1
            self.labelMoves.setText("Moves: " + str(self.numMoves))
        if n == 2 and stack == self.target:    # when dropping on tower 3 we will test if finished
            print("Solved in", self.numMoves, "moves.")
            self.button1.setText("\u2714")
            self.button2.setText("\u2714")
            self.button3.setText("\u2714")
            self.button3.setEnabled(False)

    def draw_tower(self, n):
        revStack = self.stacks[n][::-1]
        t = "\n".join([self.stoneChar*i for i in revStack])
        [self.tower1, self.tower2, self.tower3][n].setText(t)

    def run(self, app):
        self.show()
        app.exec_()

    def quit(self):
        print("Closing...")
        self.close()

def main():
    app = QtWidgets.QApplication()
    main_window().run(app)

if __name__ == "__main__":
    main()

#!/usr/bin/python
# coding: utf-8

import functools
from PySide2 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tower of Hanoi")
        self.resize(640, 400)

        self.numDisks = 3
        self.diskHeight = 16

        # Colors for "Natural"
        self.darkBrown = QtGui.QColor(0xff71481b)   # (0xff87551f)
        self.lightBrown = QtGui.QColor(0xffda9e5e)  # (0xffd59149)

        # Colors for backgrounds
        self.base03 = QtGui.QColor(0xff002b36)    # Solarized base03
        self.base02 = QtGui.QColor(0xff073642)              # base02
        self.base01 = QtGui.QColor(0xff586e75)              # base01
        self.base00 = QtGui.QColor(0xff657b83)              # base00
        # self.base0 = QtGui.QColor(0xff839496)               # base0
        self.base1 = QtGui.QColor(0xff93a1a1)               # base1
        # self.base2 = QtGui.QColor(0xffeee8d5)               # base2
        self.base3 = QtGui.QColor(0xfffdf6e3)               # base3

        # Colors for "Rainbow"
        self.yellow = QtGui.QColor(0xffb58900)              # yellow
        self.orange = QtGui.QColor(0xffcb4b16)              # orange
        self.red = QtGui.QColor(0xffdc322f)                 # red
        # self.magenta = QtGui.QColor(0xffd33682)             # magenta
        self.violet = QtGui.QColor(0xff6c71c4)              # violet
        self.blue = QtGui.QColor(0xff268bd2)                # blue
        self.cyan = QtGui.QColor(0xff2aa198)                # cyan
        self.green = QtGui.QColor(0xff859900)               # green

        # Colors for "Speccy"
        self.zx1 = QtGui.QColor(0xff0000b2)
        self.zx2 = QtGui.QColor(0xffb20000)
        self.zx3 = QtGui.QColor(0xffb200b2)
        self.zx4 = QtGui.QColor(0xff00b200)
        self.zx5 = QtGui.QColor(0xff00b2b2)
        self.zx6 = QtGui.QColor(0xffb2b200)
        self.zx7 = QtGui.QColor(0xffb2b2b2)
        self.diskOutline = self.base02

        menu = self.menuBar()
        menuGame = menu.addMenu("&Game")
        item_G_R = QtWidgets.QAction(QtGui.QIcon("icons/restart.png"),
                                     "&Restart", self)
        item_G_D = QtWidgets.QAction(QtGui.QIcon("icons/difficulty.png"),
                                     "&Difficulty setting...", self)
        item_G_Q = QtWidgets.QAction(QtGui.QIcon("icons/exit.png"),
                                     "&Quit", self)
        menuGame.addAction(item_G_R)
        menuGame.addAction(item_G_D)
        menuGame.addSeparator()
        menuGame.addAction(item_G_Q)
        item_G_R.triggered.connect(self.init_state)
        item_G_D.triggered.connect(self.difficulty_dialog)
        item_G_Q.triggered.connect(self.close)
        item_G_R.setShortcut("Ctrl+R")
        # alternatively: item_G_R.setShortcut(QtGui.QKeySequence("Ctrl+R"))
        item_G_D.setShortcut("Ctrl+D")
        item_G_Q.setShortcut("Ctrl+Q")
        item_G_R.setStatusTip("Restart with the same number of disks (Ctrl+R)")
        item_G_D.setStatusTip("Choose number of disks and restart (Ctrl+D)")
        item_G_Q.setStatusTip("Close the application")

        menuColors = menu.addMenu("&Colors")
        item_C_N = QtWidgets.QAction(QtGui.QIcon("icons/7disks.png"),
                                     "&Natural", self)
        item_C_R = QtWidgets.QAction(QtGui.QIcon("icons/solarized.png"),
                                     "&Rainbow", self)
        item_C_S = QtWidgets.QAction(QtGui.QIcon("icons/speccy.png"),
                                     "&Speccy", self)
        item_C_D = QtWidgets.QAction(QtGui.QIcon("icons/dark.png"),
                                     "&Dark background", self)
        item_C_L = QtWidgets.QAction(QtGui.QIcon("icons/light.png"),
                                     "&Light background", self)
        menuColors.addAction(item_C_N)
        menuColors.addAction(item_C_R)
        menuColors.addAction(item_C_S)
        menuColors.addSeparator()
        menuColors.addAction(item_C_D)
        menuColors.addAction(item_C_L)
        item_C_N.triggered.connect(lambda: self.set_colors("natural"))
        item_C_R.triggered.connect(lambda: self.set_colors("rainbow"))
        item_C_S.triggered.connect(lambda: self.set_colors("speccy"))
        item_C_D.triggered.connect(lambda: self.set_fg_bg(fg=self.base1,
                                                          bg=self.base03))
        item_C_L.triggered.connect(lambda: self.set_fg_bg(fg=self.base01,
                                                          bg=self.base3))
        item_C_N.setStatusTip("Shades of brown")
        item_C_R.setStatusTip("Rainbow")
        item_C_S.setStatusTip("ZX Spectrum")
        item_C_D.setStatusTip("Set a dark background")
        item_C_L.setStatusTip("Set a light background")

        menuHelp = menu.addMenu("&Help")
        item_H_H = QtWidgets.QAction("&How to play", self)
        item_H_A = QtWidgets.QAction("&About...", self)
        menuHelp.addAction(item_H_H)
        menuHelp.addAction(item_H_A)
        item_H_H.triggered.connect(self.help_message)
        item_H_A.triggered.connect(self.about_message)

        toolBar = self.addToolBar("Tools")
        toolBar.addAction(item_G_R)
        toolBar.addAction(item_G_D)
        toolBar.addSeparator()
        toolBar.addAction(item_C_N)
        toolBar.addAction(item_C_R)
        toolBar.addAction(item_C_S)
        toolBar.addSeparator()
        toolBar.addAction(item_C_D)
        toolBar.addAction(item_C_L)

        self.content = QtWidgets.QLabel()
        self.content.setAutoFillBackground(True)

        layout = QtWidgets.QGridLayout()
        self.content.pushButtons = []
        self.content.towers = []
        for i in range(3):
            button = QtWidgets.QPushButton()
            button.setFixedHeight(50)
            button.clicked.connect(functools.partial(self.pick_or_drop, i))
            layout.addWidget(button, 0, i)
            self.content.pushButtons.append(button)
            tower = QtWidgets.QLabel()
            layout.addWidget(tower, 2, i, 1, 1, QtCore.Qt.AlignCenter)
            self.content.towers.append(tower)

        self.content.hand = QtWidgets.QLabel()
        self.content.message = QtWidgets.QLabel()
        layout.addWidget(self.content.hand, 1, 0, 1, 3,
                         QtCore.Qt.AlignCenter)
        layout.addWidget(self.content.message, 3, 0, 1, 3,
                         QtCore.Qt.AlignCenter)
        self.content.setLayout(layout)
        self.setCentralWidget(self.content)
        self.color_setting = "rainbow"
        self.set_fg_bg(fg=self.base1, bg=self.base03)
        self.init_state()

    def init_state(self):
        self.numMoves = 0
        self.target = list(range(self.numDisks, 0, -1))
        self.stacks = [self.target[:], [], []]    # [:] for an independent copy
        self.hand = 0
        self.prepare_pushbuttons("pick")
        self.set_colors()
        self.content.message.setText("")
        self.statusBar().clearMessage()

    def pick(self, n):
        if self.stacks[n]:
            self.lastPick = n
            self.hand = self.stacks[n].pop()
            self.draw_tower(n)
            self.draw_hand()
            self.statusBar().clearMessage()
            self.prepare_pushbuttons("drop")

    def drop(self, n):
        if self.stacks[n] == [] or self.stacks[n][-1] > self.hand:
            stack = self.stacks[n]
            stack.append(self.hand)
            self.draw_tower(n)
            self.hand = 0
            self.draw_hand()
            self.statusBar().clearMessage()
            self.prepare_pushbuttons("pick")
            # returning a disk to the same position won't count as a move
            if n != self.lastPick:
                self.numMoves += 1
                self.content.message.setText("Moves: {}".format(self.numMoves))
            # when dropping on tower 2 or 3, test if we are finished
            if (n == 1 and stack == self.target) or \
               (n == 2 and stack == self.target):
                self.content.message.setText("Congratulations, puzzle solved "
                                             "in {} moves".
                                             format(self.numMoves))
                for btn in self.content.pushButtons:
                    btn.setIcon(QtGui.QIcon("icons/ok.png"))
                    btn.setEnabled(False)
                    btn.setStatusTip("")

    def pick_or_drop(self, n):
        if self.hand:
            self.drop(n)
        else:
            self.pick(n)

    def prepare_pushbuttons(self, for_what):
        for i in range(3):
            btn = self.content.pushButtons[i]
            key = "{}".format(i + 1)
            if for_what == "pick" and self.stacks[i]:
                btn.setIcon(QtGui.QIcon("icons/up.png"))
                btn.setEnabled(True)
                btn.setShortcut(key)
                btn.setStatusTip("Pick from the {} tower ({})"
                                 .format(["first", "second", "third"][i], key))
                btn.setShortcutAutoRepeat(False)   # not working
            elif for_what == "drop" and (self.stacks[i] == []
                                         or self.stacks[i][-1] > self.hand):
                btn.setIcon(QtGui.QIcon("icons/down.png"))
                btn.setEnabled(True)
                btn.setShortcut(key)
                btn.setStatusTip("Drop on the {} tower ({})"
                                 .format(["first", "second",
                                          "third"][i], key))
                btn.setShortcutAutoRepeat(False)   # not working
            else:
                btn.setIcon(QtGui.QIcon("icons/forbidden.png"))
                btn.setEnabled(False)
                btn.setStatusTip("")

    def draw_tower(self, n):
        stack = self.stacks[n]
        img = QtGui.QImage(200, 200, QtGui.QImage.Format_ARGB32)
        img.fill(self.content.backgroundRole())
        painter = QtGui.QPainter()
        painter.begin(img)
        painter.setPen(self.base00)
        painter.setBrush(self.base00)
        baseWidth = 180
        baseTop = 177
        rodWidth = 6
        rodTop = 40
        painter.drawRect((img.width() - baseWidth)//2, baseTop, baseWidth, 10)
        painter.drawRect((img.width() - rodWidth)//2,
                         rodTop, rodWidth, baseTop - rodTop)
        painter.setPen(self.diskOutline)
        for i, x in enumerate(stack):
            painter.setBrush(self.listColors[x - 1])
            diskWidth = 40 + 20*(x - 1)
            painter.drawRoundedRect((img.width() - diskWidth)//2,
                                    baseTop - 1 - (i+1)*self.diskHeight,
                                    diskWidth, self.diskHeight, 0, 0)
        painter.end()
        pixmap = QtGui.QPixmap.fromImage(img)
        self.content.towers[n].setPixmap(pixmap)

    def draw_hand(self):
        img = QtGui.QImage(400, 40, QtGui.QImage.Format_ARGB32)
        img.fill(self.content.backgroundRole())
        if self.hand:
            painter = QtGui.QPainter()
            painter.begin(img)
            painter.setPen(self.diskOutline)
            painter.setBrush(self.listColors[self.hand - 1])
            diskWidth = 40 + 20*(self.hand - 1)
            painter.drawRoundedRect((img.width() - diskWidth)//2,
                                    (img.height() - self.diskHeight)//2,
                                    diskWidth, self.diskHeight, 0, 0)
            painter.end()
        pixmap = QtGui.QPixmap.fromImage(img)
        self.content.hand.setPixmap(pixmap)

    def calculate_range(self, color1, color2, n):
        result = []
        for i in range(n):
            result.append(QtGui.QColor(color1.red() + i/n*(color2.red()
                                                           - color1.red()),
                                       color1.green() + i/n*(color2.green()
                                                             - color1.green()),
                                       color1.blue() + i/n*(color2.blue()
                                                            - color1.blue())))
        return result

    def set_colors(self, setting=None):
        if setting:
            self.color_setting = setting
        else:
            setting = self.color_setting
        if setting == "natural":
            self.listColors = self.calculate_range(self.darkBrown,
                                                   self.lightBrown,
                                                   self.numDisks)
        elif setting == "rainbow":
            self.listColors = [self.red, self.orange, self.yellow, self.green,
                               self.cyan, self.blue, self.violet]
        elif setting == "speccy":
            self.listColors = [self.zx7, self.zx6, self.zx5, self.zx4,
                               self.zx3, self.zx2, self.zx1]
        for i in range(3):
            self.draw_tower(i)
        self.draw_hand()

    def set_fg_bg(self, fg=None, bg=None):
        tempPal = self.content.palette()
        if fg:
            tempPal.setColor(tempPal.WindowText, fg)
        if bg:
            tempPal.setColor(tempPal.Window, bg)
        self.content.setPalette(tempPal)

    def difficulty_dialog(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("Difficulty setting")
        self.dialog.resize(320, 200)
        rbuttonGroup = QtWidgets.QButtonGroup()
        layout = QtWidgets.QGridLayout()
        for i in range(3, 8):
            rbutton = QtWidgets.QRadioButton("{} disks".format(i))
            rbutton.setIcon(QtGui.QIcon("icons/{}disks.png".format(i)))
            rbutton.setIconSize(QtCore.QSize(48, 48))
            rbuttonGroup.addButton(rbutton, id=i)
            layout.addWidget(rbutton, (i - 3)//2, 1 - i % 2)
        rbuttonGroup.button(self.numDisks).setChecked(True)
        buttonOK = QtWidgets.QPushButton("OK")
        buttonCancel = QtWidgets.QPushButton("Cancel")
        buttonOK.clicked.connect(self.dialog.accept)
        buttonCancel.clicked.connect(self.dialog.reject)
        self.dialog.accepted.connect(lambda: self
                                     .set_difficulty(rbuttonGroup.checkedId()))
        layout.addWidget(buttonOK, 3, 0)
        layout.addWidget(buttonCancel, 3, 1)
        self.dialog.setLayout(layout)
        self.dialog.show()

    def set_difficulty(self, n):
        self.numDisks = n
        self.init_state()

    def help_message(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("How to play")
        msg.setIconPixmap(QtGui.QPixmap("icons/5disks_color.png"))
        msg.setText("""<center><p>To pick or drop disks, click on corresponding
buttons or use keys 1, 2 and 3.</p>
<p>The goal of the game is to move the entire stack to another rod, obeying the
following simple rules:</p>
<ul><li>only one disk can be moved at a time</li>
<li>each move consists of taking the upper disk from one of the stacks and
placing it on top of another stack or on an empty rod</li>
<li>no disk may be placed on top of a smaller disk</li></ul>
<p>Source: <a href="https://en.wikipedia.org/wiki/Tower_of_Hanoi">Wikipedia</a>
</p></center>""")
        msg.exec_()

    def about_message(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("About Tower of Hanoi")
        msg.setIconPixmap(QtGui.QPixmap("icons/5disks.png"))
        msg.setText("""<center><b>Tower of Hanoi</b><p>version 0.9.6,
3rd February 2019</p><p>
<a href="https://github.com/myrmica-habilis/tower-of-hanoi">GitHub page</a>
</p></center>""")
        msg.exec_()

    def run(self, app):
        self.show()
        app.exec_()


def main():
    app = QtWidgets.QApplication()
    MainWindow().run(app)


if __name__ == "__main__":
    main()

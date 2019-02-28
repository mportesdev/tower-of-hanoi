#!/usr/bin/python
# coding: utf-8

from PySide2 import QtWidgets, QtCore, QtGui
import utils
import colors


class Tower:
    """Custom class for a single tower.
    """

    def __init__(self, parent_app, name, key):
        self.app = parent_app
        self.name = name
        self.key = key
        self.stack = []

        self.widget = QtWidgets.QLabel()
        self.pushbutton = QtWidgets.QPushButton()
        self.pushbutton.setFixedHeight(50)
        self.pushbutton.clicked.connect(self.pick_or_drop)

    def pick_or_drop(self):
        if self.app.hand:
            self.drop()
        else:
            self.pick()

    def pick(self):
        if self.stack:
            disk_value = self.stack.pop()
            self.redraw()
            self.app.pick(self.name, disk_value)

    def drop(self):
        if self.stack == [] or self.stack[-1] > self.app.hand:
            self.stack.append(self.app.hand)
            self.redraw()
            self.app.drop(self.name, self.stack)

    def prepare_pushbutton(self, hand):
        # hand is empty, prepare button for picking if possible
        if hand == 0 and self.stack:
            self.pushbutton.setIcon(QtGui.QIcon("icons/up.png"))
            self.pushbutton.setEnabled(True)
            self.pushbutton.setShortcut(self.key)
            self.pushbutton.setStatusTip("Pick from the {} tower ({})"
                                         .format(self.name, self.key))
            self.pushbutton.setShortcutAutoRepeat(False)   # not working

        # hand is not empty, prepare button for dropping if possible
        elif hand and (self.stack == [] or self.stack[-1] > hand):
            self.pushbutton.setIcon(QtGui.QIcon("icons/down.png"))
            self.pushbutton.setEnabled(True)
            self.pushbutton.setShortcut(self.key)
            self.pushbutton.setStatusTip("Drop on the {} tower ({})"
                                         .format(self.name, self.key))
            self.pushbutton.setShortcutAutoRepeat(False)   # not working

        # otherwise deactivate button
        else:
            self.pushbutton.setIcon(QtGui.QIcon("icons/forbidden.png"))
            self.pushbutton.setEnabled(False)
            self.pushbutton.setStatusTip("")

    def redraw(self):
        disk_height = 16
        base_width = 180
        base_top = 177
        rod_width = 6
        rod_top = 40

        img = QtGui.QImage(200, 200, QtGui.QImage.Format_ARGB32)
        img.fill(self.app.content.backgroundRole())

        painter = QtGui.QPainter()
        painter.begin(img)

        # draw base & rod
        painter.setPen(colors.ROD)
        painter.setBrush(QtGui.QBrush(colors.ROD))

        painter.drawRect((img.width() - base_width) // 2, base_top,
                         base_width, 10)
        painter.drawRect((img.width() - rod_width) // 2, rod_top,
                         rod_width, base_top - rod_top)

        # draw disks
        painter.setPen(colors.OUTLINE)

        for i, x in enumerate(self.stack):
            painter.setBrush(QtGui.QBrush(self.app.color_list[x - 1]))
            disk_width = 20 + 20 * x
            painter.drawRoundedRect((img.width() - disk_width) // 2,
                                    base_top - 1 - (i + 1) * disk_height,
                                    disk_width, disk_height, 3, 3)

        painter.end()
        pixmap = QtGui.QPixmap.fromImage(img)
        self.widget.setPixmap(pixmap)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tower of Hanoi")
        self.resize(QtCore.QSize(640, 480))

        self.num_disks = 3

        menu = self.menuBar()
        menu_Game = menu.addMenu("&Game")
        item_G_R = QtWidgets.QAction(QtGui.QIcon("icons/restart.png"),
                                     "&Restart", self)
        item_G_D = QtWidgets.QAction(QtGui.QIcon("icons/difficulty.png"),
                                     "&Difficulty setting...", self)
        item_G_Q = QtWidgets.QAction(QtGui.QIcon("icons/exit.png"),
                                     "&Quit", self)
        menu_Game.addAction(item_G_R)
        menu_Game.addAction(item_G_D)
        menu_Game.addSeparator()
        menu_Game.addAction(item_G_Q)
        item_G_R.triggered.connect(self.init_state)
        item_G_D.triggered.connect(self.difficulty_dialog)
        item_G_Q.triggered.connect(self.close)
        item_G_R.setShortcut("Ctrl+R")
        item_G_D.setShortcut("Ctrl+D")
        item_G_Q.setShortcut("Ctrl+Q")
        item_G_R.setStatusTip("Restart with the same number of disks (Ctrl+R)")
        item_G_D.setStatusTip("Choose number of disks and restart (Ctrl+D)")
        item_G_Q.setStatusTip("Close the application")

        menu_Colors = menu.addMenu("&Colors")
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
        menu_Colors.addAction(item_C_N)
        menu_Colors.addAction(item_C_R)
        menu_Colors.addAction(item_C_S)
        menu_Colors.addSeparator()
        menu_Colors.addAction(item_C_D)
        menu_Colors.addAction(item_C_L)
        item_C_N.triggered.connect(lambda: self.set_colors("natural"))
        item_C_R.triggered.connect(lambda: self.set_colors("rainbow"))
        item_C_S.triggered.connect(lambda: self.set_colors("speccy"))
        item_C_D.triggered.connect(lambda: self.set_fg_bg(fg=colors.LIGHT_FG,
                                                          bg=colors.DARK_BG))
        item_C_L.triggered.connect(lambda: self.set_fg_bg(fg=colors.DARK_FG,
                                                          bg=colors.LIGHT_BG))
        item_C_N.setStatusTip("Shades of brown")
        item_C_R.setStatusTip("Rainbow")
        item_C_S.setStatusTip("ZX Spectrum")
        item_C_D.setStatusTip("Set a dark background")
        item_C_L.setStatusTip("Set a light background")

        menu_Help = menu.addMenu("&Help")
        item_H_H = QtWidgets.QAction("&How to play", self)
        item_H_A = QtWidgets.QAction("&About...", self)
        menu_Help.addAction(item_H_H)
        menu_Help.addAction(item_H_A)
        item_H_H.triggered.connect(self.help_message)
        item_H_A.triggered.connect(self.about_message)

        tool_bar = self.addToolBar("Tools")
        tool_bar.addAction(item_G_R)
        tool_bar.addAction(item_G_D)
        tool_bar.addSeparator()
        tool_bar.addAction(item_C_N)
        tool_bar.addAction(item_C_R)
        tool_bar.addAction(item_C_S)
        tool_bar.addSeparator()
        tool_bar.addAction(item_C_D)
        tool_bar.addAction(item_C_L)

        self.content = QtWidgets.QLabel()
        self.content.setAutoFillBackground(True)

        layout = QtWidgets.QGridLayout()
        self.towers = []

        for i, args in enumerate((("left", "1"), ("middle", "2"),
                                  ("right", "3"))):
            tower = Tower(self, *args)
            self.towers.append(tower)
            layout.addWidget(tower.pushbutton, 0, i)
            layout.addWidget(tower.widget, 2, i, 1, 1,
                             QtCore.Qt.AlignCenter)

        self.content.hand = QtWidgets.QLabel()
        layout.addWidget(self.content.hand, 1, 0, 1, 3,
                         QtCore.Qt.AlignCenter)

        self.content.message = QtWidgets.QLabel()
        layout.addWidget(self.content.message, 3, 0, 1, 3,
                         QtCore.Qt.AlignCenter)

        self.content.setLayout(layout)
        self.setCentralWidget(self.content)
        self.color_setting = "rainbow"
        self.set_fg_bg(fg=colors.LIGHT_FG, bg=colors.DARK_BG)
        self.init_state()

    def init_state(self):
        self.num_moves = 0
        self.hand = 0
        self.target = list(range(self.num_disks, 0, -1))
        for tower, stack in zip(self.towers, (self.target[:], [], [])):
            tower.stack = stack
            tower.prepare_pushbutton(self.hand)
        self.set_colors()
        self.content.message.setText("")
        self.statusBar().clearMessage()

    def pick(self, tower_name, disk_value):
        self.last_pick = tower_name
        self.hand = disk_value
        self.draw_hand()
        for tower in self.towers:
            tower.prepare_pushbutton(self.hand)
        self.statusBar().clearMessage()

    def drop(self, tower_name, stack):
        self.hand = 0
        self.draw_hand()
        for tower in self.towers:
            tower.prepare_pushbutton(self.hand)
        self.statusBar().clearMessage()

        # returning a disk to the same position won't count as a move
        if tower_name != self.last_pick:
            self.num_moves += 1
            self.content.message.setText("Moves: {}"
                                         .format(self.num_moves))

        # when dropping on tower 2 or 3, test if we are finished
        if stack == self.target and tower_name != "left":
            self.content.message.setText("Congratulations, puzzle"
                                         " solved in {} moves"
                                         .format(self.num_moves))
            for tower in self.towers:
                tower.pushbutton.setIcon(QtGui.QIcon("icons/ok.png"))
                tower.pushbutton.setEnabled(False)
                tower.pushbutton.setStatusTip("")

    def draw_hand(self):
        disk_height = 16

        img = QtGui.QImage(400, 40, QtGui.QImage.Format_ARGB32)
        img.fill(self.content.backgroundRole())
        if self.hand:
            painter = QtGui.QPainter()
            painter.begin(img)
            painter.setPen(colors.OUTLINE)
            painter.setBrush(QtGui.QBrush(self.color_list[self.hand - 1]))
            disk_width = 20 + 20 * self.hand
            painter.drawRoundedRect((img.width() - disk_width) // 2,
                                    (img.height() - disk_height) // 2,
                                    disk_width, disk_height, 3, 3)
            painter.end()
        pixmap = QtGui.QPixmap.fromImage(img)
        self.content.hand.setPixmap(pixmap)

    def set_colors(self, setting=None):
        if setting:
            self.color_setting = setting
        else:
            setting = self.color_setting

        if setting == "natural":
            # calculate scales of color components
            reds = utils.even_steps(colors.DARK_BROWN["R"],
                                    colors.LIGHT_BROWN["R"], self.num_disks)
            greens = utils.even_steps(colors.DARK_BROWN["G"],
                                      colors.LIGHT_BROWN["G"], self.num_disks)
            blues = utils.even_steps(colors.DARK_BROWN["B"],
                                     colors.LIGHT_BROWN["B"], self.num_disks)

            # generate colors from components
            self.color_list = [QtGui.QColor(r, g, b, 255)
                               for r, g, b in zip(reds, greens, blues)]

        elif setting == "rainbow":
            self.color_list = [colors.RED, colors.ORANGE, colors.YELLOW,
                               colors.GREEN, colors.CYAN, colors.BLUE,
                               colors.VIOLET]

        elif setting == "speccy":
            self.color_list = [colors.SPECCY_WHITE, colors.SPECCY_YELLOW,
                               colors.SPECCY_CYAN, colors.SPECCY_GREEN,
                               colors.SPECCY_MAGENTA, colors.SPECCY_RED,
                               colors.SPECCY_BLUE]

        for tower in self.towers:
            tower.redraw()
        self.draw_hand()

    def set_fg_bg(self, fg=None, bg=None):
        temp_pal = self.content.palette()
        if fg:
            temp_pal.setColor(temp_pal.WindowText, fg)
        if bg:
            temp_pal.setColor(temp_pal.Window, bg)
        self.content.setPalette(temp_pal)

    def difficulty_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Difficulty setting")
        dialog.resize(320, 200)
        rbutton_group = QtWidgets.QButtonGroup()
        layout = QtWidgets.QGridLayout()

        for i in range(3, 8):
            rbutton = QtWidgets.QRadioButton("{} disks".format(i))
            rbutton.setIcon(QtGui.QIcon("icons/{}disks.png".format(i)))
            rbutton.setIconSize(QtCore.QSize(48, 48))
            rbutton_group.addButton(rbutton, id=i)
            layout.addWidget(rbutton, (i - 3) // 2, 1 - i % 2)

        rbutton_group.button(self.num_disks).setChecked(True)
        button_OK = QtWidgets.QPushButton("OK")
        button_Cancel = QtWidgets.QPushButton("Cancel")
        button_OK.clicked.connect(dialog.accept)
        button_Cancel.clicked.connect(dialog.reject)
        dialog.accepted.connect(lambda: self.set_difficulty(rbutton_group
                                                            .checkedId()))
        layout.addWidget(button_OK, 3, 0)
        layout.addWidget(button_Cancel, 3, 1)
        dialog.setLayout(layout)
        dialog.exec_()

    def set_difficulty(self, n):
        self.num_disks = n
        self.init_state()

    def help_message(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("How to play")
        msg.setIconPixmap(QtGui.QPixmap("icons/5disks_color.png"))
        msg.setText("""<center><p>To pick or drop disks, click on corresponding
pushbuttons or use keys 1, 2 and 3.</p>
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

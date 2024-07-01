# coding:utf-8
import json
import sys

# import qdarktheme
from PySide6.QtCore import Qt, Signal, QEasingCurve, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QFrame
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, MessageBox,
                            isDarkTheme, setTheme, Theme,
                            PopUpAniStackedWidget, setThemeColor)
from qframelesswindow import FramelessWindow, TitleBar

import Expenses
import Incomes


APP_NAME = "Cashflow"

with open("resource/Data/config.json", "r") as themes_file:
    _themes = json.load(themes_file)

#theme_color = _themes["theme"]
#progressive = _themes["progressive"]


class StackedWidget(QFrame):
    """ Stacked widget """

    currentChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=False):
        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.Type.InQuad)

    def setCurrentIndex(self, index, popOut=False):
        self.setCurrentWidget(self.view.widget(index), popOut)


class CustomTitleBar(TitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(18, 18)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(
            1, self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(
            2, self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.titleLabel.setObjectName('titleLabel')
        self.window().windowTitleChanged.connect(self.setTitle)

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(QIcon(icon).pixmap(18, 18))


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        # use dark theme mode
        setTheme(Theme.DARK)

        # change the theme color
        # setThemeColor(theme_color)

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationBar = NavigationInterface(self)
        self.stackWidget = StackedWidget(self)

        # create sub interface
        self.expenseInterface = Expenses.Expenses()
        self.incomeInterface = Incomes.Incomes()
        #self.settingsInterface = settings.SettingsPage()

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.hBoxLayout.addWidget(self.navigationBar)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.addSubInterface(self.expenseInterface, QIcon("resource/Icons/expense.png"), 'Expenses', selectedIcon=QIcon("resource/Icons/expense.png"))
        self.addSubInterface(self.incomeInterface, QIcon("resource/Icons/income.png"), 'Incomes', selectedIcon=QIcon("resource/Icons/income.png"))

       # self.addSubInterface(self.settingsInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM,
       #                      FIF.SETTING)
        self.navigationBar.addItem(
            routeKey='About',
            icon=FIF.HELP,
            text='About',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.navigationBar.setCurrentItem(self.expenseInterface.objectName())

    def initWindow(self):
        self.resize(1000, 600)
        self.setWindowIcon(QIcon('resources/icons/icon.png'))
        self.setWindowTitle('Cashflow')
        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP, selectedIcon=None):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationBar.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/{color}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationBar.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        text_for_about = f"Heya! it's Rohan, the creator of {APP_NAME}. I hope you've enjoyed using this app as much as I enjoyed making it." + "" + "\n" + "\n" \
                                                                                                                                                            "I'm a school student and I can't earn my own money LEGALLY. So any donations will be largely appreciated. Also, if you find any bugs / have any feature requests, you can open a Issue/ Pull Request in the Repo." \
                                                                                                                                                            "You can visit GitHub by pressing the button below. You can find Ko-Fi link there :) " + "\n" + "\n" + \
                         f"Once again, thank you for using {APP_NAME}. Please consider giving it a star ⭐ as it will largely motivate me to create more of such apps. Also do consider giving me a follow ;) "
        w = MessageBox(
            APP_NAME,
            text_for_about,
            self
        )
        w.yesButton.setText('GitHub')
        w.cancelButton.setText('Return')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://github.com/rohankishore/Cashflow"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    #qdarktheme.enable_hi_dpi()
    w = Window()
    #qdarktheme.setup_theme("dark", custom_colors={"primary": theme_color})
    w.show()
    sys.exit(app.exec())

import sys

import qdarktheme
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, Qt, QAction
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout,
                               QWidget, QTabWidget, QSizePolicy)

import Expenses, Incomes, Investments


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CashFlow')

        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # Menu Bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Import')

        exit_action = QAction('Expenses', self)
        exit_action.triggered.connect(self.import_expenses)
        file_menu.addAction(exit_action)

        self.exp_widget = Expenses.Expenses()

        self.btn_1 = QPushButton(self)
        self.btn_2 = QPushButton(self)
        self.btn_3 = QPushButton(self)

        expense_icon = QIcon('expense.png')
        self.btn_1.setIcon(expense_icon)
        self.btn_1.setStyleSheet("QPushButton { align: right; }")
        self.btn_1.setIconSize(QSize(50, 50))
        self.btn_1.setFixedSize(50, 50)
        self.btn_1.setStyleSheet("border: none;")

        income_icon = QIcon('income.png')
        self.btn_2.setIcon(income_icon)
        self.btn_2.setStyleSheet("QPushButton { align: center; }")
        self.btn_2.setIconSize(QSize(55, 55))
        self.btn_2.setFixedSize(55, 55)
        self.btn_2.setStyleSheet("border: none;")

        investment_icon = QIcon('investment.png')
        self.btn_3.setIcon(investment_icon)
        self.btn_3.setStyleSheet(
            """
            QPushButton {
                align: left;
            }
            QPushButton:hover {
                background-color: #4e5157;
            }
            """
        )
        self.btn_3.setIconSize(QSize(50, 50))
        self.btn_3.setFixedSize(50, 50)
        self.btn_3.setStyleSheet("border: none;")

        self.linebreak_widget = QWidget()
        self.linebreak_widget.setFixedHeight(20)  # Adjust the height as needed

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)

        self.btn_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.tab1 = self.expenses(self)
        self.tab2 = self.incomes(self)
        self.tab3 = self.investments(self)
        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setFixedWidth(1)
        #left_widget.setLayout(left_layout)
        left_layout.addWidget(left_widget)

        left_layout.addWidget(self.btn_1)
        l1 = QLabel("Expenses")
        l1.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(l1)
        left_layout.addWidget(self.linebreak_widget)
        left_layout.addWidget(self.btn_2)
        l2 = QLabel("Incomes")
        l2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        left_layout.addWidget(l2)
        left_layout.addWidget(self.linebreak_widget)
        left_layout.addWidget(self.btn_3)
        l3 = QLabel("Investments")
        left_layout.addWidget(l3)
        left_layout.addStretch(1)
        left_layout.setSpacing(2)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none; background-color: 191919;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
        main_widget = QWidget()
        # main_widget.setStyleSheet("background-color: #000000; color: white; border: none;")
        main_widget.setStyleSheet(
            ("*{color: qlineargradient(spread: pad, x1: 0 y1: 0, x2: 1 y2: 0, stop:0 rgba(0, 0, 0, 255), "
             "stop:1 rgba(255, 255, 255, 255)); "
             "background: qlineargradient( x1:0 y1:0, x2:1 y2:0, stop:0 #191b1f, "
             "stop:1 #191b1f, stop:2 #282c2f); color: white; border: none}"))

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def import_expenses(self):
        Expenses.Expenses.import_(self.exp_widget)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    @staticmethod
    def expenses(self):
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.exp_widget)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    @staticmethod
    def incomes(self):
        main_layout = QVBoxLayout()
        inc_widget = Incomes.Incomes()
        main_layout.addWidget(inc_widget)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    @staticmethod
    def investments(self):
        main_layout = QVBoxLayout()
        inv_widget = Investments.Investments()
        main_layout.addWidget(inv_widget)
        main = QWidget()
        main.setLayout(main_layout)
        return main


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("dark")
    ex = Window()
    ex.showMaximized()
    ex.show()
    sys.exit(app.exec())

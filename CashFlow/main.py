import json
import sys

import qdarktheme
# import qdarktheme
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, Qt, QAction
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout,
                               QWidget, QTabWidget, QSizePolicy, QDockWidget, QComboBox, QLineEdit, QMessageBox,
                               QCheckBox)
from qt_material import apply_stylesheet
import Expenses
import Incomes
import Investments

with open("config.json", "r") as themes_file:
    _themes = json.load(themes_file)


class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()

        self.json_data = {"editor_theme": "", "margin_theme": "", "lines_theme": ""}

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addStretch()
        # layout.addSpacing(100)

        theme_label1 = QLabel("Theme :")
        theme_label2 = QLabel("Theming :")
        self.theme_combobox = QComboBox()
        # self.theme_combobox.setCurrentText(self._window._themes["font"])
        theme_opt = ['dark_amber',
                     'dark_blue',
                     'dark_cyan',
                     'dark_lightgreen',
                     'dark_pink',
                     'dark_purple',
                     'dark_red',
                     'dark_teal',
                     'dark_yellow',
                     'light_amber',
                     'light_blue',
                     'light_cyan',
                     'light_cyan_500',
                     'light_lightgreen',
                     'light_pink',
                     'light_purple',
                     'light_red',
                     'light_teal',
                     'light_yellow']
        self.theme_combobox.addItems(theme_opt)

        self.theming_combobox = QComboBox()
        # self.theme_combobox.setCurrentText(self._window._themes["font"])
        theming_opt = ['Material (Default)', 'Flat Dark (compatibility issues on Python >=3.11)']
        self.theming_combobox.addItems(theming_opt)

        # current_font_theme = self._window._themes.get("font", "")
        self.theming_combobox.setCurrentText(_themes["theming"])
        layout.addWidget(theme_label1)
        layout.addWidget(self.theme_combobox)
        layout.addWidget(theme_label2)
        layout.addWidget(self.theming_combobox)

        self.invert_secondary = QCheckBox("Invert Secondary (For Light Mode): ")
        if _themes["invert"] == "true":
            self.invert_secondary.setChecked(True)
        else:
            pass
        layout.addWidget(self.invert_secondary)

        # Save Button
        save_button = QPushButton("Apply")
        save_button.setStyleSheet(
            "QPushButton {"
            "   border-radius: 10px;"
            "   padding: 5px;"
            "background-color: #121212;"
            "color: white;"
            "}"
        )
        save_button.clicked.connect(self.save_json)
        layout.addWidget(save_button)

        self.setLayout(layout)
        self.setWindowTitle("Settings")

    def save_json(self):
        _themes["theme_type"] = self.theme_combobox.currentText()
        if self.invert_secondary.isChecked():
            _themes["invert"] = "true"
        else:
            _themes["invert"] = "false"
        _themes["theming"] = self.theming_combobox.currentText()

        with open("config.json", "w") as json_file:
            json.dump(_themes, json_file)

        QMessageBox.information(
            self,
            "Settings Applied!",
            "The chosen settings have been applied. Restart Aura Text to see the changes.",
        )


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

        expense_action = QAction('Expenses', self)
        expense_action.triggered.connect(self.import_expenses)
        file_menu.addAction(expense_action)

        config_action = QAction('Preferences', self)
        config_action.triggered.connect(self.preferences)
        menubar.addAction(config_action)

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
        # left_widget.setLayout(left_layout)
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

    def preferences(self):
        config_dock = QDockWidget("Preferences", self)
        config_dock.setMinimumWidth(200)

        self.settings_widget = ConfigPage()
        self.settings_layout = QVBoxLayout(self.settings_widget)
        self.settings_layout.addWidget(self.settings_widget)
        config_dock.setWidget(self.settings_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, config_dock)

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


extra = {
    # Button colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',
    # Font
    'font_family': 'Consolas',
}

inversion = False
if _themes["invert"] == "true":
    inversion = True
else:
    inversion = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    theme = (_themes["theme_type"] + ".xml")
    theming = _themes["theming"]
    if theming == "Flat Dark (compatibility issues on Python >=3.11)":
        qdarktheme.setup_theme("dark")
    elif theming == "Material (Default)":
        apply_stylesheet(app, theme=theme, extra=extra, invert_secondary=inversion)
    ex = Window()
    ex.showMaximized()
    ex.show()
    sys.exit(app.exec())

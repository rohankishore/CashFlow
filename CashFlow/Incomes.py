import sqlite3

from PySide6 import QtCore
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import (QHeaderView, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout,
                               QWidget, QDateEdit, QComboBox)
from PySide6.QtCharts import QChartView, QPieSeries, QChart
from tkinter import messagebox

class Incomes(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.items = 0

        INCOMES_DATABASE_FILE = "incomes.db"

        self.connection = sqlite3.connect(INCOMES_DATABASE_FILE)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                description TEXT,
                price REAL,
                payment_mode TEXT,
                date TEXT)"""
        )

        self.connection.commit()

        # Left Widget
        self.table = QTableWidget()
        self.table.setStyleSheet(
            "* {background: qlineargradient(x1:0 y1:0, x2:1 y2:0, stop:0 #181a1e, stop:1 #282c2f); color: white;}"
            "QHeaderView::section {color: #C1D7F0; background-color: #191b1f; border: none}"  # Change the heading text color to red
        )
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Description", "Price", "Payment Mode", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Chart
        self.chart_view = QChartView()
        self.table.setStyleSheet(
            "* {background: qlineargradient(x1:0 y1:0, x2:1 y2:0, stop:0 #181a1e, stop:1 #282c2f); color: white;}"
            "QHeaderView::section {color: #C1D7F0; background-color: #191b1f; border: none}"
            # Change the heading text color to red
        )

        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # Right Widget
        self.description = QLineEdit()
        self.price = QLineEdit()
        self.payment_mode = QComboBox()
        self.date_picker = QDateEdit()

        self.description = QLineEdit()
        self.description.setStyleSheet(
            "QLineEdit {"
            "   border-radius: 10px;"
            "   padding: 5px;"
            "background-color: #282c2f;"
            "}"
        )
        self.price = QLineEdit()
        self.price.setStyleSheet(
            "QLineEdit {"
            "   border-radius: 10px;"
            "   padding: 5px;"
            "background-color: #282c2f;"
            "}"
        )

        self.payment_mode = QComboBox()
        self.payment_mode.setStyleSheet(
            "QComboBox {"
            "   border-radius: 10px;"
            "   padding: 5px;"
            "background-color: #282c2f;"
            "}"
        )

        self.sortby = QComboBox()
        self.sortby.setStyleSheet(
            "QComboBox {"
            "   border-radius: 10px;"
            "   padding: 5px;"
            "background-color: #282c2f;"
            "}"
        )
        self.sortby.addItem("Date")
        self.sortby.addItem("Price (Low to High)")
        self.sortby.addItem("Price (High to Low)")

        self.date_picker = QDateEdit()
        self.date_picker.setStyleSheet(
            "QDateEdit {"
            "   border-radius: 10px;"
            "   padding: 5px;"
            "background-color: #282c2f;"
            "}"
        )

        self.linebreak_widget = QWidget()
        self.linebreak_widget.setFixedHeight(11)

        self.payment_mode.addItem("Cash")
        self.payment_mode.addItem("Paytm")
        self.payment_mode.addItem("Google Pay")
        self.payment_mode.addItem("Apple Pay")
        self.payment_mode.addItem("Amazon Pay")
        self.payment_mode.addItem("PayPal")
        self.payment_mode.addItem("Bank Transfer")
        self.payment_mode.addItem("Payoneer")

        self.add = QPushButton("Add")
        self.add.setStyleSheet(
            "QPushButton {"
            "   border-radius: 10px;"
            "   padding: 5px;"
            "background-color: #282c2f;"
            "}"
        )


        # Disabling 'Add' button
        self.add.setEnabled(False)

        self.right = QVBoxLayout()
        self.right.addWidget(QLabel("Sort By:"))
        self.right.addWidget(self.sortby)
        self.right.addWidget(self.linebreak_widget)
        self.right.addWidget(QLabel("Income Source"))
        self.right.addWidget(self.description)
        self.right.addWidget(QLabel("Amount"))
        self.right.addWidget(self.price)
        self.right.addWidget(QLabel("Payment Mode"))
        self.right.addWidget(self.payment_mode)
        self.right.addWidget(QLabel("Date of Recieval"))
        self.right.addWidget(self.date_picker)
        self.right.addWidget(self.add)
        self.right.addWidget(self.chart_view)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.right)

        self.setLayout(self.layout)

        self.add.clicked.connect(self.add_element)
        self.description.textChanged[str].connect(self.check_disable)
        self.price.textChanged[str].connect(self.check_disable)
        self.payment_mode.currentTextChanged[str].connect(self.check_disable)

        self.fill_table()
        self.plot_data()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Delete:
            self.clear_element()
        else:
            super().keyPressEvent(event)

    @Slot()
    def add_element(self):
        des = self.description.text()
        price = self.price.text()
        mode = self.payment_mode.currentText()
        date = self.date_picker.date().toString(Qt.ISODate)

        try:
            price = float(price)

            self.cursor.execute(
                """INSERT INTO expenses (description, price, payment_mode, date) VALUES (?, ?, ?, ?)""",
                (des, price, mode, date),
            )
            self.connection.commit()

            description_item = QTableWidgetItem(des)
            price_item = QTableWidgetItem(f"{price:.2f}")
            payment_mode_item = QTableWidgetItem(mode)
            date_item = QTableWidgetItem(date)

            description_item.setTextAlignment(Qt.AlignCenter)
            price_item.setTextAlignment(Qt.AlignCenter)
            payment_mode_item.setTextAlignment(Qt.AlignCenter)
            date_item.setTextAlignment(Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, description_item)
            self.table.setItem(self.items, 1, price_item)
            self.table.setItem(self.items, 2, payment_mode_item)
            self.table.setItem(self.items, 3, date_item)

            self.description.setText("")
            self.price.setText("")
            self.items += 1
            self.plot_data()
        except ValueError:
            messagebox.showerror("Invalid Amount!", "Invalid Amount:", price, "Make sure to enter a valid amount!")
    @Slot()
    def check_disable(self, x):
        if not self.description.text() or not self.price.text() or not self.payment_mode.currentText():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)

    @Slot()
    def plot_data(self):
        series = QPieSeries()

        for i in range(self.table.rowCount()):
            is_income_item = self.table.item(i, 3)
            is_income = is_income_item.text() == "Yes"

            if not is_income:
                text = self.table.item(i, 0).text()
                number = float(self.table.item(i, 1).text())
                series.append(text, number)

        chart = QChart()
        chart.setBackgroundBrush(QBrush(QColor("#191b1f")))
        legend = chart.legend()
        legend.setBrush(QBrush(QColor("#FFFFFF")))
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)

    def fill_table(self):
        self.cursor.execute("""SELECT * FROM expenses""")
        expenses = self.cursor.fetchall()

        for desc, price, mode, date, is_income in expenses:
            description_item = QTableWidgetItem(desc)
            price_item = QTableWidgetItem(f"{price:.2f}")
            payment_mode_item = QTableWidgetItem(mode)

            #payment_mode_item = QTableWidgetItem(mode)
            date_item = QTableWidgetItem(date)

            description_item.setTextAlignment(Qt.AlignCenter)
            price_item.setTextAlignment(Qt.AlignCenter)
            payment_mode_item.setTextAlignment(Qt.AlignCenter)
            date_item.setTextAlignment(Qt.AlignCenter)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, description_item)
            self.table.setItem(self.items, 1, price_item)
            self.table.setItem(self.items, 2, payment_mode_item)
            self.table.setItem(self.items, 3, date_item)

            self.items += 1

    @Slot()
    def clear_element(self):
        selected_rows = [index.row() for index in self.table.selectedIndexes()]
        for row in selected_rows:
            description_item = self.table.item(row, 0)
            price_item = self.table.item(row, 1)
            payment_mode_item = self.table.item(row, 2)
            is_income_item = self.table.item(row, 3)

            description = description_item.text()
            price = float(price_item.text())
            payment_mode = payment_mode_item.text()
            is_income = is_income_item.text() == "Yes"

            # Remove the expense from the SQLite table
            if is_income:
                table_name = "incomes"
            else:
                table_name = "expenses"

            self.cursor.execute(
                f"DELETE FROM {table_name} WHERE description = ? AND price = ? AND payment_mode = ?",
                (description, price, payment_mode),
            )
            self.connection.commit()
            self.table.removeRow(row)
            self.plot_data()

    @Slot()
    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0

import csv
import sqlite3
import os

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import (QHeaderView, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QVBoxLayout,
                             QWidget, QDateEdit, QComboBox, QDockWidget, QFileDialog, QMessageBox)
from PySide6.QtCharts import QChartView, QPieSeries, QChart, QLineSeries
from tkinter import messagebox


class Expenses(QWidget):
    def __init__(self):

        QWidget.__init__(self)
        self.items = 0
#        self.setAttribute(Qt.WA_TranslucentBackground)

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        EXPENSE_DATABASE_FILE = os.path.join(script_dir, 'resource', 'expenses.db')

        # SQLite connection
        self.connection = sqlite3.connect(EXPENSE_DATABASE_FILE)
        self.cursor = self.connection.cursor()

        # Create the expenses table if it doesn't exist
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                description TEXT,
                price REAL,
                payment_mode TEXT,
                date TEXT,
                is_income INTEGER
            )"""
        )
        # self.cursor.execute("ALTER TABLE expenses ADD COLUMN is_income INTEGER")

        self.connection.commit()

        # Left Widget
        self.table = QTableWidget()

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                gridline-color: #3c3f41;
                border: none;
            }
            QHeaderView::section {
                background-color: #2b2d30;
                color: #bbbbbb;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #3c3f41;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4e5157;
            }
        """)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Description", "Price", "Payment Mode", "Date"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Right Widget
        self.description = QLineEdit()
        self.description.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                padding: 8px;
                background-color: #2b2d30;
                color: #e0e0e0;
                border: 1px solid #3c3f41;
            }
            QLineEdit:focus {
                border: 1px solid #4a9eff;
            }
        """)
        self.price = QLineEdit()
        self.price.setStyleSheet("""
            QLineEdit {
                border-radius: 8px;
                padding: 8px;
                background-color: #2b2d30;
                color: #e0e0e0;
                border: 1px solid #3c3f41;
            }
            QLineEdit:focus {
                border: 1px solid #4a9eff;
            }
        """)

        self.payment_mode = QComboBox()
        self.payment_mode.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                background-color: #2b2d30;
                color: #e0e0e0;
                border: 1px solid #3c3f41;
            }
            QComboBox:hover {
                border: 1px solid #4a9eff;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        self.sortby = QComboBox()
        self.sortby.setStyleSheet("""
            QComboBox {
                border-radius: 8px;
                padding: 8px;
                background-color: #2b2d30;
                color: #e0e0e0;
                border: 1px solid #3c3f41;
            }
            QComboBox:hover {
                border: 1px solid #4a9eff;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        self.sortby.addItem("Date")
        self.sortby.addItem("Price (Low to High)")
        self.sortby.addItem("Price (High to Low)")

        self.date_picker = QDateEdit()
        self.date_picker.setStyleSheet("""
            QDateEdit {
                border-radius: 8px;
                padding: 8px;
                background-color: #2b2d30;
                color: #e0e0e0;
                border: 1px solid #3c3f41;
            }
            QDateEdit:hover {
                border: 1px solid #4a9eff;
            }
        """)

        self.linebreak_widget = QWidget()
        self.linebreak_widget.setFixedHeight(11)

        self.payment_mode.addItem("Cash")
        self.payment_mode.addItem("Credit Card")
        self.payment_mode.addItem("Debit Card")
        self.payment_mode.addItem("EMI")
        self.payment_mode.addItem("Mobile Wallets")
        self.payment_mode.addItem("Paytm")
        self.payment_mode.addItem("Google Pay")
        self.payment_mode.addItem("Apple Pay")
        self.payment_mode.addItem("Amazon Pay")
        self.payment_mode.addItem("Wire Transfer")
        self.payment_mode.addItem("Paypal")

        self.add = QPushButton("Add")
        self.add.setStyleSheet("""
            QPushButton {
                border-radius: 8px;
                padding: 10px;
                background-color: #4a9eff;
                color: white;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:disabled {
                background-color: #3c3f41;
                color: #777;
            }
        """)

        # Disabling 'Add' button
        self.add.setEnabled(False)

        self.right_dock = QDockWidget(self)
        self.right_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.right = QVBoxLayout()
        label_style = "color: #bbbbbb; font-size: 12px; font-weight: bold; padding-top: 10px;"
        
        sort_label = QLabel("Sort By:")
        sort_label.setStyleSheet(label_style)
        self.right.addWidget(sort_label)
        self.right.addWidget(self.sortby)
        self.right.addWidget(self.linebreak_widget)
        
        desc_label = QLabel("Reason of Expense")
        desc_label.setStyleSheet(label_style)
        self.right.addWidget(desc_label)
        self.right.addWidget(self.description)
        
        price_label = QLabel("Price")
        price_label.setStyleSheet(label_style)
        self.right.addWidget(price_label)
        self.right.addWidget(self.price)
        
        payment_label = QLabel("Payment Mode")
        payment_label.setStyleSheet(label_style)
        self.right.addWidget(payment_label)
        self.right.addWidget(self.payment_mode)
        
        date_label = QLabel("Date of Expense")
        date_label.setStyleSheet(label_style)
        self.right.addWidget(date_label)
        self.right.addWidget(self.date_picker)
        self.right.addWidget(self.add)
        self.right.addWidget(self.chart_view)

        dock_contents = QWidget()
        dock_contents.setLayout(self.right)
        self.right_dock.setWidget(dock_contents)

        # QWidget Layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.right_dock)
        # self.layout.addLayout(self.right)

        self.setLayout(self.layout)

        # Initialize data after all UI components are created
        self.fill_table()
        self.plot_data()
        self.plot_history_graph()

        self.sortby.currentTextChanged.connect(self.sort_by_func)
        self.add.clicked.connect(self.add_element)
        self.description.textChanged[str].connect(self.check_disable)
        self.price.textChanged[str].connect(self.check_disable)
        self.payment_mode.currentTextChanged[str].connect(self.check_disable)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Delete:
            self.clear_element()
        else:
            super().keyPressEvent(event)

    # @Slot()
    def add_element(self):
        des = self.description.text()
        price = self.price.text()
        mode = self.payment_mode.currentText()
        date = self.date_picker.date().toString(Qt.DateFormat.ISODate)

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

            description_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            payment_mode_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)

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
            messagebox.showerror("Invalid Price!", "Invalid Price:", price, "Make sure to enter a valid price!")

    def plot_history_graph(self):
        # Clear any existing series from the chart
        chart = QChart()
        chart.setBackgroundBrush(QBrush(QColor("#191b1f")))  # Set background brush

        # Create a line series for the history graph
        series = QLineSeries()
        series.setName("Expense History")  # Set series name

        # Retrieve data from the database for plotting
        self.cursor.execute("SELECT date, price FROM expenses ORDER BY date")
        expense_data = self.cursor.fetchall()

        # Populate the line series with data
        for index, (date, price) in enumerate(expense_data):
            # Use index as x-axis value and price as y-axis value
            series.append(float(index), float(price))

        # Add the series to the chart
        chart.addSeries(series)

        # Set chart title and axes labels
        chart.setTitle("Expense History")
        chart.createDefaultAxes()

        # Set the chart to the chart view
        self.chart_view.setChart(chart)

        # Adjust chart appearance if needed
        # (e.g., set background color, legend position, axis labels, etc.)

    def import_(self):

        reply = QMessageBox.question(self, 'Wait a Min!', 'Are the column names included in the file>?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
            if fileName:
                print(fileName)
                with open(fileName, 'r') as f:
                    reader = csv.reader(f)
                    columns = next(reader)
                    query = 'insert into expenses({0}) values ({1})'
                    query = query.format(','.join(columns), ','.join('?' * len(columns)))
                    cursor = self.connection.cursor()
                    for data in reader:
                        cursor.execute(query, data)
                    self.connection.commit()
            else:
                pass
        else:
            fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)")
            if fileName:
                print(fileName)
                with open(fileName, 'r') as f:
                    reader = csv.reader(f)
                    data = next(reader)
                    query = 'insert into expenses values ({0})'
                    query = query.format(','.join('?' * len(data)))
                    cursor = self.connection.cursor()
                    cursor.execute(query, data)
                    for data in reader:
                        cursor.execute(query, data)
                    self.connection.commit()
            else:
                pass

    def check_disable(self, x):
        if not self.description.text() or not self.price.text() or not self.payment_mode.currentText():
            self.add.setEnabled(False)
        else:
            self.add.setEnabled(True)

    def sort_by_date_clicked(self):
        self.table.sortItems(3, Qt.SortOrder.AscendingOrder)  # Sort by date column (index 3) in ascending order

    def sort_by_price_htl_clicked(self):
        self.table.sortItems(1, Qt.SortOrder.AscendingOrder)  # Sort by price column (index 1) in ascending order

    def sort_by_price_lth_clicked(self):
        self.table.sortItems(1, Qt.SortOrder.AscendingOrder)  # Sort by price column (index 1) in ascending order

    def sort_by_func(self):
        a = self.sortby.currentText()
        if a == "Date":
            self.sort_by_date_clicked()
        elif a == "Price (Low to High)":
            self.sort_by_price_htl_clicked()
        else:
            self.sort_by_price_lth_clicked()

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
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.chart_view.setChart(chart)

    def fill_table(self):
        self.cursor.execute("""SELECT * FROM expenses""")
        expenses = self.cursor.fetchall()

        for desc, price, mode, date, is_income in expenses:
            description_item = QTableWidgetItem(desc)
            price_item = QTableWidgetItem(f"{price:.2f}")
            payment_mode_item = QTableWidgetItem(mode)
            date_item = QTableWidgetItem(date)

            description_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            payment_mode_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)

            self.table.insertRow(self.items)
            self.table.setItem(self.items, 0, description_item)
            self.table.setItem(self.items, 1, price_item)
            self.table.setItem(self.items, 2, payment_mode_item)
            self.table.setItem(self.items, 3, date_item)

            self.items += 1

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

    def clear_table(self):
        self.table.setRowCount(0)
        self.items = 0

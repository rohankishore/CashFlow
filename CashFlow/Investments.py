import sys
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (NavigationInterface, NavigationItemPosition, MessageBox,
                            isDarkTheme, setTheme, Theme, ComboBox, PushButton,LineEdit,
                            PopUpAniStackedWidget, setThemeColor)
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChartView, QPieSeries, QChart


class Investments(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("Investments")

        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # Create the option combo box
        self.option_combo = ComboBox()

        self.option_combo.addItem("Lumpsum")
        self.option_combo.addItem("Recurring")
        self.option_combo.currentTextChanged.connect(self.updateUI)

        # Create a QVBoxLayout for the existing widgets
        self.inputs_layout = QVBoxLayout()

        # Create input labels and fields
        self.amount_label = QLabel("Initial Amount:")
        self.amount_field = LineEdit()

        self.amount_slider = QSlider(Qt.Horizontal)
        self.amount_slider.setMinimum(0)
        self.amount_slider.setMaximum(1000000)
        self.amount_slider.valueChanged.connect(self.updateAmountField)

        self.interest_label = QLabel("Interest Rate (%):")
        self.interest_field = LineEdit()

        self.interest_slider = QSlider(Qt.Horizontal)
        self.interest_slider.setMinimum(0)
        self.interest_slider.setMaximum(35)
        self.interest_slider.valueChanged.connect(self.updateInterestField)

        self.years_label = QLabel("Number of Years:")
        self.years_field = LineEdit()

        self.years_slider = QSlider(Qt.Horizontal)
        self.years_slider.setMinimum(0)
        self.years_slider.setMaximum(60)
        self.years_slider.valueChanged.connect(self.updateYearsField)

        # Add the input fields and sliders to the inputs_layout
        self.inputs_layout.addWidget(self.amount_label)
        self.inputs_layout.addWidget(self.amount_field)
        self.inputs_layout.addWidget(self.amount_slider)
        self.inputs_layout.addWidget(self.interest_label)
        self.inputs_layout.addWidget(self.interest_field)
        self.inputs_layout.addWidget(self.interest_slider)
        self.inputs_layout.addWidget(self.years_label)
        self.inputs_layout.addWidget(self.years_field)
        self.inputs_layout.addWidget(self.years_slider)

        # Add the inputs_layout to the main layout
        self.layout.addWidget(self.option_combo)
        self.layout.addLayout(self.inputs_layout)

        # Create the calculate button
        self.calculate_button = PushButton("Calculate")

        self.calculate_button.clicked.connect(self.calculate)

        # Create the result label
        self.result_label = QLabel("")
        self.result_label.setFont(("Consolas", 14))
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Add the calculate button and result label to the main layout
        self.layout.addWidget(self.calculate_button)
        self.layout.addWidget(self.result_label)

        # Create the pie chart
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setStyleSheet("background-color: #191b1f")

        # Set the layout stretch factor of the chart_view
        self.layout.addWidget(self.chart_view, stretch=1)

        # Set the central widget of the main window
        self.setCentralWidget(self.widget)

        # Initialize the UI based on the selected option
        self.updateUI()

    def updateUI(self):
        option = self.option_combo.currentText()
        if option == "Lumpsum":
            self.years_label.setEnabled(True)
            self.years_field.setEnabled(True)
            self.years_slider.setEnabled(True)
        elif option == "Recurring":
            self.years_label.setEnabled(False)
            self.years_field.setEnabled(False)
            self.years_slider.setEnabled(False)

    def updateAmountField(self):
        self.amount_field.setText(str(self.amount_slider.value()))

    def updateInterestField(self):
        self.interest_field.setText(str(self.interest_slider.value()))

    def updateYearsField(self):
        self.years_field.setText(str(self.years_slider.value()))

    def calculate(self):
        try:
            option = self.option_combo.currentText()
            if option == "Lumpsum":
                amount = float(self.amount_field.text())
                interest = float(self.interest_field.text())
                years = int(self.years_field.text())

                # Perform the lump sum calculation
                result = amount * (1 + (interest / 100)) ** years
                self.result_label.setText(f"Total amount after {years} years: {result:.2f}")

                # Update the pie chart
                self.updatePieChart(amount, result)
            elif option == "Recurring":
                amount = float(self.amount_field.text())
                interest = float(self.interest_field.text())
                years = int(self.years_field.text())

                # Perform the recurring calculation
                total = 0
                for i in range(years):
                    total += amount
                    total *= (1 + (interest / 100))
                self.result_label.setText(f"Total amount after {years} years: {total:.2f}")

                # Update the pie chart
                self.updatePieChart(amount * years, total)

        except ValueError:
            self.result_label.setText("Invalid input")

    def updatePieChart(self, investment, returns):
        chart = QChart()
        series = QPieSeries()
        series.append("Investment", investment)
        series.append("Returns", returns - investment)
        chart.addSeries(series)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart.setBackgroundBrush(QBrush(QColor("#191b1f")))
        legend = chart.legend()
        legend.setBrush(QBrush(QColor("#FFFFFF")))
        self.chart_view.setChart(chart)
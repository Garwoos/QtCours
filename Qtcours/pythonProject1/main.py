import pickle

from PySide6 import QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, \
    QListWidget, QGridLayout, QSizePolicy, QMenuBar, QTextEdit
from functools import partial


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator baby")

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)


        self.history = QTextEdit()
        self.history.setReadOnly(True)
        main_layout.addWidget(self.history)

        self.result = QLabel("0")
        self.result.setStyleSheet("background-color: grey")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setAlignment(Qt.AlignBottom)
        self.result.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result.setScaledContents(True)
        main_layout.addWidget(self.result)

        main_layout.addLayout(grid_layout)

        buttons = {
            "9": (1, 2),
            "8": (1, 1),
            "7": (1, 0),
            "6": (2, 2),
            "5": (2, 1),
            "4": (2, 0),
            "3": (3, 2),
            "2": (3, 1),
            "1": (3, 0),
            "0": (4, 0, 1, 2),
            "C": (0, 0),
            ".": (4, 2)
        }

        button_objects = {}
        for button_text, grid_position in buttons.items():
            button = QPushButton(button_text)
            button.setStyleSheet("""
                QPushButton {
                    background-color: black;
                }
                QPushButton:hover {
                    background-color: red;
                }
            """)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            grid_layout.addWidget(button, *grid_position)
            button_objects[button_text] = button

        multiplication = QPushButton("*")
        multiplication.setStyleSheet("""
                                        QPushButton {
                                            background-color: black;
                                        }
                                        QPushButton:hover {
                                            background-color: red;
                                        }
                                    """)
        multiplication.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        addition = QPushButton("+")
        addition.setStyleSheet("""
                                        QPushButton {
                                            background-color: black;
                                        }
                                        QPushButton:hover {
                                            background-color: red;
                                        }
                                    """)
        addition.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        soustraction = QPushButton("-")
        soustraction.setStyleSheet("""
                                        QPushButton {
                                            background-color: black;
                                        }
                                        QPushButton:hover {
                                            background-color: red;
                                        }
                                    """)
        soustraction.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        egal = QPushButton("=")
        egal.setStyleSheet("""
                                        QPushButton {
                                            background-color: black;
                                        }
                                        QPushButton:hover {
                                            background-color: red;
                                        }
                                    """)
        egal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        division = QPushButton("/")
        division.setStyleSheet("""
                                        QPushButton {
                                            background-color: black;
                                        }
                                        QPushButton:hover {
                                            background-color: red;
                                        }
                                    """)
        division.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        grid_layout.addWidget(multiplication, 1, 3)
        grid_layout.addWidget(addition, 3, 3)
        grid_layout.addWidget(soustraction, 2, 3)
        grid_layout.addWidget(egal, 4, 3)
        grid_layout.addWidget(division, 0, 3)

        #connexion des boutons
        for button_text in buttons.keys():
            button_objects[button_text].clicked.connect(partial(self.add_number, button_text))

        multiplication.clicked.connect(partial(self.add_number, "*"))
        addition.clicked.connect(partial(self.add_number, "+"))
        soustraction.clicked.connect(partial(self.add_number, "-"))
        division.clicked.connect(partial(self.add_number, "/"))
        egal.clicked.connect(partial(self.calculate))

        button_objects['C'].clicked.connect(lambda: self.result.setText("0"))
        button_objects['.'].clicked.connect(lambda: self.result.setText(self.result.text() + "."))

        try:
            with open('history.pkl', 'rb') as f:
                self.history.setPlainText(pickle.load(f))
        except FileNotFoundError:
            pass

        self.setLayout(main_layout)

    def resizeEvent(self, event):
        # Call the parent class method first
        super().resizeEvent(event)

        # Calculate the new font size based on the window size
        new_font_size = self.width() // 20  # Adjust the divisor to get the desired font size

        # Create a new QFont object with the new size
        new_font = QFont("Arial", new_font_size)
        new_font_history = QFont("Arial", new_font_size//2)
        # Set the new font for the QLabel
        self.result.setFont(new_font)

        self.history.setFont(new_font_history)

        # Set the new font for the buttons
        for button in self.findChildren(QPushButton):
            button.setFont(new_font)

    def keyPressEvent(self, event):
        if event.text() in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/','.', 'C']:
            self.add_number(event.text())
        if event.key() == Qt.Key_Backspace:
            #inférieur ou égal à 1
            if (self.result.text() == "0") or (len(self.result.text()) <= 1):
                self.result.setText("0")
            else :
                self.result.setText(self.result.text()[:-1])
        if event.key() == Qt.Key_Return:
            self.calculate()
        if (event.key() == Qt.Key_Escape) and (self.windowState() == Qt.WindowNoState):
            my_widget.showFullScreen()
        elif (event.key() == Qt.Key_Escape) and (self.windowState() == Qt.WindowFullScreen):
            my_widget.showNormal()


    def add_number(self, number):
        if self.result.text() == "0":
            self.result.setText(number)
        else:
            if (self.result.text()[-1] in ['+', '-', '*', '/','.'] and number in ['+', '-', '*', '/', '.']):
                self.result.setText(self.result.text()[0:-1] + number)
            else :
                self.result.setText(self.result.text() + number)

    def calculate_expression(self, expression):
        for operator in ['+', '-']:
            if operator in expression:
                numbers = expression.split(operator)
                if operator == '+':
                    return self.calculate_expression(numbers[0]) + self.calculate_expression(numbers[1])
                else:
                    return self.calculate_expression(numbers[0]) - self.calculate_expression(numbers[1])

        for operator in ['*', '/']:
            if operator in expression:
                numbers = expression.split(operator)
                if operator == '*':
                    return self.calculate_expression(numbers[0]) * self.calculate_expression(numbers[1])
                else:
                    return self.calculate_expression(numbers[0]) / self.calculate_expression(numbers[1])
        return float(expression)

    def calculate(self):
        text = self.result.text()
        resultat = self.calculate_expression(text)
        self.history.append(f"{text} = {resultat}")
        self.result.setText(str(resultat))

    def closeEvent(self, event):
        # Save history to file
        with open('history.pkl', 'wb') as f:
            pickle.dump(self.history.toPlainText(), f)
        event.accept()

app = QApplication()
my_widget = MyWindow()
my_widget.show()
app.exec()
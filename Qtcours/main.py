from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, QListWidget
from functools import partial


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("To do list")
        self.setFixedSize(400, 500)

        main_layout = QVBoxLayout()
        self.liste_cool = QListWidget()
        self.ecrire_c_est_cool = QLineEdit()
        self.bouton_clear_mais_cool = QPushButton("Clear")
        main_layout.addWidget(self.liste_cool)
        main_layout.addWidget(self.ecrire_c_est_cool)
        main_layout.addWidget(self.bouton_clear_mais_cool)
        self.bouton_clear_mais_cool.clicked.connect(self.clear)
        self.ecrire_c_est_cool.returnPressed.connect(self.add_item)
        self.ecrire_c_est_cool.returnPressed.connect(self.ecrire_c_est_cool.clear)
        self.liste_cool.doubleClicked.connect(self.clear_this_item)
        self.bouton_save = QPushButton("Save")
        self.bouton_save.clicked.connect(self.save_list)
        main_layout.addWidget(self.bouton_save)
        self.setLayout(main_layout)
        self.load_list()

    def clear(self):
        self.liste_cool.clear()

    def clear_this_item(self):
        self.liste_cool.takeItem(self.liste_cool.currentRow())
    def add_item(self):
        self.liste_cool.addItem(self.ecrire_c_est_cool.text())

    def save_list(self):
        with open("todolist.txt", "w") as f:
            for i in range(self.liste_cool.count()):
                f.write(self.liste_cool.item(i).text() + "\n")

    def load_list(self):
        with open("todolist.txt", "r") as f:
            for line in f:
                self.liste_cool.addItem(line.strip())

app = QApplication()
my_widget = MyWindow()
my_widget.show()
app.exec()

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, \
    QLineEdit, QMainWindow, QTableWidget
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Sets up the title of the application
        self.setWindowTitle("Student Manager System")

        # navbar for file and help
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Adding extra menu items for file
        add_student_action = QAction("Add Student", self)
        file_menu_item.addAction(add_student_action)

        # Adding extra menu item for help
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))

        # Sets the widget as a central widget to the main window
        self.setCentralWidget(self.table, 1)


    def load_data(self):
        self.table


app = QApplication(sys.argv)
add_calculator = MainWindow()
add_calculator.show()
sys.exit(app.exec())
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, \
    QLineEdit, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


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
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Adding extra menu item for help
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.load_data()

        # Sets the widget as a central widget to the main window
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")

        # Makes sure that it doesn't overwrite old data
        self.table.setRowCount(0)

        # Iterates through the data
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            print(row_number, row_data)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        """Inserts new student's data into the table in the gui window"""
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
    """Creates a bew gui that takes students data"""
    def __init__(self):
        super().__init__()

        # Set up for new window title and size
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Layout for the new window
        layout = QVBoxLayout()

        # Name input
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Course input list
        self.student_course = QComboBox()
        self.student_course.addItems(["Biology", "Math", "Astronomy", "Physics"])
        layout.addWidget(self.student_course)

        # Mobile input
        self.student_mobile = QLineEdit()
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        # Submit button used to submit the data into the database
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        # Adding the widget into the new window
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.student_course.itemText(self.student_course.currentIndex())
        mobile = self.student_mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES(?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        # Refreshes the data after adding a student
        main_window.load_data()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
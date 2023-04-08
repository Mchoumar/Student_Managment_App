from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, \
    QLineEdit, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, \
    QStatusBar, QGridLayout, QMessageBox
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3


class DatabaseConnection:
    def __init__(self, databasefile="database.db"):
        self.databasefile = databasefile

    def connect(self):
        connection = sqlite3.connect(self.databasefile)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Sets up the title of the application
        self.setWindowTitle("Student Manager System")
        self.setMinimumSize(800, 600)

        # navbar for file, help, and edit
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Adding extra menu items for file
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Adding extra menu item for help
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        # Adding extra menu item for edit
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.open_search)
        edit_menu_item.addAction(search_action)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.load_data()

        # Sets the widget as a central widget to the main window
        self.setCentralWidget(self.table)

        # Set the toolbar widget
        toolbar = QToolBar()
        # Allows the user to move the toolbar where ever they wish
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        # Adding actions widgets
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create status bar and add status bar element
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell clic
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        # Add edit button to the status bar
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        # Add delete button to the status bar
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Clears the status bar buttons
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Add the widgets to the status bar
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = DatabaseConnection().connect()
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

    def open_search(self):
        """Search for a student, and it displays it for you on the table"""
        search_dialog = Search()
        search_dialog.exec()

    def edit(self):
        """Edits students data"""
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        """Deletes students data"""
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        """Displays information about the application"""
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the course "The Python Mega Course".
        Feel free to modify and reuse this app.
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set up for new window title and size
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Layout for the new window
        layout = QVBoxLayout()

        # Gets the selected row
        index = main_window.table.currentRow()

        # Extract the student ID
        self.student_id = main_window.table.item(index, 0).text()

        # Extract the student name
        student_name = main_window.table.item(index, 1).text()

        # Name input
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Extract the student mobile
        course_name = main_window.table.item(index, 2).text()

        # Course input list
        self.student_course = QComboBox()
        self.student_course.addItems(["Biology", "Math", "Astronomy", "Physics"])
        self.student_course.setCurrentText(course_name)
        layout.addWidget(self.student_course)

        # Extract the student mobile
        student_mobile = main_window.table.item(index, 3).text()

        # Mobile input
        self.student_mobile = QLineEdit(student_mobile)
        self.student_mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.student_mobile)

        # Submit button used to submit the data into the database
        submit_button = QPushButton("Update")
        submit_button.clicked.connect(self.update_student)
        layout.addWidget(submit_button)

        # Adding the widget into the new window
        self.setLayout(layout)

    def update_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(), self.student_course.currentText(), self.student_mobile.text(),
                        self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set up for new window title
        self.setWindowTitle("Delete Student Data")

        # Layout for the new window
        layout = QGridLayout()

        # Confirmation for deletion
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        # Adding all widgets into the window
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)

        # Adds the layout into the window
        self.setLayout(layout)

        # Checks if the user pressed yes or no
        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.cancel)

    def cancel(self):
        """If the user press no then it closes the delete window"""
        self.close()

    def delete_student(self):
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The records was deleted successfully")
        confirmation_widget.exec()


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
        # Gets the data from the input window
        name = self.student_name.text()
        course = self.student_course.itemText(self.student_course.currentIndex())
        mobile = self.student_mobile.text()

        # Starts a connection with the database file
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        # Executes SQL query to insert students data into the database
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES(?, ?, ?)",
                       (name, course, mobile))

        # Commits the data into the database and closes the connection
        connection.commit()
        cursor.close()
        connection.close()

        # Refreshes the data after adding a student
        main_window.load_data()


class Search(QDialog):
    def __init__(self):
        super().__init__()

        # Set up for new window title and size
        self.setWindowTitle("Search Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Student")
        layout.addWidget(self.search_input)

        # Search button
        search_button = QPushButton("Enter")
        search_button.clicked.connect(self.data_search)
        layout.addWidget(search_button)

        # Adds all the widgets into the search window
        self.setLayout(layout)

    def data_search(self):
        name = self.search_input.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()

        """Refers to the main window, searches for the name
        and check if the flags matches the name"""
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        # Iterates through the list of matches names and displays them
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        # Commits the data into the database and closes the connection
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
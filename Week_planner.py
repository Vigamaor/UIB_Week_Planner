import Find_time
import plan_scraper
import datetime

import sys
import os
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QPalette, QColor, QIcon, QCursor
from PySide2.QtWidgets import (QAction, QApplication, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QWidget, QStyleFactory, QMessageBox, QGridLayout, QComboBox)


class SubjectControls(QWidget):
    def __init__(self, mainwindow):
        QWidget.__init__(self)
        self.mainwindow = mainwindow

        # Create labels
        self.semester_drop_down_label = QLabel("Choose Semester", self)

        # Create buttons
        self.add_subject_button = QPushButton("Add Subject", self)
        self.delete_subject_button = QPushButton("Delete subject")
        self.clear_json_button = QPushButton("Clear all subjects", self)

        # Text line field
        self.add_subject_field = QLineEdit(self)

        # Connect buttons
        self.add_subject_button.clicked.connect(self.add_subject)
        self.add_subject_field.returnPressed.connect(self.add_subject)
        self.delete_subject_button.clicked.connect(self.delete_subject)
        self.clear_json_button.clicked.connect(self.clear_json_action)

        # Drop down menues
        self.semester_drop_down = QComboBox(self)
        self.delete_subject_drop_down = QComboBox(self)

        # Gets the data we will have in the drop down menues
        self.update_subject_drop_down()
        self.set_semester_drop_down()

        self.grid = QGridLayout()

        # Add widgets to layout
        self.grid.addWidget(self.add_subject_field, 0, 0)
        self.grid.addWidget(self.add_subject_button, 0, 1)
        self.grid.addWidget(self.semester_drop_down_label, 1, 0)
        self.grid.addWidget(self.semester_drop_down, 2, 0)
        self.grid.addWidget(self.delete_subject_button, 3, 1)
        self.grid.addWidget(self.delete_subject_drop_down, 3, 0)
        self.grid.addWidget(self.clear_json_button, 4, 0)

        self.setLayout(self.grid)

    @Slot()
    def clear_json_action(self):
        try:
            os.remove("plans.json")
        except FileNotFoundError:
            pass  # If the file doesn't exist we just move on

        self.update_subject_drop_down()

    @Slot()
    def add_subject(self):
        self.mainwindow.application.setOverrideCursor(QCursor(Qt.WaitCursor))
        subject = plan_scraper.extract_data(self.add_subject_field.text(), self.semester_drop_down.currentData())
        if subject == "error":
            self.mainwindow.error_message("Could not find the subject please check that you have spelled the id correctly")
        else:
            self.mainwindow.subjects.append(subject)
            self.update_subject_drop_down()
            self.add_subject_field.clear()

        self.mainwindow.application.restoreOverrideCursor()

    def delete_subject(self):
        subject = self.delete_subject_drop_down.currentData()
        box = QMessageBox()
        box.setText(f"Are you sure you want to delete {subject.subject_code}")
        box.setIcon(QMessageBox.Question)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        button = box.exec_()
        if button == QMessageBox.Yes:
            self.mainwindow.subjects.remove(subject)
            self.update_subject_drop_down()

    def update_subject_drop_down(self):
        self.delete_subject_drop_down.clear()
        for subject in self.mainwindow.subjects:
            self.delete_subject_drop_down.addItem(subject.subject_code, userData=subject)

    def set_semester_drop_down(self):
        # TODO finne en måtte å sette det neste semesteret som default
        year = datetime.datetime.now().year
        self.semester_drop_down.addItem(f"{year} Spring", userData=f"{year - 2000}v")
        self.semester_drop_down.addItem(f"{year} Autumn", userData=f"{year - 2000}h")
        self.semester_drop_down.addItem(f"{year} Spring", userData=f"{year - 1999}v")
        self.semester_drop_down.addItem(f"{year} Autumn", userData=f"{year - 1999}h")




class ResultWidget(QWidget):
    def __init__(self, mainwindow):
        QWidget.__init__(self)
        self.mainwindow = mainwindow

        # Create labels
        self.search_bar_label = QLabel("Search Bar", self)

        # Create buttons
        self.create_schedule_button = QPushButton("Create Schedule", self)
        self.advanced_options_button = QPushButton("Advanced Options", self)
        self.search_button = QPushButton("Search", self)

        # Text line field
        self.search_bar = QLineEdit(self)

        # The resutl window
        self.result_list = QTableWidget(self)

        # connect buttons
        self.create_schedule_button.clicked.connect(self.create_shecdule)
        self.advanced_options_button.clicked.connect(self.advanced_options)
        self.search_button.clicked.connect(self.search)
        self.search_bar.returnPressed.connect(self.search)  # returnPressed notices when enter is pressed

        self.grid = QGridLayout()

        # Adding widgets to layout
        self.grid.addWidget(self.create_schedule_button, 1, 0)
        self.grid.addWidget(self.search_bar_label, 0, 1)
        self.grid.addWidget(self.search_bar, 1, 1)
        self.grid.addWidget(self.search_button, 1, 2)
        self.grid.addWidget(self.advanced_options_button, 1, 3)
        self.grid.addWidget(self.result_list, 2, 0, 1, 4)

        self.setLayout(self.grid)




    @Slot()
    def create_shecdule(self):
        if self.mainwindow.subjects == [] :
            self.mainwindow.error_message("No subjects loaded plese add some subjects and try again.")
        else:
            schedule = Find_time.create_schedules(self.subjects)
        # TODO must we gather information from multiple sources like a variable and from the Json or do we load from
        #  the Json earlier and get all information from variable
        #  TODO show the information on the screen


    @Slot()
    def advanced_options(self):
        pass

    @Slot()
    def search(self):
        text = self.search_bar.text()
        print(text)

class MainWindow(QMainWindow):
    def __init__(self, subjects, application):
        # Data
        self.subjects = subjects
        self.application = application

        QMainWindow.__init__(self)
        self.setWindowTitle("UIB Week Planner")
        self.setGeometry(600, 200, 600, 800)  # The first two sets the location the window spawns
        self.setMinimumHeight(600)
        self.setMinimumWidth(800)

        # Logo
        icon = QIcon("deps/logo-transparent.png")
        self.setWindowIcon(icon)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Options")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)


        # Changing the colour theme of the application
        set_dark_theme = QAction("Set Dark Theme", self)
        set_dark_theme.triggered.connect(self.dark_theme)

        # Adding all the buttons we created above to the menu bar.
        self.file_menu.addAction(exit_action)
        self.file_menu.addAction(set_dark_theme)

        # Create and set the central widget
        self.controls = QWidget()
        self.setCentralWidget(self.controls)

        # We set the layout we will use for our two custom sets of widgets
        self.controlsLayout = QHBoxLayout()

        result_square = ResultWidget(self)
        subject_controls = SubjectControls(self)

        self.controlsLayout.addWidget(result_square)
        self.controlsLayout.addWidget(subject_controls)
        self.controls.setLayout(self.controlsLayout)
        #self.controlsLayout.

    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def dark_theme(self):  # TODO make a settings file so you can remember settings
        # TODO make it so you can switch between colours.
        app.setStyle(QStyleFactory.create("fusion"))
        darktheme = QPalette()
        darktheme.setColor(QPalette.Window, QColor(45, 45, 45))
        darktheme.setColor(QPalette.WindowText, QColor(222, 222, 222))
        darktheme.setColor(QPalette.Button, QColor(45, 45, 45))
        darktheme.setColor(QPalette.ButtonText, QColor(222, 222, 222))
        darktheme.setColor(QPalette.AlternateBase, QColor(222, 222, 222))
        darktheme.setColor(QPalette.ToolTipBase, QColor(222, 222, 222))
        darktheme.setColor(QPalette.Highlight, QColor(45, 45, 45))

        app.setPalette(darktheme)

    @Slot()
    def error_message(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

def menu():
    pass
    # TODO System for å hente data
    # TODO GUI for å vise data
    # TODO system for å cleare json lagret data.



if __name__ == "__main__":
    subjects = Find_time.get_data()
    app = QApplication(sys.argv)
    window = MainWindow(subjects, app)
    window.resize(800, 600)
    window.show()
    app.exec_()



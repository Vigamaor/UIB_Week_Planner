import Find_time
import plan_scraper

import sys
import os
import datetime
import qdarkstyle
from PySide2.QtCore import Qt, Slot
from PySide2.QtGui import QIcon, QCursor
from PySide2.QtWidgets import (QAction, QApplication, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTableWidget, QTableWidgetItem,
                               QWidget, QMessageBox, QGridLayout, QComboBox)


class SubjectControls(QWidget):
    def __init__(self, mainwindow):
        QWidget.__init__(self)
        self.mainwindow = mainwindow

        # Create labels
        self.spacer_label = QLabel("", self)
        self.semester_drop_down_label = QLabel("Choose Semester", self)

        # Create buttons
        self.add_subject_button = QPushButton("Add Subject", self)
        self.delete_subject_button = QPushButton("Delete subject")
        self.clear_json_button = QPushButton("Clear all subjects", self)
        self.save_to_file_button = QPushButton("Save subjects to file", self)

        # Text line field
        self.add_subject_field = QLineEdit(self)

        # Connect buttons
        self.add_subject_button.clicked.connect(self.add_subject)
        self.add_subject_field.returnPressed.connect(self.add_subject)
        self.delete_subject_button.clicked.connect(self.delete_subject)
        self.clear_json_button.clicked.connect(self.clear_json_action)
        self.save_to_file_button.clicked.connect(self.save_subjects_file)

        # Drop down menues
        self.semester_drop_down = QComboBox(self)
        self.delete_subject_drop_down = QComboBox(self)

        # Gets the data we will have in the drop down menues
        self.update_subject_drop_down()
        self.set_semester_drop_down()

        self.grid = QGridLayout()

        # Add widgets to layout
        self.grid.addWidget(self.spacer_label, 0, 0)
        self.grid.addWidget(self.add_subject_field, 1, 0)
        self.grid.addWidget(self.add_subject_button, 1, 1)
        self.grid.addWidget(self.save_to_file_button, 2, 0)
        self.grid.addWidget(self.semester_drop_down_label, 3, 0)
        self.grid.addWidget(self.semester_drop_down, 4, 0)
        self.grid.addWidget(self.delete_subject_button, 5, 1)
        self.grid.addWidget(self.delete_subject_drop_down, 5, 0)
        self.grid.addWidget(self.clear_json_button, 6, 0)

        self.setLayout(self.grid)

    @Slot()
    def save_subjects_file(self):
        plan_scraper.write_to_file(self.mainwindow.subjects)
        self.mainwindow.information_message("Save successfull")

    @Slot()
    def clear_json_action(self):
        try:
            os.remove("plans.json")
        except FileNotFoundError:
            pass  # If the file doesn't exist we just move on

        self.mainwindow.subjects = []
        self.update_subject_drop_down()

    @Slot()
    def add_subject(self):
        self.mainwindow.application.setOverrideCursor(QCursor(Qt.WaitCursor))
        subject = plan_scraper.extract_data(self.add_subject_field.text(), self.semester_drop_down.currentData())
        if subject == "error":
            self.mainwindow.information_message("Could not find the subject please check that you have spelled the id correctly")
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
        year = datetime.datetime.now().year
        self.semester_drop_down.addItem(f"{year} Spring", userData=f"{year - 2000}v")
        self.semester_drop_down.addItem(f"{year} Autumn", userData=f"{year - 2000}h")
        self.semester_drop_down.addItem(f"{year + 1} Spring", userData=f"{year - 1999}v")
        self.semester_drop_down.addItem(f"{year + 1} Autumn", userData=f"{year - 1999}h")

        if datetime.datetime.now().month <= 7:
            self.semester_drop_down.setCurrentIndex(1)
        else:
            self.semester_drop_down.setCurrentIndex(0)


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

        # The result window
        self.result_list = QTableWidget(self)

        # connect buttons
        self.create_schedule_button.clicked.connect(self.create_schedule)
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
    def create_schedule(self):
        self.result_list.clear()
        if not self.mainwindow.subjects:  # Checks that the subject list is empty
            self.mainwindow.information_message("No subjects loaded plese add some subjects and try again.")
        else:
            schedule = Find_time.create_schedules(self.mainwindow.subjects)

            self.result_header = []
            for i, group in enumerate(schedule[0]):
                self.result_list.insertColumn(i)
                self.result_header.append(str(group.subject_code))

            self.result_list.setColumnCount(len(self.result_header))
            self.result_list.setHorizontalHeaderLabels(self.result_header)
            self.result_list.setRowCount(len(schedule))

            for row, groups in enumerate(schedule):
                for column, group in enumerate(groups):
                    self.result_list.setItem(row, column, QTableWidgetItem(group.name))
            # TODO find ways to improve the display


    @Slot()
    def advanced_options(self):
        self.mainwindow.information_message("Not yet implemented")

    @Slot()
    def search(self):
        subject_code = None
        for row in range(self.result_list.rowCount()):
            self.result_list.showRow(row)
        text = self.search_bar.text()
        if ":" in text:
            subject_code = text.split(":")[0]
            text = "".join(text.split(":")[1:])
        text = text.strip()
        items = self.result_list.findItems(text, Qt.MatchContains)
        row_list = []
        if subject_code is not None:
            for i, column in enumerate(self.result_header):
                if subject_code.lower() == column.lower():
                    column_index = i
            for item in items:
                if item.column() == column_index:
                    row_list.append(item.row())
        else:
            for item in items:
                row_list.append(item.row())
        for row in range(self.result_list.rowCount()):
            if row not in row_list:
                self.result_list.hideRow(row)


class MainWindow(QMainWindow):
    def __init__(self, subjects, application):
        # Data
        self.subjects = subjects
        self.application = application

        # Information about if the application is in dark mode
        self.dark_mode = False

        QMainWindow.__init__(self)
        self.setWindowTitle("UIB Week Planner")
        self.setGeometry(600, 200, 850, 600)  # The first two sets the location the window spawns
        self.setMinimumHeight(600)
        self.setMinimumWidth(850)

        # Logo
        icon = QIcon("deps/logo-transparent.png")
        self.setWindowIcon(icon)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("Options")

        # Exit QAction
        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.exit_app)

        # Changing the colour theme of the application
        self.set_dark_theme = QAction("Set Dark Theme", self)
        self.set_dark_theme.triggered.connect(self.dark_theme)

        #About menu
        self.about_menu = QAction("About", self)
        self.about_menu.triggered.connect(self.about)


        # Adding all the buttons we created above to the menu bar.
        self.file_menu.addAction(self.exit_action)
        self.file_menu.addAction(self.set_dark_theme)
        self.file_menu.addAction(self.about_menu)

        # Create and set the central widget
        self.controls = QWidget()
        self.setCentralWidget(self.controls)

        # We set the layout we will use for our two custom sets of widgets
        self.controlsLayout = QGridLayout()

        result_square = ResultWidget(self)
        subject_controls = SubjectControls(self)

        self.controlsLayout.setColumnStretch(0, 2)
        self.controlsLayout.setColumnStretch(1, 0)

        self.controlsLayout.addWidget(result_square, 0, 0, 5, 1)
        self.controlsLayout.addWidget(subject_controls, 0, 1, 1, 1)

        self.controls.setLayout(self.controlsLayout)

    @Slot()
    def about(self):
        pass

    @Slot()
    def exit_app(self):
        QApplication.quit()

    @Slot()
    def dark_theme(self):  # TODO make a settings file so you can remember settings
        if not self.dark_mode:
            app.setStyleSheet(qdarkstyle.load_stylesheet())
            self.set_dark_theme.setText("Set Light Theme")
            self.dark_mode = True
        else:
            app.setStyleSheet("")
            self.set_dark_theme.setText("Set Dark Theme")
            self.dark_mode = False

    @Slot()
    def information_message(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()


if __name__ == "__main__":
    subjects = Find_time.get_data()
    app = QApplication(sys.argv)
    window = MainWindow(subjects, app)
    window.show()
    sys.exit(app.exec_())

import sys
import os
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, QCoreApplication, Qt


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

    # Override the default method to avoid exiting the tray application.
    def closeEvent(self, event):
        event.ignore()
        self.hide()


# Create a custom QMainWindow class for the system tray example
class SystemTrayExample(QObject):

    def __init__(self):
        super(SystemTrayExample, self).__init__()

        # Create a QSystemTrayIcon instance and set the icon to the given path
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("media/ear.jpeg"))

        # Create a QMenu for the tray icon's context menu
        tray_menu = QMenu()

        # Create a "Start" action for the context menu
        start_action = tray_menu.addAction("Start")
        start_action.triggered.connect(self.start_transcribe)

        # Create a "Pause" action for the context menu
        pause_action = tray_menu.addAction("Pause")
        pause_action.triggered.connect(self.pause_transcribe)

        # Rename the "Hide" action to "End"
        end_action = tray_menu.addAction("End")
        end_action.triggered.connect(self.end_transcribe)

        # Create a "Show" action for the context menu
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show_window)

        # Create an "Exit" action for the context menu
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app)

        # Set the context menu for the tray icon
        self.tray_icon.setContextMenu(tray_menu)
        # Show the tray icon
        self.tray_icon.show()

    def start_transcribe(self):
        """Wrapper of starting a transcribe function"""
        print("Starting transcribing")

    def pause_transcribe(self):
        """Wrapper of pausing a transcribing function"""
        print("Pausing transcribing")

    def end_transcribe(self):
        """Wrapper of ending a transcribe function"""
        print("Ending transcribing")

    def pause_transcribe(self):
        """Wrapper of pausing a transcribing function"""
        print("Pausing transcribing")
    
    def show_window(self):
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Transcribed text will be shown here.")
        self.text_edit.setFixedSize(500, 500)

        self.window = MyWindow()
        self.window.setWindowTitle("My Window")
        self.window.setFixedSize(550, 550)

        layout = QVBoxLayout(self.window)
        layout.addWidget(self.text_edit)

        self.window.show()

    # Custom slot for exiting the application
    def exit_app(self):
        # Hide the tray icon and quit the application
        self.tray_icon.hide()
        QCoreApplication.instance().quit()


if __name__ == '__main__':
    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Set the application identifier and name
    app.setApplicationName('SystemTrayApp')
    app.setOrganizationName('com.example')

    # Set application attributes to enable high DPI scaling and plugin-based applications on macOS
    # app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # app.setAttribute(Qt.AA_EnableHighDpiScaling)
    # app.setAttribute(Qt.AA_MacPluginApplication)
    app.setDesktopFileName('Info.plist')

    # Create an instance of the SystemTrayExample class and run the application event loop
    ex = SystemTrayExample()
    sys.exit(app.exec())

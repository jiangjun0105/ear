from __future__ import annotations

import asyncio
import sys
import signal
import logging
from pathlib import Path

from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QVBoxLayout, QWidget, QTextEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QObject, QCoreApplication

from transcribe import transcribe_audio
from collect import collect_audio


def get_asset_path(path: str):
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys._MEIPASS)
    else:
        base_dir = Path(__file__).parent.parent

    return str(base_dir / path)

class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

    def closeEvent(self, event):
        event.ignore()
        self.hide()

async def start_transcribe():
    # queue = asyncio.Queue()

    collector_task = asyncio.create_task(collect_audio(recording_length=5))
    transcriber_task = asyncio.create_task(transcribe_audio())

    await asyncio.gather(collector_task, transcriber_task)

ICON_PATH = get_asset_path("asset/ear.png")


class EarTrayApp(QObject):
    def __init__(self):
        super(EarTrayApp, self).__init__()

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(ICON_PATH))
        logging.debug(f'ICON_PATH: {ICON_PATH}')

        tray_menu = QMenu()
        self.initialize_tray_menu(tray_menu)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


    def initialize_tray_menu(self, tray_menu: QMenu) -> None:
        """Add buttons to the tray menu."""
        start_action = tray_menu.addAction("Start")
        start_action.triggered.connect(self.start_transcribe)

        pause_action = tray_menu.addAction("Pause")
        pause_action.triggered.connect(self.pause_transcribe)

        end_action = tray_menu.addAction("End")
        end_action.triggered.connect(self.end_transcribe)

        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show_window)

        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_app)

        
    def start_transcribe(self):
        logging.debug("Starting transcribing")
        asyncio.run(start_transcribe())

    def pause_transcribe(self):
        logging.debug("Pausing transcribing")

    def end_transcribe(self):
        logging.debug("Ending transcribing")

    def show_window(self):
        if not hasattr(self, 'window'):
            self.text_edit = QTextEdit()
            self.text_edit.setPlaceholderText(f"Transcribed text will be shown here.\n{ICON_PATH}")
            self.text_edit.setFixedSize(500, 500)

            self.window = MyWindow()
            self.window.setWindowTitle("My Window")
            self.window.setFixedSize(550, 550)

            layout = QVBoxLayout(self.window)
            layout.addWidget(self.text_edit)

        self.window.show()
        self.window.activateWindow()
        self.window.raise_()

    def exit_app(self):
        self.tray_icon.hide()
        QCoreApplication.instance().quit()


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)

    app.setApplicationName('Ear')
    app.setOrganizationName('Jun Jiang')

    ex = EarTrayApp()
    sys.exit(app.exec()) 


if __name__ == '__main__':
    main()
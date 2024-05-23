# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import QSize
from views.analyzer_view import AnalyzerView
from models.video_model import VideoModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SignSense")
        self.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        self.setMinimumSize(900, 540)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QHBoxLayout(self.main_widget)

        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_widget)

        self.logo_label = QLabel("SignSense")
        self.logo_label.setObjectName("logo_label")
        self.menu_list = QListWidget()
        self.menu_list.setObjectName("menu_list")
        self.menu_list.setIconSize(QSize(32, 32))
        self.add_menu_item("Обучение", "./resources/icons/Home.svg")
        self.add_menu_item("Словарь", "./resources/icons/Dictionary.svg")
        self.add_menu_item("Анализатор", "./resources/icons/View.svg")
        self.add_menu_item("Статистика", "./resources/icons/Market.svg")
        self.add_menu_item("Настройки", "./resources/icons/Setting.svg")

        self.menu_list.currentItemChanged.connect(self.display_module)

        self.nav_container = QWidget()
        self.nav_layout = QVBoxLayout(self.nav_container)
        self.nav_layout.addWidget(self.logo_label)
        self.nav_layout.addWidget(self.menu_list)
        self.layout.addWidget(self.nav_container)

        self.content_area = QWidget()
        self.content_area.setObjectName("content")
        self.content_layout = QVBoxLayout(self.content_area)
        self.layout.addWidget(self.content_area)

        self.analyzer_view = AnalyzerView()
        self.video_model = VideoModel()
        self.video_model.frame_ready.connect(self.analyzer_view.update_frame)
        self.video_model.gesture_recognized.connect(self.analyzer_view.update_gesture)

        self.controllers = {
            "Обучение": QLabel("Обучение"),
            "Словарь": QLabel("Словарь"),
            "Анализатор": self.analyzer_view,
            "Статистика": QLabel("Статистика"),
            "Настройки": QLabel("Настройки")
        }

        self.current_module = None

    def add_menu_item(self, name, icon_path=None):
        item = QListWidgetItem(name)
        if icon_path:
            item.setIcon(QIcon(icon_path))
        self.menu_list.addItem(item)

    def display_module(self, current, previous):
        if not current:
            return

        if self.current_module is not None:
            self.content_layout.removeWidget(self.current_module)
            self.current_module.hide()

        self.current_module = self.controllers.get(current.text())
        if self.current_module:
            self.content_layout.addWidget(self.current_module)
            self.current_module.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("resources/styles/styles.qss", "r", encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

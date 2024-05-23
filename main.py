import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from controllers.learning_controller import LearningController
from controllers.dictionary_controller import DictionaryController
from controllers.analyzer_controller import AnalyzerController
from controllers.statistics_controller import StatisticsController
from controllers.settings_controller import SettingsController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SignSense")

        # Установка иконки приложения
        self.setWindowIcon(QIcon("./resources/icons/logo.svg"))

        # Установка минимального размера окна
        self.setMinimumSize(900, 540)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QHBoxLayout(self.main_widget)

        # Side menu layout
        self.menu_layout = QVBoxLayout()

        # Adding the text logo to the side menu
        self.logo_label = QLabel("SignSense")
        self.logo_label.setObjectName("logo_label")

        self.menu_layout.addWidget(self.logo_label)

        # Side menu
        self.menu_list = QListWidget()
        self.menu_list.setObjectName("menu_list")
        self.menu_list.setIconSize(QSize(32, 32))

        self.add_menu_item("Обучение", "./resources/icons/Home.svg")
        self.add_menu_item("Словарь", "./resources/icons/Dictionary.svg")
        self.add_menu_item("Анализатор", "./resources/icons/View.svg")
        self.add_menu_item("Статистика", "./resources/icons/Market.svg")
        self.add_menu_item("Настройки", "./resources/icons/Setting.svg")

        self.menu_list.currentItemChanged.connect(self.display_module)

        self.menu_layout.addWidget(self.menu_list)

        # Adding the side menu layout to the main layout
        self.layout.addLayout(self.menu_layout)

        self.content_area = QWidget()
        self.content_area.setObjectName("content")
        self.layout.addWidget(self.content_area)

        # Инициализация контроллеров
        self.controllers = {
            "Обучение": LearningController(),
            "Словарь": DictionaryController(),
            "Анализатор": AnalyzerController(),
            "Статистика": StatisticsController(),
            "Настройки": SettingsController()
        }

        self.current_controller = None

    def add_menu_item(self, name, icon_path=None):
        item = QListWidgetItem(name)
        if icon_path:
            item.setIcon(QIcon(icon_path))
        self.menu_list.addItem(item)

    def display_module(self, current, previous):
        if self.current_controller is not None:
            self.current_controller.view.hide()

        self.current_controller = self.controllers[current.text()]
        self.layout.addWidget(self.current_controller.view)
        self.current_controller.view.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Загрузка и применение стилей
    with open("resources/styles/styles.qss", "r", encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

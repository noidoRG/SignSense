# modules/main_window.py

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from modules.learning import Learning
from modules.dictionary import Dictionary
from modules.analyzer import Analyzer
from modules.statistics import Statistics
from modules.settings import Settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SignSense")
        self.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        self.setMinimumSize(900, 540)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QHBoxLayout(self.main_widget)

        self.menu_layout = QVBoxLayout()

        # Изменение для использования изображения логотипа
        self.logo_label = QLabel()
        self.logo_label.setObjectName("logo_label")
        pixmap = QPixmap("./resources/icons/full_logo.svg")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_layout.addWidget(self.logo_label)

        self.menu_list = QListWidget()
        self.menu_list.setObjectName("menu_list")
        self.menu_list.setIconSize(QSize(32, 32))

        self.add_menu_item("Обучение", "./resources/icons/Home.svg")
        self.add_menu_item("Словарь", "./resources/icons/Dictionary.svg")
        self.add_menu_item("Анализатор", "./resources/icons/Analyzer.svg")
        self.add_menu_item("Статистика", "./resources/icons/Market.svg")
        self.add_menu_item("Настройки", "./resources/icons/Setting.svg")
        self.add_menu_item("Выход", "./resources/icons/Quit.svg")

        self.menu_list.currentItemChanged.connect(self.display_module)

        self.menu_layout.addWidget(self.menu_list)
        self.layout.addLayout(self.menu_layout)

        self.learning = Learning()
        self.dictionary = Dictionary()
        self.analyzer = Analyzer()
        self.statistics = Statistics()
        self.settings = Settings()

        self.modules = {
            "Обучение": self.learning,
            "Словарь": self.dictionary,
            "Анализатор": self.analyzer,
            "Статистика": self.statistics,
            "Настройки": self.settings
        }

        self.current_module = None

        self.settings.learnt_reset.connect(self.statistics.update_statistics)
        self.settings.mastered_reset.connect(self.statistics.update_statistics)
        self.learning.gesture_learnt.connect(self.statistics.update_statistics)

        self.select_default_item()  # Выбираем элемент списка по умолчанию

    def add_menu_item(self, name, icon_path=None):
        item = QListWidgetItem(name)
        if icon_path:
            item.setIcon(QIcon(icon_path))
        self.menu_list.addItem(item)

    def display_module(self, current, previous):
        if self.current_module is not None:
            if isinstance(self.current_module, Analyzer):
                self.current_module.stop_video()
            self.layout.removeWidget(self.current_module)
            self.current_module.hide()

        if current.text() == "Выход":
            self.close()
            return

        self.current_module = self.modules[current.text()]
        self.layout.addWidget(self.current_module)
        self.current_module.show()
        if isinstance(self.current_module, Analyzer):
            self.current_module.start_video()

    def select_default_item(self):
        self.menu_list.setCurrentRow(0)  # Выбираем первый элемент (Обучение)
        self.display_module(self.menu_list.currentItem(), None)  # Отображаем модуль обучения


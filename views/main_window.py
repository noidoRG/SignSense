# views/main_window.py

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from views.learning_view import LearningView
from views.dictionary_view import DictionaryView
from views.analyzer_view import AnalyzerView
from views.statistics_view import StatisticsView
from views.settings_view import SettingsView

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

        self.logo_label = QLabel("SignSense")
        self.logo_label.setObjectName("logo_label")
        self.menu_layout.addWidget(self.logo_label)

        self.menu_list = QListWidget()
        self.menu_list.setObjectName("menu_list")
        self.menu_list.setIconSize(QSize(32, 32))

        self.add_menu_item("Обучение", "./resources/icons/Home.svg")
        self.add_menu_item("Словарь", "./resources/icons/Dictionary.svg")
        self.add_menu_item("Анализатор", "./resources/icons/View.svg")
        self.add_menu_item("Статистика", "./resources/icons/Market.svg")
        self.add_menu_item("Настройки", "./resources/icons/Setting.svg")
        self.add_menu_item("Выход", "./resources/icons/Quit.svg")

        self.menu_list.currentItemChanged.connect(self.display_module)

        self.menu_layout.addWidget(self.menu_list)
        self.layout.addLayout(self.menu_layout)

        self.learning_view = LearningView()
        self.dictionary_view = DictionaryView()
        self.analyzer_view = AnalyzerView()
        self.statistics_view = StatisticsView()
        self.settings_view = SettingsView()

        self.modules = {
            "Обучение": self.learning_view,
            "Словарь": self.dictionary_view,
            "Анализатор": self.analyzer_view,
            "Статистика": self.statistics_view,
            "Настройки": self.settings_view
        }

        self.current_module = None

        self.settings_view.learnt_reset.connect(self.statistics_view.update_statistics)
        self.settings_view.mastered_reset.connect(self.statistics_view.update_statistics)
        self.learning_view.gesture_learnt.connect(self.statistics_view.update_statistics)

    def add_menu_item(self, name, icon_path=None):
        item = QListWidgetItem(name)
        if icon_path:
            item.setIcon(QIcon(icon_path))
        self.menu_list.addItem(item)

    def display_module(self, current, previous):
        if self.current_module is not None:
            if isinstance(self.current_module, AnalyzerView):
                self.current_module.stop_video()
            self.layout.removeWidget(self.current_module)
            self.current_module.hide()

        if current.text() == "Выход":
            self.close()
            return

        self.current_module = self.modules[current.text()]
        self.layout.addWidget(self.current_module)
        self.current_module.show()
        if isinstance(self.current_module, AnalyzerView):
            self.current_module.start_video()

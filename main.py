import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from modules.learning_module import LearningModule
from modules.dictionary_module import DictionaryModule
from modules.analyzer_module import AnalyzerModule
from modules.statistics_module import StatisticsModule
from modules.settings_module import SettingsModule

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
        
        # Adding the logo to the side menu
        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("./resources/icons/full_logo.svg").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.menu_layout.addWidget(self.logo_label)
        
        # Side menu
        self.menu_list = QListWidget()
        self.menu_list.setIconSize(QSize(32, 32))
        
        self.add_menu_item("Обучение", "./resources/icons/Home_black.svg")
        self.add_menu_item("Словарь", "./resources/icons/Dictionary_black.svg")
        self.add_menu_item("Анализатор", "./resources/icons/View_black.svg")
        self.add_menu_item("Статистика", "./resources/icons/Market_black.svg")
        self.add_menu_item("Настройки", "./resources/icons/Setting_black.svg")
        
        self.menu_list.currentItemChanged.connect(self.display_module)
        
        self.menu_layout.addWidget(self.menu_list)
        
        # Adding the side menu layout to the main layout
        self.layout.addLayout(self.menu_layout)
        
        self.content_area = QWidget()
        self.content_area.setObjectName("content")
        self.layout.addWidget(self.content_area)
        
        self.modules = {
            "Обучение": LearningModule(),
            "Словарь": DictionaryModule(),
            "Анализатор": AnalyzerModule(),
            "Статистика": StatisticsModule(),
            "Настройки": SettingsModule()
        }
        
        self.current_module = None
    
    def add_menu_item(self, name, icon_path=None):
        item = QListWidgetItem(name)
        if icon_path:
            item.setIcon(QIcon(icon_path))
        self.menu_list.addItem(item)
    
    def display_module(self, current, previous):
        if self.current_module is not None:
            self.layout.removeWidget(self.current_module)
            self.current_module.hide()
        
        self.current_module = self.modules[current.text()]
        self.layout.addWidget(self.current_module)
        self.current_module.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Загрузка и применение стилей
    with open("resources/styles/styles.qss", "r", encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

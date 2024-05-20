import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget
from modules.learning_module import LearningModule
from modules.dictionary_module import DictionaryModule
from modules.analyzer_module import AnalyzerModule
from modules.statistics_module import StatisticsModule
from modules.settings_module import SettingsModule

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SignSense")
        
        # Установка минимального размера окна
        self.setMinimumSize(900, 540)
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        self.layout = QVBoxLayout()
        
        # Side menu
        self.menu_list = QListWidget()
        self.menu_list.addItems(["Обучение", "Словарь", "Анализатор", "Статистика", "Настройки"])
        self.menu_list.currentItemChanged.connect(self.display_module)
        
        self.layout.addWidget(self.menu_list)
        
        self.main_widget.setLayout(self.layout)
        
        self.modules = {
            "Обучение": LearningModule(),
            "Словарь": DictionaryModule(),
            "Анализатор": AnalyzerModule(),
            "Статистика": StatisticsModule(),
            "Настройки": SettingsModule()
        }
        
        self.current_module = None
    
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



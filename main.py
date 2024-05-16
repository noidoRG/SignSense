from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar, QStackedWidget
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QTimer


from widgets.training_widget import TrainingWidget
from widgets.test_widget import TestWidget
from widgets.sandbox_widget import SandboxWidget
from widgets.translator_widget import TranslatorWidget
from widgets.stats_settings_widget import StatsSettingsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SignSense")
        
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        self.training_widget = TrainingWidget()
        self.test_widget = TestWidget()
        self.sandbox_widget = SandboxWidget()
        self.translator_widget = TranslatorWidget()
        self.stats_settings_widget = StatsSettingsWidget()
        
        self.central_widget.addWidget(self.training_widget)
        self.central_widget.addWidget(self.test_widget)
        self.central_widget.addWidget(self.sandbox_widget)
        self.central_widget.addWidget(self.translator_widget)
        self.central_widget.addWidget(self.stats_settings_widget)
        

        self.create_toolbars()
        
        self.show()


    def create_toolbars(self):
        tool_bar = QToolBar("Main Toolbar")
        
        training_action = QAction("Обучение", self)
        test_action = QAction("Проверка", self)
        analysis_action = QAction("Анализатор", self)
        stats_action = QAction("Статистика", self)
        
        training_action.triggered.connect(self.show_training)
        test_action.triggered.connect(self.show_test)
        analysis_action.triggered.connect(self.show_sandbox)
        stats_action.triggered.connect(self.show_stats_settings)
        
        tool_bar.addAction(training_action)
        tool_bar.addAction(test_action)
        tool_bar.addAction(analysis_action)
        tool_bar.addAction(stats_action)
        
        self.addToolBar(tool_bar)
    
    def show_training(self):
        self.central_widget.setCurrentWidget(self.training_widget)
    
    def show_test(self):
        self.central_widget.setCurrentWidget(self.test_widget)
    
    def show_sandbox(self):
        self.central_widget.setCurrentWidget(self.sandbox_widget)
    
    def show_translator(self):
        self.central_widget.setCurrentWidget(self.translator_widget)
    
    def show_stats_settings(self):
        self.central_widget.setCurrentWidget(self.stats_settings_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

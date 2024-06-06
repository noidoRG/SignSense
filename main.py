# main.py

import sys
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Загрузка и применение стилей
    with open("resources/styles/styles.qss", "r", encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

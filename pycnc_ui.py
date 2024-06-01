import sys
from PyQt6.QtWidgets import QApplication
from ui.home import Ui_MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = Ui_MainWindow()
    splash.show()
    sys.exit(app.exec())
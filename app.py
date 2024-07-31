import sys
from PyQt5.QtWidgets import QApplication
from ui import TranslatorApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TranslatorApp()
    sys.exit(app.exec_())
from app import WeatherEnt_App
from PyQt5.QtWidgets import QApplication
import sys


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wea = WeatherEnt_App()
    wea.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

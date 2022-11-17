import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from wheatherent_design import Ui_MainWindow
from Weather import get_weather
from threading import Thread
from setting import Settings_Wind
import keyboard
import time
from plyer import notification

RU = ['Найти', 'Город:', 'Погода:', 'Температура (На данный момент):', 'Скорость ветра:',
      'м/c', 'Влажность:', 'Давление:', 'Па', 'Такой город не найден',
      {'Mon': 'Пн', 'Tue': 'Вт', 'Wed': 'Ср', 'Thu': 'Чт', 'Fri': 'Пт', 'Sat': 'Сб', 'Sun': 'Вс'},
      {'Jan': 'Янв', 'Feb': 'Февр', 'Mar': 'Март', 'Apr': 'Апр', 'May': 'Май', 'Jun': 'Июнь',
       'Jul': 'Июль', 'Aug': 'Авг', 'Sep': 'Сент', 'Oct': 'Октб', 'Nov': 'Нояб', 'Dec': 'Дек'}]

ENG = ['Find', 'City:', 'Weather:', 'Temperature (At the moment):', 'Wind speed:',
       'meters/second', 'Humidity:', 'Pressure:', 'hPa', 'No such city has been found']


class WeatherEnt_App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setup_app()
        self.add_funcs_to_buttons()
        self.app_is_working = True
        self.API_TOKEN = '02464cacce159f7ad880a65e11890f17'

        self.hotkey = keyboard.add_hotkey('Ctrl+Alt+W', self.show_notification)
        self.time_between_not = 0

        th = Thread(target=self.get_time)
        th.start()

    def setup_app(self):
        f = open('app_settings.txt', 'r')
        data = f.read().split('\n')
        f.close()

        lang = data[0][6:]
        theme = data[2][7:]
        keyboard_shortcut = data[3][32:]
        self.choosen_city = data[5][14:]

        if keyboard_shortcut == 'False':
            self.keyboard_shortcut = False
        else:
            self.keyboard_shortcut = True

        self.translate_app(lang)
        if theme == 'dark':
            self.set_theme(QColor(0, 0, 0))

    def translate_app(self, language):
        if language == 'ru':
            self.language = RU
        else:
            self.language = ENG

        self.search_button.setText(self.language[0])
        self.CITY_LBL.setText(self.language[1])
        self.WHEATHER_LBL.setText(self.language[2])
        self.TEMP_LBL.setText(self.language[3])
        self.WIND_LBL.setText(self.language[4])
        self.HUMIDITY_LBL.setText(self.language[6])
        self.PRESSURE_LBL.setText(self.language[7])

    def set_theme(self, theme):
        if theme != QColor(255, 255, 255):
            self.setStyleSheet(f'background-color: rgb(25, 25, 25)')
            self.time_lbl.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.error_lbl.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.city_entry.setStyleSheet(f'background-color: rgb(255, 255, 255)')
            self.search_button.setStyleSheet(f'background-color: rgb(255, 255, 255)')
            self.CITY_LBL.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.WHEATHER_LBL.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.TEMP_LBL.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.WIND_LBL.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.HUMIDITY_LBL.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.PRESSURE_LBL.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.name_of_city_lbl.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.weather_lbl.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.temp_lbl.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.wind_speed_lbl.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.humidity_lbl.setStyleSheet(f'color: rgb(255, 255, 255)')
            self.pressure_lbl.setStyleSheet(f'color: rgb(255, 255, 255)')

    def add_funcs_to_buttons(self):
        self.close_btn.clicked.connect(self.close_app)
        self.search_button.clicked.connect(self.find_weather)
        self.settings_but.clicked.connect(self.open_settings)

    def close_app(self):
        self.app_is_working = False
        self.close()

    def get_time(self):
        while True:
            t = time.ctime(time.time())

            day_of_week = t[:3]
            day_of_month = t[8:10]
            month = t[4:7]
            now_time = t[11:16]
            if self.language == RU:
                self.time_lbl.setText(f'{now_time}, {self.language[-2][day_of_week]} '
                                      f'{day_of_month} {self.language[-1][month]}')
            else:
                self.time_lbl.setText(f'{now_time} {day_of_week} {day_of_month} {month}')
            time.sleep(1)
            if self.time_between_not > 0:
                self.time_between_not -= 1

            if not self.app_is_working:
                break

    def find_weather(self):
        city = self.city_entry.text()
        data = get_weather(city, self.API_TOKEN)
        try:
            name_of_city = data['name']
            type_of_weather = data['weather'][0]['description']
            temp = data['main']['temp']
            wind_speed = data['wind']['speed']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']

            self.error_lbl.setText('')
            self.name_of_city_lbl.setText(str(name_of_city))
            self.weather_lbl.setText(str(type_of_weather).capitalize())
            self.temp_lbl.setText(str(round(temp, 1)) + '°C')
            self.wind_speed_lbl.setText(str(round(wind_speed, 1)) + f' {self.language[5]}')
            self.humidity_lbl.setText(str(humidity) + '%')
            self.pressure_lbl.setText(str(pressure) + f' {self.language[8]}')

        except TypeError:
            self.error_lbl.setText(f'{self.language[9]}')
            self.name_of_city_lbl.setText('-')
            self.weather_lbl.setText('-')
            self.temp_lbl.setText('-')
            self.wind_speed_lbl.setText('-')
            self.humidity_lbl.setText('-')
            self.pressure_lbl.setText('-')

    def open_settings(self):
        a = Settings_Wind()
        a.exec()

    def show_notification(self):
        if self.time_between_not == 0 and self.keyboard_shortcut:
            try:
                weather = get_weather(self.choosen_city, self.API_TOKEN)

                temp = weather['main']['temp']
                wind_speed = weather['wind']['speed']
                weather_id = int(weather['weather'][0]['id'])
                if 200 <= weather_id < 300:
                    icon = 'thunderstorm'
                elif 300 <= weather_id < 400 or 520 <= weather_id <= 531:
                    icon = 'shower-rain'
                elif 500 <= weather_id <= 504:
                    icon = 'rain'
                elif weather_id == 511 or 600 <= weather_id < 700:
                    icon = 'snow'
                elif 700 <= weather_id < 800:
                    icon = 'mist'
                elif weather_id == 800:
                    icon = 'clear-sky'
                elif weather_id == 801:
                    icon = 'few-clouds'
                elif weather_id == 802:
                    icon = 'scattered-clouds'
                else:
                    icon = 'broken-clouds'

                notification.notify(title='WhetherEnt', message=f'{self.language[3][:11]}: {temp}° '
                                                                f'\n{self.language[4]} {wind_speed} {self.language[5]}',
                                    app_icon=f'{icon}.ico')
                self.time_between_not = 10
            except Exception:
                pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return

        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wea = WeatherEnt_App()
    wea.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())

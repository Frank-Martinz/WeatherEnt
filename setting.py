import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor
from settings_design import Ui_Settings
from Weather import get_coords


RU = ['Язык:', 'Тип градусов:', ['Цельсий', 'Фаренгейт', 'Кельвин'], 'Тема:', ['Светлая', 'Тёмная'],
      'Отправка уведомлений по нажатию сочетаний клавиш', 'Сочетание клавиш: CTRL + ALT + W',
      '- Город, информацию о котором вы хотите получать', 'Изменить', 'Принять изменения', 'Такого города нет!']

ENG = ['Language:', 'Type of degrees', ['Celsius', 'Fahrenheit', 'Kelvin'], 'Theme:', ['Light', 'Dark'],
       'Sending notifications by pressing keyboard shortcuts', 'Keyboard shortcut: CTRL + ALT + W',
       '- The city you want to receive information about', 'Change', 'Accept changes', 'There is no such city!']


class Settings_Wind(QDialog, Ui_Settings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setup_wind()
        self.add_funcs()
        self.API_TOKEN = '02464cacce159f7ad880a65e11890f17'

    def add_funcs(self):
        self.close_btn.clicked.connect(self.close_dial)
        self.commit_btn.clicked.connect(self.accept_changes)
        self.change_btn.clicked.connect(self.change_city)
        self.on_or_off_message_btn.clicked.connect(self.turn_on_off_keyboard_shortcut)

    def close_dial(self):
        self.close()

    def setup_wind(self):
        f = open('app_settings.txt', 'r')
        data = f.read().split('\n')

        lang = data[0][6:]
        degree = data[1][6:]
        theme = data[2][7:]
        keyboard_shortcut = data[3][32:]
        choosen_city = data[5][14:]

        self.kbd_shrtct = data[4][19:]

        self.set_language(lang)
        self.set_theme(QColor(255, 255, 255) if theme == 'light' else QColor(0, 0, 0))
        if keyboard_shortcut == 'False':
            self.keyboard_shortcut_bool = False
            self.turn_on_off_keyboard_shortcut()
        else:
            self.keyboard_shortcut_bool = True
            self.on_or_off_message_btn.setChecked(True)

        self.lang_combobox.setCurrentText('Русский' if lang == 'ru' else 'English')
        if degree == 'metric':
            self.degree_combobox.setCurrentText('Цельсий' if lang == 'ru' else 'Celsius')
        elif degree == 'imperial':
            self.degree_combobox.setCurrentText('Фаренгейт' if lang == 'ru' else 'Fahrenheit')
        else:
            self.degree_combobox.setCurrentText('Кельвин' if lang == 'ru' else 'Kelvin')
        if theme == 'light':
            self.theme_combobox.setCurrentText('Светлая' if lang == 'ru' else 'Light')
        else:
            self.theme_combobox.setCurrentText('Тёмная' if lang == 'ru' else 'Dark')

        self.city_entry.setText(choosen_city)

    def accept_changes(self):
        f = open('app_settings.txt', 'w')
        lang = self.lang_combobox.currentText()
        degree = self.degree_combobox.currentText()
        if degree == 'Цельсий' or degree == 'Celsius':
            degree = 'metric'
        elif degree == 'Фаренгейт' or degree == 'Fahrenheit':
            degree = 'imperial'
        else:
            degree = 'standart'

        theme = self.theme_combobox.currentText()
        if theme == 'Светлая' or theme == 'Light':
            theme = 'light'
        else:
            theme = 'dark'

        city = self.city_entry.text()
        if 'Error' in get_coords(city, self.API_TOKEN) and self.keyboard_shortcut_bool:
            f.write(f'lang: {"ru" if lang == "Русский" else "eng"}\n'
                    f'temp: {degree}\n'
                    f'theme: {theme}\n'
                    f'keyboard shortcut (True/False): False\n'
                    f'keyboard shortcut: \n'
                    f'choosen_city: ')
            f.close()
            self.error_lbl.setText(self.language[10])
            self.city_entry.setText('')
            return False

        f.write(f'lang: {"ru" if lang == "Русский" else "eng"}\n'
                f'temp: {degree}\n'
                f'theme: {theme}\n'
                f'keyboard shortcut (True/False): {self.keyboard_shortcut_bool}\n'
                f'keyboard shortcut: CTRL+ALT+W\n'
                f'choosen_city: {city}')

        f.close()

    def set_language(self, language):
        if language == 'ru':
            self.language = RU
        else:
            self.language = ENG

        self.lang_lbl.setText(self.language[0])
        self.type_of_degrees.setText(self.language[1])
        for item in range(3):
            self.degree_combobox.removeItem(0)
        self.degree_combobox.insertItems(0, self.language[2])
        self.theme_lbl.setText(self.language[3])
        for item in range(2):
            self.theme_combobox.removeItem(0)
        self.theme_combobox.insertItems(0, self.language[4])
        self.on_or_off_message_btn.setText(self.language[5])
        self.keyboard_shortcut.setText(self.language[6])
        self.city_lbl.setText(self.language[7])
        self.change_btn.setText(self.language[8])
        self.commit_btn.setText(self.language[9])

    def set_theme(self, theme):
        if theme != QColor(255, 255, 255):
            self.setStyleSheet(f'background-color: rgb(50, 50, 50)')
            self.lang_lbl.setStyleSheet('color: rgb(200, 200, 200)')
            self.lang_combobox.setStyleSheet('background-color: rgb(200, 200, 200)')
            self.type_of_degrees.setStyleSheet('color: rgb(200, 200, 200)')
            self.degree_combobox.setStyleSheet('background-color: rgb(200, 200, 200)')
            self.theme_lbl.setStyleSheet('color: rgb(200, 200, 200)')
            self.theme_combobox.setStyleSheet('background-color: rgb(200, 200, 200)')
            self.on_or_off_message_btn.setStyleSheet('color: rgb(200, 200, 200)')
            self.keyboard_shortcut.setStyleSheet('color: rgb(200, 200, 200)')
            self.city_entry.setStyleSheet('background-color: rgb(200, 200, 200)')
            self.city_lbl.setStyleSheet('color: rgb(200, 200, 200)')
            self.change_btn.setStyleSheet('background-color: rgb(200, 200, 200)')
            self.commit_btn.setStyleSheet('background-color: rgb(200, 200, 200)')
            self.error_lbl.setStyleSheet('color: rgb(200, 200, 200)')

    def turn_on_off_keyboard_shortcut(self):
        self.keyboard_shortcut_bool = self.on_or_off_message_btn.isChecked()
        self.keyboard_shortcut.setDisabled(not self.keyboard_shortcut_bool)
        self.city_entry.setDisabled(not self.keyboard_shortcut_bool)
        self.city_lbl.setDisabled(not self.keyboard_shortcut_bool)
        self.change_btn.setDisabled(not self.keyboard_shortcut_bool)

    def change_city(self):
        self.error_lbl.setText('')
        city = self.city_entry.text()
        lat, lon = get_coords(city, self.API_TOKEN)
        if lat == lon == 'Error':
            self.error_lbl.setText(self.language[10])
            self.city_entry.setText('')

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
    stg = Settings_Wind()
    stg.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
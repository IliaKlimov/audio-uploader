"""
    Программа для загрузки mp3 аудиозаписей на сервер POST запросом
    поддерживает парсинг даты и имя спикера из имени файла (формат файла "DD.MM.YY SPEAKER.mp3")
    Интерфейс на QT (PySide2)
"""
import json
import re
import sys

import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from PySide2 import QtCore, QtGui, QtWidgets

from ui import Ui_Dialog

TESTING_MODE = False
PIDS_FILE = "pids.txt"  # Файл с id
URL = "http://httpbin.org/post"
API_KEY = "nope"


# Вызов файлового диалога и его regex-обработка для автозаполнения
def parse_file():
    file = QtWidgets.QFileDialog.getOpenFileName(dir=file_dir, filter="mp3 file (*.mp3)")[0]
    ui.fileTextLine.setText(file)
    regex = re.search(r"(\d\d)\.(\d\d)\.\d?\d?(\d\d) *(\w+)?.mp3$", file)
    if regex is not None:
        print("Parsed dd={} mm={} yy={} speaker={}".format(*regex.groups()))
        dd, mm, yy, speaker = regex.groups()
        ui.DateTextLine.setText("{}.{}.20{}".format(dd, mm, yy))

        # Автоматический выбор  из списка если он указан в имени файла.
        if speaker is not None:
            for el in [ui.comboBox.itemText(i) for i in range(ui.comboBox.count())]:
                if el.startswith(speaker):
                    ui.comboBox.setCurrentText(el)
                    print("Find Speaker: " + el)
                    break
    else:
        ui.DateTextLine.setText("")


# Составление словаря из файла в формате - "value key" -> {key:value}. В данном случае "ID ИмяСпикера"
def setDictFromFile(file, pids_dict):
    with open(file, encoding="utf8") as f:
        for spl in f.read().splitlines():
            pid, name = spl.split(" ", maxsplit=1)
            pids_dict[name] = int(pid)


def get_newest_list(URL):
    r = requests.get(URL, params={"authors": 1})
    dict = json.loads(r.text)
    dict = {el['speaker']: el['id'] for el in dict}
    return dict


def setListSpeakers(pids_dict):
    try:
        pids_dict = get_newest_list(URL)
    except Exception:
        ui.fileTextLine.setText(f"No connection or wrong settings")
        setDictFromFile(PIDS_FILE, pids_dict)
        print("Pids loaded from file")
    for el in pids_dict:
        ui.comboBox.addItem(el, userData=pids_dict[el])


# Создание отдельного потока для загрузки файла на сервер. Необходимо для того, чтобы главное окно не фризилось при загрузке.
class UploadThread(QtCore.QThread):
    def __init__(self, send_file, params):
        QtCore.QThread.__init__(self)
        self.send_file = send_file
        self.params = params

    def run(self):
        ui.fileTextLine.setText("Загрузка..")
        ui.pushButton.setEnabled(False)
        try:
            # r = requests.post(URL, files=self.send_file, data=self.params)
            r = requests.post(URL, data=self.params, headers={'Content-Type': self.params.content_type})
        except Exception as e:
            ui.fileTextLine.setText(f"Что-то тут не так( {e}", )
        else:
            print("Status code", r.status_code)
            print(r.text)
            with open('output.txt', 'wb') as f:
                f.write(r.content)
            ui.fileTextLine.setText("Готово!")
        finally:
            ui.pushButton.setEnabled(True)

#Прогресс загрузки в процентах
def create_callback(encoder, f_output=print):
    encoder_len = encoder.len

    def callback(monitor):
        percent = monitor.bytes_read * 1e2 / encoder_len
        f_output("{percent:3.0f}%".format(percent=percent))

    return callback


def upload():
    file = ui.fileTextLine.text()
    date = ui.DateTextLine.text()

    # Обработка пустых значений файла или даты
    if not file:
        ui.msgBox.setText("Укажи файл!")
        ui.msgBox.exec()
        print("ERROR - file not selected")
        return
    if not date:
        ui.msgBox.setText("Укажи дату!")
        ui.msgBox.exec()
        print("ERROR - date not entered")
        return
    regex = re.search(r"(\d\d)\.(\d\d)\.(?:\d\d|)(\d\d)$", date)
    if regex is None:
        ui.msgBox.setText("Ты правильно ввел дату?")
        ui.msgBox.exec()
        print("ERROR - date is not correct")
        return

    dd, mm, yy = regex.groups()
    speakerid = ui.comboBox.currentData()
    print(dd, mm, yy, speakerid)
    filename = "{}.{}.{}.mp3".format(yy, mm, dd)

    # it = upload_in_chunks("pids.txt", ui.fileTextLine.setText, 10)

    # send_file = {'file': (filename, IterableToFileAdapter(it), 'audio/mp3')}
    send_file = {'file': (filename, open(file, "rb"), 'audio/mp3')}
    encoder = MultipartEncoder({
        "api_key": API_KEY,
        "pid": str(speakerid),
        "date": "20{}-{}-{}".format(yy, mm, dd),
        'file': (filename, open(file, "rb"), 'audio/mp3'),
    })
    callback = create_callback(encoder, ui.fileTextLine.setText)
    monitor = MultipartEncoderMonitor(encoder, callback)
    print(f"Отправляю файл под именем '{filename}',\npid: {speakerid}")

    ui.thread = UploadThread(send_file, monitor)
    ui.thread.start()


if __name__ == "__main__":
    # UI setup
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QMainWindow()
    Dialog.setWindowIcon(QtGui.QIcon('favicon.png'))
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    print("UI is valid")
    file_dir = "."

    if not TESTING_MODE:
        try:
            from settings import *
        except ImportError:
            ui.fileTextLine.setText("settings.py not found")
            print("Settings not found")

    pids_dict = {}
    setListSpeakers(pids_dict)
    print("List ok")

    # Выбор 23 id "по умолчанию"
    ui.comboBox.setCurrentIndex(ui.comboBox.findData(23))


    ui.fileButton.clicked.connect(parse_file)
    ui.pushButton.clicked.connect(upload)

    Dialog.show()
    print("Show UI")
    sys.exit(app.exec_())
    input()

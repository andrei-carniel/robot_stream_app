# This is a sample Python script.
import sys
import threading
import time

from PyQt5.QtWidgets import QApplication, QMainWindow

from udp_broadcast import UDP_Broadcast_Threaded_Class
from ui_mainwindow import Ui_MainWindow

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Compile the interface:
# pip install pyuic5-tool
# pyuic5 -x mainwindow.ui -o ui_mainwindow.py

# thread variables
thread_broadcast = None
receiving_broadcast = True

# lists to store data
list_devices = []




class MainWindow:

    def __init__(self):
        global thread_broadcast

        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        thread_broadcast = UDP_Broadcast_Threaded_Class()

        # Inicia a thread
        thread_broadcast.start_thread()

        x = threading.Thread(target=thread_function)
        x.start()

        # self.ui.lv_device.clicked.connect(self.on_list_devices_clicked)
        # self.ui.lv_cam.clicked.connect(self.on_list_cam_clicked)
        # self.ui.lv_control.clicked.connect(self.on_list_control_clicked)
        # self.ui.bt_connect.clicked.connect(self.on_button_connect_clicked)

    def show(self):
        self.main_win.show()

def thread_function():
    global thread_broadcast, receiving_broadcast

    # Loop principal para pegar os dados da thread
    try:
        while receiving_broadcast:
            data = thread_broadcast.get_data()
            if data:
                print(f"Recebido: {data}")

            time.sleep(1)
    finally:
        # Encerra a thread ao final
        thread_broadcast.stop_thread()

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_win = MainWindow()
#     main_win.show()
#
#
#     sys.exit(app.exec_())

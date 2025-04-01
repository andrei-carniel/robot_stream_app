# This is a sample Python script.
import sys
import threading
import time

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem

from cam.connect_cam import Connect_cam
from udp.udp_bcast import DataReceiver
from udp.udp_client import UdpClient
from ui_mainwindow import Ui_MainWindow
import pygame
from pygame.locals import *

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Compile the interface:
# pip install pyuic5-tool
# pyuic5 -x mainwindow.ui -o ui_mainwindow.py

# thread variables
thread_broadcast = None
receiving_broadcast = True
thread_control = None

# variáveis apra controlar o envio de mensagens
BROADCAST_PORT = 10006;
SERVER_UDP_IP = 0;
SERVER_UDP_PORT = 0;
BUFFER_SIZE = 1024;
CONTROL_KEY = "wickedbotz";


device_list = [] # Lista de devices
joystick_list = []# Lista de joysticks

class MainWindow:

    def __init__(self):
        global thread_broadcast

        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        # self.ui.lv_device.clicked.connect(self.on_list_devices_clicked)
        # self.ui.lv_cam.clicked.connect(self.on_list_cam_clicked)
        # self.ui.lv_control.clicked.connect(self.on_list_control_clicked)
        self.ui.bt_connect.clicked.connect(self.on_button_connect_clicked)

        # Inicia a thread para receber dados via UDP
        self.receiver = DataReceiver(self.update_address)  # Passando self.update_address como função de callback
        self.receiver.start()

        # Inicializa o Pygame
        pygame.init()
        # Inicializa o módulo de joystick
        pygame.joystick.init()

        thread_control = threading.Thread(target=self.update_joystick_list)
        thread_control.start()

        # Garante que a thread seja finalizada ao fechar a janela
        # self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_address(self, new_device):
        global SERVER_UDP_PORT, SERVER_UDP_IP
        # Função que atualiza a tela com os novos dados
        # self.label.config(text=new_data)
        SERVER_UDP_IP = new_device.ip
        SERVER_UDP_PORT = new_device.port
        print(f"Recebido: " + new_device.ip + ":" + str(new_device.port))

        add_new_device = True

        # Verifica se o novo dispositivo já está na lista, comparando IP e porta
        for device in device_list:
            device.is_alive()
            if device.is_dead:
                device_list.remove(device)
            elif new_device.ip == device.ip and new_device.port == device.port and new_device.name == device.name:
                device.reset_time()
                add_new_device = False

        if add_new_device:
            device_list.append(new_device)

        self.update_device_list()

    def update_device_list(self):
        global device_list
        # Cria o modelo para o QListView
        self.device_model = QStandardItemModel(self.ui.lv_device)
        self.ui.lv_device.setModel(self.device_model)

        # Limpa o modelo antes de adicionar os dispositivos novamente
        self.device_model.clear()

        # Supondo que você já tenha uma lista de dispositivos que foram adicionados
        for device in device_list:
            # Cria um item para cada dispositivo
            item = QStandardItem(device.get_formated_name())
            self.device_model.appendRow(item)
    def on_close(self):
        # Para a thread ao fechar a janela
        self.receiver.stop()
        self.receiver.join()  # Espera a thread terminar

    def show(self):
        self.main_win.show()

    # inicia a thread do control de xbox
    def on_button_connect_clicked(self):
        global thread_control, BUFFER_SIZE, joystick_list, device_list

        pos_dev = self.ui.lv_device.currentIndex().row()
        pos_ctrl = self.ui.lv_control.currentIndex().row()

        if pos_dev < 0 or pos_ctrl < 0:
            print("Selecione um dispositivo e um controle para conectar.")
            # return

        thread_control = threading.Thread(target=self.control_start)
        thread_control.start()

    def control_start(self):
        global thread_broadcast, control_working
        udp_client = UdpClient(SERVER_UDP_IP, SERVER_UDP_PORT, BUFFER_SIZE)
        #camera = Connect_cam(SERVER_UDP_IP)
        print("Iniciando CAMERA...")
        #camera.run()
        print("Camera iniciada")

        # Verifica e inicializa o primeiro joystick, se houver
        joystick_count = pygame.joystick.get_count()

        if joystick_count == 0:
            print("Nenhum joystick detectado.")
            return  # Finaliza o método se não houver joystick
        else:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            print(f"Controle detectado: {joystick.get_name()}")
            print(f"Quantidade de eixos (sticks/triggers): {joystick.get_numaxes()}")
            print(f"Quantidade de botões: {joystick.get_numbuttons()}")
            print(f"Quantidade de hats (direcional): {joystick.get_numhats()}")

        control_working = True

        # Loop principal para pegar os dados da thread
        try:
            while control_working:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        control_working = False

                    # Detecta movimento dos eixos (sticks e triggers)
                    if event.type == pygame.JOYAXISMOTION:
                        # if (event.axis == 0):  # esquerda/direita direcional da esquerda, valores -1 a 1
                        # if (event.axis == 1):  # cima/baixo direcional da esquerda, valores -1 a 1
                        # if (event.axis == 2):#esquerda/direta direcional da direita, valores -1 a 1
                        # if (event.axis == 3):#cima/baixo direcional da direita, valores -1 a 1
                        # if (event.axis == 4):#triggger esquerda, valores -1 (totalmente solto) a 1 (totalmente pressionado)
                        # if (event.axis == 5):#triggger direita, valores -1 (totalmente solto) a 1 (totalmente pressionado)
                        print(f"Eixo {event.axis} valor: {event.value}")

                    # Detecta botões pressionados
                    if event.type == pygame.JOYBUTTONDOWN:
                        # 0 é A
                        # 1 é B
                        # 2 é X
                        # 3 é Y
                        # 8 é botão do joystick esquerdo
                        # 9 é botão do joystick direito

                        if event.button == 0: #101 - FRONT para frente
                            udp_client.send_message("1:102:255")
                        if event.button == 1: #104 - RIGHT para direita
                            udp_client.send_message("1:104:255")
                        if event.button == 2: #103 - LEFT para esquerda
                            udp_client.send_message("1:103:255")
                        if event.button == 3: #102 - BACK para trás
                            udp_client.send_message("1:101:255")

                        print(f"Botão {event.button} pressionado.")

                    # Detecta botões liberados
                    if event.type == pygame.JOYBUTTONUP:
                        # 0 é A
                        # 1 é B
                        # 2 é X
                        # 3 é Y
                        # 8 é botão do joystick esquerdo
                        # 9 é botão do joystick direito
                        if event.button == 0 or event.button == 1 or event.button == 2 or event.button == 3:
                            udp_client.send_message("1:100:255")

                        print(f"Botão {event.button} liberado.")

                    # Detecta movimento do direcional (hat)
                    if event.type == pygame.JOYHATMOTION:
                        # cima (0, 1), baixo (0, -1), esquerda (-1, 0), direita (1, 0)
                        print(f"Hat {event.hat} movido para: {event.value}")

        finally:
            # Encerra o socket e recursos
            udp_client.close()
            #camera.stop()
            pygame.quit()
            control_working = False

    def update_joystick_list(self):
        """Verifica e atualiza a lista de joysticks disponíveis."""
        global joystick_list, thread_control, device_list

        control_working = True

        # Loop principal para pegar os dados da thread
        try:
            while control_working:
                # Conta quantos joysticks estão conectados
                joystick_count = pygame.joystick.get_count()

                # Limpa a lista e atualiza com os joysticks disponíveis
                joystick_list.clear()

                for i in range(joystick_count):
                    joystick = pygame.joystick.Joystick(i)
                    joystick.init()
                    joystick_info = {
                        'name': joystick.get_name(),
                        'id': i,
                        'axes': joystick.get_numaxes(),
                        'buttons': joystick.get_numbuttons(),
                        'hats': joystick.get_numhats()
                    }
                    joystick_list.append(joystick_info)

                # Exibe a lista atualizada
                print("Lista de Joysticks Atualizada:")

                # Cria o modelo para o QListView
                self.control_model = QStandardItemModel(self.ui.lv_control)
                self.ui.lv_control.setModel(self.control_model)

                # Limpa o modelo antes de adicionar os dispositivos novamente
                self.control_model.clear()

                # Supondo que você já tenha uma lista de dispositivos que foram adicionados
                for js in joystick_list:
                    # Cria um item para cada dispositivo
                    # Converte o dicionário para uma string formatada
                    joystick_info_str = f"Joystick {js['id']}: {js['name']} - Eixos: {js['axes']}, Botões: {js['buttons']}, Hats: {js['hats']}"

                    item = QStandardItem(joystick_info_str)
                    self.control_model.appendRow(item)

                time.sleep(5)  # Verifica a cada 5 segundos (ajuste o intervalo conforme necessário)
        finally:
            # Encerra a thread ao final
            control_working = False
            print("Thread encerrada")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()

    sys.exit(app.exec_())

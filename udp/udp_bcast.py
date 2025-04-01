import threading
import socket
import time

from object.bcast_udp import BcastUdp

BROADCAST_PORT = 10006;
SERVER_UDP_IP = 0;
SERVER_UDP_PORT = 0;
BUFFER_SIZE = 1024;
CONTROL_KEY = "wickedbotz";

sock_client = None
sock_server = None

# Classe que recebe dados via UDP em uma thread separada
class DataReceiver(threading.Thread):
    def __init__(self, update_func, udp_ip="127.0.0.1", udp_port=5005):
        super().__init__()
        global sock_client
        self.update_func = update_func  # Função para atualizar a interface
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.running = True
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.bind((self.udp_ip, self.udp_port))
        # Cria um socket UDP
        sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # permite a reutilização de socket
        sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # configura socket para escutar no broad cast
        sock_client.bind(('', BROADCAST_PORT))
        print("Escutando broadcast na porta", BROADCAST_PORT)

    def run(self):
        # Loop para receber dados UDP
        global sock_client, BROADCAST_PORT, SERVER_UDP_IP, SERVER_UDP_PORT, BUFFER_SIZE, CONTROL_KEY

        # Recebe pacotes em broadcast
        while self.running:
            data, addr = sock_client.recvfrom(BUFFER_SIZE) #já bloqueia a thread até que um pacote seja recebido.
            # print("Recebido de", addr, ":", data.decode())

            if data:
                decoded_data = data.decode('utf-8')  # Decodifica os dados recebidos
                ip_info = decoded_data.split(':')

                if (ip_info[0] == CONTROL_KEY):
                    SERVER_UDP_IP = str(ip_info[1])
                    SERVER_UDP_PORT = int(ip_info[2])
                    robot_name = str(ip_info[3])

                    # print("IP: ", SERVER_UDP_PORT, " Porta: ", SERVER_UDP_PORT)
                    data = BcastUdp(SERVER_UDP_IP, SERVER_UDP_PORT, robot_name)

                    # Envia para a classe principal os dados filtrados
                    self.update_func(data)

            # Espera 1 segundo antes de gerar mais dados
            time.sleep(1)

    def stop(self):
        self.running = False
        self.sock.close()  # Fecha o socket UDP ao encerrar a thread
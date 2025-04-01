import queue
import socket
import time
import threading
from queue import Queue


BROADCAST_PORT = 10006;
SERVER_UDP_IP = 0;
SERVER_UDP_PORT = 0;
BUFFER_SIZE = 1024;
CONTROL_KEY = "wickedbotz";

sock_client = None
sock_server = None


def send_message_to_server():
    global sock_server, SERVER_UDP_IP, SERVER_UDP_PORT, BUFFER_SIZE;

    # Cria um socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "UP - pressed"

    for x in range (10):
        # time.sleep(1)
        # Envia uma mensagem para o ESP32
        message = message + " -> " + str(x)
        sock.sendto(message.encode(), (SERVER_UDP_IP, SERVER_UDP_PORT))
        print(f"Mensagem {message} enviada para {SERVER_UDP_IP}:{SERVER_UDP_PORT}")

    message = "UP - released"

    # Fecha o socket
    sock.close()


class UDP_Broadcast_Threaded_Class:
    def __init__(self):
        # Inicializa a fila para armazenar dados retornados pela thread
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.thread_task)
        self.running = False

    def start_thread(self):
        """Inicia a execução da thread."""
        self.running = True
        self.thread.start()

    def thread_task(self):
        """Tarefa a ser executada pela thread."""
        global sock_client, BROADCAST_PORT, SERVER_UDP_IP, SERVER_UDP_PORT, BUFFER_SIZE, CONTROL_KEY;

        # Cria um socket UDP
        sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # permite a reutilização de socket
        sock_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);

        # configura socket para escutar no broad cast
        sock_client.bind(('', BROADCAST_PORT))

        print("Escutando broadcast na porta", BROADCAST_PORT)
        waiting_connection = True

        # Recebe pacotes em broadcast
        while self.running:
            data, addr = sock_client.recvfrom(BUFFER_SIZE)
            # print("Recebido de", addr, ":", data.decode())

            # decode da mensagem
            message = data.decode()
            ip_info = message.split(':')

            if (ip_info[0] == CONTROL_KEY):
                SERVER_UDP_IP = ip_info[1]
                SERVER_UDP_PORT = int(ip_info[2])
                # print("IP: ", SERVER_UDP_PORT, " Porta: ", SERVER_UDP_PORT)
                data = SERVER_UDP_IP, SERVER_UDP_PORT
                # Coloca o dado na fila para ser retornado
                self.queue.put(data)
                # Espera 1 segundo antes de gerar mais dados

            time.sleep(1)


    def get_data(self):
        """Retorna dados da fila se houver, ou None se a fila estiver vazia."""
        try:
            return self.queue.get_nowait()  # Tenta pegar dados da fila sem bloquear
        except queue.Empty:
            return None  # Se a fila estiver vazia, retorna None

    def stop_thread(self):
        """Encerra a execução da thread."""
        self.running = False
        self.thread.join()  # Aguarda a thread terminar


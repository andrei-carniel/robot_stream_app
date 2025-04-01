import socket

BUFFER_SIZE = 1024;

class UdpClient:
    def __init__(self, server_ip, server_port, buffer_size=BUFFER_SIZE):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message, repeat=2):
        """
        "param1:param2:param3", exemplo "0:STOP:255"
        param1: número inteiro
        - 0 para operações com led
        - 1 para operações com o motor

        param2: número inteiro
        - 100 - STOP para parar
        - 101 - FRONT para frente
        - 102 - BACK para trás
        - 103 - LEFT para esquerda
        - 104 - RIGHT para direita
        - 105 - LIGHT para ativar luz de forma intermitente

        param3: número inteiro
        - LED >> 0 para desligar o led
        - LED >> 1 para ligar o led
        - Motor >> 0 para velocidade mínima do motor
        - Motor >> 255 para velocidade máxima do motor

        Envia a mensagem para o servidor UDP, repetindo 'repeat' vezes.
        :param message: A mensagem inicial a ser enviada.
        :param repeat: Número de repetições da mensagem.
        """
        for x in range(repeat):
            # Envia a mensagem para o servidor
            self.sock.sendto(message.encode(), (self.server_ip, self.server_port))
            print(f"Mensagem '{message}' enviada para {self.server_ip}:{self.server_port}")

    def close(self):
        """
        Fecha o socket UDP.
        """
        self.sock.close()
        print("Socket fechado.")
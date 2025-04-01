import cv2

class Connect_cam:
    def __init__(self, ip):
        self.url = "http://" + str(ip) + ":81/stream"
        self.cap = cv2.VideoCapture(self.url)
        # URL do stream de vídeo do ESP32-CAM
        #url = "http://<IP_DO_ESP>:81/stream"  # Substitua pelo IP do ESP32-CAM

    def run(self):
        # Inicia a captura de vídeo
        #cap = cv2.VideoCapture(self.url)

        if not self.cap.isOpened():
            print("Erro ao abrir o stream")
            exit()

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Falha ao receber frame")
                break

            # Exibe o frame
            cv2.imshow('ESP32-CAM', frame)

            # Sai do loop ao pressionar a tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def stop(self):
        # Libera a captura e fecha a janela
        self.cap.release()
        cv2.destroyAllWindows()

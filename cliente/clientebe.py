import socket
import PyQt5
import threading
import sys
import PyQt5.QtCore

class Cliente(PyQt5.QtCore.QObject):

    generar_conexion_signal = PyQt5.QtCore.pyqtSignal(str, int)
    mensaje_recibido_signal = PyQt5.QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.estado_conexion_signal = None
        self.mensaje_enviado_signal = None
        self.init_signals()

    
    def init_signals(self):
        self.generar_conexion_signal.connect(self.intentar_conexion)
        self.mensaje_recibido_signal.connect(self.enviar_mensaje)

    def intentar_conexion(self, host, port):
        self.host = host
        self.port = port

        self.server_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_cliente.connect((self.host, self.port))
            self.conexion()
        except:
            self.estado_conexion_signal.emit(False)
            self.cerrar_conexion()
        
    def conexion(self):
        self.estado_conexion_signal.emit(True)
        self.thread = threading.Thread(target=self.recibir_mensaje, args=(self.server_cliente,))
        self.thread.start()
        
    def enviar_mensaje(self, mensaje):
        mensaje_encriptado = mensaje.encode()
        try:
            self.server_cliente.send(mensaje_encriptado)
        except:
            error_mnsj = 'CLIENTE: [SE HA PERDIDO LA CONEXION CON EL HOST]'
            self.mensaje_enviado_signal.emit(error_mnsj)

    def recibir_mensaje(self, server):
        while True:
            try:
                self.mensaje = server.recv(4096)
            except:
                break
            if len(self.mensaje.decode()) > 0:
                self.mensaje_enviado_signal.emit(self.mensaje.decode('utf-8'))

    def cerrar_conexion(self):
        self.server_cliente.close()
    

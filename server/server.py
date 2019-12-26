import socket
import threading
import time
import json


class Servidor:

    def __init__(self, host):

        self.host = host
        self.port = 2001  # DEJARE PORT 2001 ESTATICO PARA SIEMPRE
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.servidor.bind((self.host, self.port))
        self.iniciar_server()

    def iniciar_server(self):
        print(' SERVIDOR ONLINE\n ')
        self.servidor.listen(20)
        self.clientes = []

        while True:
            conn, addr = self.servidor.accept()
            conn.send(
                "\n<span style='color:#40FF00;font-style:italic'>Bienvenidos al Chat Cifrado!\n".encode('utf-8'))
            self.clientes.append((conn, addr[1]))
            print(f"<Se ha Conectado el usuario {addr[1]}>")
            self.enviar_mensajes(
                f"<span style='color:#40FF00;font-style:italic'>SERVER: [Se ha Conectado el usuario {addr[1]}]\n".encode('utf-8'), conn)
            threading._start_new_thread(self.clientthread, (conn, addr))

    def clientthread(self, conn, addr):
        while True:
            try:
                mensaje = conn.recv(4096)
                if mensaje:
                    mensaje_enviar = f"[{addr[1]}]: {mensaje.decode()}"
                    mensaje_personal = f"[TU]: {mensaje.decode()}"
                    conn.sendall(mensaje_personal.encode())
                    self.enviar_mensajes(mensaje_enviar.encode(), conn)
                    print(
                        f"[Mensaje de {addr[1]} a las {time.strftime('%H:%M:%S')}]: {mensaje.decode()}")
                else:
                    self.descartar(conn)
                    break
            except:
                continue

    def enviar_mensajes(self, mensaje, conn):
        for cliente in self.clientes:
            if cliente[0] != conn:
                try:
                    cliente[0].send(mensaje)
                except:
                    self.descartar(cliente)

    def descartar(self, cliente):
        if cliente in self.clientes:
            self.clientes.remove(cliente)
            cliente[0].shutdown(2)
            cliente[0].close()
            self.enviar_mensajes(
                f"<span style='color:#FF0000;font-style:italic'>SERVER: [Se ha Desconectado el usuario {cliente[1]}]\n".encode('utf-8'), None
            )


if __name__ == '__main__':
    import requests

    with open('parametros.json', 'r') as fil:
        datos = json.load(fil)
        host = datos[0]['IP_ADDRESS']
        fil.close()

    if host == '0.0.0.0':
        try:
            external_ip = requests.get('https://api.ipify.org').text
        except:
            external_ip = 'Nan'
        print(f' IP:{external_ip}, PORT: 2001')
    else:
        print(f'IP:{host}, PORT: 2001')

    server = Servidor(host)
    server

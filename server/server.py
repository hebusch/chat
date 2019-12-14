import socket
import threading
import time
import json 

class Servidor:

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.servidor.bind((self.host, self.port))
        self.iniciar_server()
    
    def iniciar_server(self):
        print(' SERVIDOR ONLINE\n ')
        self.servidor.listen(100)
        self.clientes = []
        self.addrs = []

        while True:
            conn, addr = self.servidor.accept()
            conn.send("\n<span style='color:#40FF00'>Bienvenidos al Chat Cifrado!\n".encode('utf-8'))
            self.clientes.append(conn)
            self.addrs.append(addr[1])
            print(f"<Se ha Conectado el usuario {addr[1]}>\n")
            self.enviar_mensajes(f"<span style='color:#40FF00'>SERVER: [Se ha Conectado el usuario {addr[1]}]\n".encode('utf-8'), conn)
            threading._start_new_thread(self.clientthread, (conn,addr))
    
    def clientthread(self, conn, addr):
        while True:
            try:
                mensaje = conn.recv(4096)
                if mensaje:
                    print(f"[Mensaje de {addr[1]} a las {time.strftime('%H:%M:%S')}]: {mensaje.decode()}")
                    mensaje_enviar = f"[{addr[1]}]: {mensaje.decode()}"
                    mensaje_personal = f"[TU]: {mensaje.decode()}"
                    conn.sendall(mensaje_personal.encode())
                    self.enviar_mensajes(mensaje_enviar.encode(), conn)
                    
                else:
                    self.descartar(conn)
            except:
                continue
        
    def enviar_mensajes(self, mensaje, conn):
        for cliente in self.clientes:
            if cliente != conn:
                try:
                    cliente.send(mensaje)
                except:
                    cliente.close()
                    self.clientes.remove(cliente)
                

    def descartar(self, conn):
        if conn in self.clientes:
            self.clientes.remove(conn)

if __name__ == '__main__':

    with open('parametros.json') as fil:
        datos = json.load(fil)
        host = datos[0]['IP_ADDRESS']
        port = datos[0]['PORT']
        fil.close()
    
    print(f' IP:{host}, PORT:{port}')
    server = Servidor(host, port)
    server
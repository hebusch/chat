import socket
import threading
import time
import json


class Servidor:

    lista_comandos = ['/help', '/hora', '/usuarios', '/desconectar']

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
            try:
                nickname = conn.recv(120).decode()
                addr1 = addr
                if nickname == 'no_nickname!':
                    pass
                else:
                    addr = (addr[0], nickname)
            except:
                addr = addr1
            print(f"<Se ha Conectado el usuario {addr[1]}>")
            conn.send(
                "\n<span style='color:#40FF00;'>Bienvenidos al Chat Cifrado!\n".encode(
                    'utf-8')
            )
            self.enviar_mensajes(
                f"<span style='color:#40FF00;'>[Se ha Conectado el usuario {addr[1]}]\n".encode(
                    'utf-8'), conn
            )
            cliente = (conn, addr[1])
            self.clientes.append(cliente)
            cliente[0].settimeout(300)
            thread = threading.Thread(
                target=self.clientthread, args=(cliente,), name=cliente[1])
            thread.daemon = True
            thread.start()

    def clientthread(self, cliente):
        while True:
            try:
                mensaje = cliente[0].recv(4096) 
                mensaje_enviar = f"[{cliente[1]}]: {mensaje.decode()}"
                mensaje_personal = f"[TU]: {mensaje.decode()}"
                cliente[0].sendall(mensaje_personal.encode())
                self.enviar_mensajes(mensaje_enviar.encode(), cliente[0])
                print(
                    f"[Mensaje de {cliente[1]} a las {time.strftime('%H:%M:%S')}]: {mensaje.decode()}")

                if mensaje.decode() == '/hora':
                    mensaje_enviar = self.hora()
                    print(
                        mensaje_enviar
                    )
                    self.enviar_mensajes(
                    f"<span style='color:#58ACFA;'>{mensaje_enviar}".encode(
                    ), self.servidor
                    )

                if mensaje.decode() == '/usuarios':
                    mensaje_enviar = self.usuarios()
                    print(
                        mensaje_enviar
                    )
                    self.enviar_mensajes(
                    f"<span style='color:#58ACFA;'>{mensaje_enviar}".encode(
                    ), self.servidor
                    )

                if mensaje.decode() == '/help':
                    mensaje_enviar = self.help(cliente[1])
                    print(
                        mensaje_enviar
                    )
                    cliente.sendall(
                    f"<span style='color:#58ACFA;'>{mensaje_enviar}".encode()
                    )

                if mensaje.decode() == '/desconectar':
                    self.descartar(cliente)
                
                if mensaje.decode() == '/info':
                    mensaje_enviar = self.info()
                    print(
                        mensaje_enviar
                    )
                    cliente.sendall(
                        f"<span style='color:#58ACFA;'>{mensaje_enviar}".encode()
                    )

            except:
                self.descartar(cliente)

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
            print(
                f"<Se ha Desconectado el usuario {cliente[1]}>"
            )
            mensaje = f"<span style='color:#FF0000;'>[Se ha Desconectado el usuario {cliente[1]}]"
            self.enviar_mensajes(mensaje.encode(), cliente[0])

    def help(self, cliente):
        mensaje_enviar = '[Comandos disponibles: '
        i = 0
        for comando in self.lista_comandos:
            if i == 0:
                mensaje_enviar = mensaje_enviar + f"{comando}"
                i += 1
            else:
                mensaje_enviar = mensaje_enviar + \
                    f", {comando}"
        mensaje_enviar = mensaje_enviar + "]"
        return mensaje_enviar

    def usuarios(self):
        mensaje_enviar = f"[Usuarios Conectados: "
        i = 0
        for usuario in self.clientes:
            if i == 0:
                mensaje_enviar = mensaje_enviar + \
                    f" {usuario[1]}"
                i += 1
            else:
                mensaje_enviar = mensaje_enviar + \
                    f", {usuario[1]}"
        return mensaje_enviar

    def hora(self):
        mensaje_enviar = f"[La hora actual es: {time.strftime('%H:%M:%S')}]"
        return mensaje_enviar
    
    def info(self):
        mensaje_enviar = f"[Estas conectado en el Servidor: {self.host}]\nHay {len(self.clientes)} usuarios conectados."
        return mensaje_enviar

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

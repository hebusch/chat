import paths
import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.QtMultimedia
from ventana import Ui_MainWindow

class Clientefe(Ui_MainWindow):
    estado_conexion_signal = PyQt5.QtCore.pyqtSignal(bool)
    mensaje_recibido_signal = PyQt5.QtCore.pyqtSignal(str)
    tecla_presionada_signal = PyQt5.QtCore.pyqtSignal()
    tecla_conectar_signal = PyQt5.QtCore.pyqtSignal()

    key_event_list = [PyQt5.QtCore.Qt.Key_Return]

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_enviar.hide()
        self.line_mensaje.hide()
        self.label_gris.hide()
        self.label_fondo.show()
        self.estado_FE = 1
        self.x = 5
        self.y = 10
        self.player = PyQt5.QtMultimedia.QMediaPlayer()
        self.sound = PyQt5.QtMultimedia.QMediaContent(PyQt5.QtCore.QUrl.fromLocalFile(paths.sound_path))
        self.player.setMedia(self.sound)
        self.player.setVolume(20)
        self.generar_conexion_signal = None
        self.mensaje_enviado_signal = None
        self.lista_labels = []
        self.init_signals()

    def init_signals(self):
        self.boton_conectar.clicked.connect(self.presionar_boton)
        self.estado_conexion_signal.connect(self.estado_conexion)
        self.mensaje_recibido_signal.connect(self.recibir_mensaje)
        self.boton_enviar.clicked.connect(self.enviar_mensaje)
        self.tecla_presionada_signal.connect(self.enviar_mensaje)
        self.tecla_conectar_signal.connect(self.presionar_boton)

    def keyPressEvent(self, event):
        if self.estado_FE == 2:
            if event.key() in self.key_event_list:
                self.tecla_presionada_signal.emit()
        if self.estado_FE == 1:
            if event.key() in self.key_event_list:
                self.tecla_conectar_signal.emit()

    def presionar_boton(self):
        self.ip_introducido = self.line_ip.displayText()
        self.port_introducido = self.line_port.displayText()

        if self.ip_introducido.replace('.','').isdigit():
            try:
                self.port_introducido = int(self.port_introducido)
                self.label_coneccion()
            except:
                self.label_emergencia.setText(
                    f"<html><head/><body><span style=' font-size:10pt; color:#ffffff;'><p align='center'>Ingrese un IP y PORT valido! </br></span></p></body></html>")
                self.label_emergencia.resize(self.label_emergencia.sizeHint())
                self.timer = PyQt5.QtCore.QTimer()
                self.timer.timeout.connect(self.actualizar_emergencia)
                self.timer.setSingleShot(True)
                self.timer.start(1500)
        else:
            self.label_emergencia.setText(
                f"<html><head/><body><span style=' font-size:10pt; color:#ffffff;'><p align='center'>Ingrese un IP y PORT valido! </br></span></p></body></html>")
            self.label_emergencia.resize(self.label_emergencia.sizeHint())
            self.timer = PyQt5.QtCore.QTimer()
            self.timer.timeout.connect(self.actualizar_emergencia)
            self.timer.setSingleShot(True)
            self.timer.start(1500)

    def actualizar_emergencia(self):
        self.label_emergencia.setText('')

    def label_coneccion(self):
        self.label_emergencia.setText(
            "<html><head/><body><span style=' font-size:10pt; color:#40FF00;'><p align='center'>CONECTANDO...</br></span></p></body></html>")
        self.label_emergencia.resize(self.label_emergencia.sizeHint())
        self.timer = PyQt5.QtCore.QTimer()
        self.timer.timeout.connect(self.generar_conexion)
        self.timer.setSingleShot(True)
        self.timer.start(1000)

    def generar_conexion(self):
        self.generar_conexion_signal.emit(self.ip_introducido, self.port_introducido)

    def estado_conexion(self, estado):
        if estado == True:
            self.boton_conectar.hide()
            self.label_ip.hide()
            self.line_ip.hide()
            self.label_port.hide()
            self.line_port.hide()
            self.labelAutor.hide()
            self.labelTitulo.hide()
            self.label_emergencia.hide()
            self.setWindowTitle(f'Chat Cifrado | IP: {self.ip_introducido} PORT: {self.port_introducido}')
            self.line_mensaje.show()
            self.boton_enviar.show()
            self.label_gris.show()
            self.estado_FE = 2

        elif estado == False:
            self.label_emergencia.setText(
                "<html><head/><body><span style=' font-size:10pt; color:#FF0000;'><p align='center'>CONEXION FALLIDA!</br></span></p></body></html>")
            self.label_emergencia.resize(self.label_emergencia.sizeHint())
            self.timer = PyQt5.QtCore.QTimer()
            self.timer.timeout.connect(self.actualizar_emergencia)
            self.timer.setSingleShot(True)
            self.timer.start(1000)

    def recibir_mensaje(self, mensaje):
        self.mensaje_a_mostrar = f"<html><head/><body><span style=' font-size:10pt; color:#ffffff;'>{mensaje}</br></span></body></html>"
        self.label = PyQt5.QtWidgets.QLabel(self.mensaje_a_mostrar, self)
        self.label.setGeometry(self.x, self.y, 0, 0)
        self.label.resize(self.label.sizeHint())
        self.player.play()
        self.label.show()
        self.lista_labels.append(self.label)
        self.y += 15
        self.actualizar_labels()

    def enviar_mensaje(self):
        mensaje = self.line_mensaje.displayText()
        self.line_mensaje.clear()
        self.mensaje_enviado_signal.emit(mensaje)

    def actualizar_labels(self):
        if self.largo(self.lista_labels) > 23:
            primer_label = self.lista_labels.pop(0)
            primer_label.hide()
            for label in self.lista_labels:
                for i in range(15):
                    x = label.pos().x()
                    y = label.pos().y()
                    label.move(x, y - 1)
            self.y -= 15
        else:
            pass

    def largo(self, lista):
        i = 0
        for elem in lista:
            i += 1
        return i

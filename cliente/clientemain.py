import PyQt5.QtWidgets
import clientefe
import clientebe
import sys

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication([])
    clienteFE = clientefe.Clientefe()
    clienteBE = clientebe.Cliente()

    clienteFE.generar_conexion_signal = clienteBE.generar_conexion_signal
    clienteBE.estado_conexion_signal = clienteFE.estado_conexion_signal
    clienteBE.mensaje_enviado_signal = clienteFE.mensaje_recibido_signal
    clienteFE.mensaje_enviado_signal = clienteBE.mensaje_recibido_signal
    clienteFE.nickname_enviar_signal = clienteBE.nickname_recibir_signal
    clienteFE.desconectar_signal = clienteBE.desconectar_signal

    clienteFE.show()

    sys.exit(app.exec_())

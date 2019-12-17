import PyQt5.QtWidgets
import PyQt5
import PyQt5.sip
import clientefe
import clientebe


import sys
app = PyQt5.QtWidgets.QApplication([])
clienteFE = clientefe.Clientefe()
clienteBE = clientebe.Cliente()

clienteFE.generar_conexion_signal = clienteBE.generar_conexion_signal
clienteBE.estado_conexion_signal = clienteFE.estado_conexion_signal
clienteBE.mensaje_enviado_signal = clienteFE.mensaje_recibido_signal
clienteFE.mensaje_enviado_signal = clienteBE.mensaje_recibido_signal

clienteFE.show()


sys.exit(app.exec_())

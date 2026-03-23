import sys
from PyQt5.QtWidgets import QApplication
from gui.app_gui import ServerMonitorGUI


app = QApplication(sys.argv)

window = ServerMonitorGUI()
window.show()

sys.exit(app.exec())

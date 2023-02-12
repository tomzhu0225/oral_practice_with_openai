import sys
from view.mainwindow import MainWindow
from model.chatsession import ChatSession
from view.controller import Controller
from PyQt5.QtWidgets import QApplication



app = QApplication(sys.argv)
# app.setStyleSheet("QMainWindow {background-color: #2b2b2b; color: white;}")
chatsession = ChatSession()
window = MainWindow()
window.show()
controller = Controller(model = chatsession, view = window)

# app.quit()
sys.exit(app.exec_())
sys.exit(0)


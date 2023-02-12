import sys
from view.mainwindow import MainWindow
from model.chatsession import ChatSession
from view.controller import Controller
from PyQt5.QtWidgets import QApplication



app = QApplication(sys.argv)
chatsession = ChatSession()
window = MainWindow()
window.show()
controller = Controller(model = chatsession, view = window)
sys.exit(app.exec_())

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget

from model.chatsession import ChatSession
from .components import ToolBar, SuggestionDockWidget, TextEdit, BackgroundInput, LowerLayout



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chat_session = ChatSession()

        # Size and Title
        self.setFixedSize(800, 900)
        self.setWindowTitle("ChatGPT Speaking Practice")

        # ToolBar
        self.toolbar = ToolBar(parent=self)
        self.addToolBar(self.toolbar)

        # Suggestion Window
        self.suggestion_window = SuggestionDockWidget()
        self.suggestion_window.setGeometry(self.x() + self.width(), self.y(), 400, 400)
        self.addDockWidget(Qt.TopDockWidgetArea, self.suggestion_window)
        # self.toolbar.addAction(self.suggestion_window.tips_action)
        
        # Create central widget, which contains:
        #   1. text_edit
        #   2. conversation backgound
        #   3. lower buttons
        self.central_widget = QWidget(parent=self)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.text_edit = TextEdit(parent=self)
        self.background_input = BackgroundInput(parent=self)
        self.lower_layout = LowerLayout(parent=self)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.background_input)
        self.layout.addLayout(self.lower_layout)

        self.central_widget.setLayout(self.layout)

        # creat bubble
        self.user_bubble = None
        self.ai_bubble = None


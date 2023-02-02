import sys
from PyQt5.QtCore import QObject, pyqtSlot,Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat,QFont,QBrush,QColor
from PyQt5.QtWidgets import QFormLayout,QDialogButtonBox, QDialog,QApplication,QDockWidget, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,QLabel,QComboBox, QLineEdit,QToolBar,QAction,QMessageBox
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import os
import openai
import requests
import time
import json
from core import recognize_from_mic,synthesize_to_speaker,respond,concatenate_me,concatenate_you,suggestion
class bubbleLabel(QLabel):
    def __init__(self, parent=None, text='', color='white', alignment=Qt.AlignLeft):
        super().__init__(parent)
        self.setText(text)
        self.setWordWrap(True)
        self.setAlignment(alignment)
        self.setStyleSheet(f'background-color: {color};  color: white;font: bold 25px Arial; padding: 25px; border-radius: 25px;')
class APIKeyDialog(QDialog):
    def __init__(self, azureapi=None, openaizpi=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("API Key")
        self.azureapi = azureapi
        self.openaiapi = openaizpi

        layout = QFormLayout()
        self.az_edit = QLineEdit(self.azureapi)
        layout.addRow("Azure API Key:", self.az_edit)
        self.op_edit = QLineEdit(self.openaiapi)
        layout.addRow("OpenAI API Key:", self.op_edit)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)
        self.setLayout(layout)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #set api key
        try:
            with open('azureapi.txt', 'r') as f:
                self.azureapi = f.read().strip()
            with open('openaiapi.txt', 'r') as f:
                self.openaiapi = f.read().strip()
        except FileNotFoundError:
            api_dialog = APIKeyDialog()
            if api_dialog.exec_() == QDialog.Accepted:
                self.azureapi = api_dialog.az_edit.text().strip()
                self.openaiapi = api_dialog.op_edit.text().strip()
                with open('azureapi.txt', 'w') as f:
                    f.write(self.azureapi)
                with open('openaiapi.txt', 'w') as f:
                    f.write(self.openaiapi)

        
        
        self.lang="zh-CN"
        # Create the toolbar
        self.toolbar = QToolBar("My Toolbar")
        self.addToolBar(self.toolbar)
        author_action = QAction("Author", self)
        self.toolbar.addAction(author_action)
        author_action.triggered.connect(self.display_author_info)
        
        #set circumstances
        self.conversation1 = ""
        self.conversation = ""
        self.is_conversation_set = False
        self.input_conversation = QLineEdit(self)
        self.input_conversation.setPlaceholderText("Enter the initial setting")
        self.input_conversation.textChanged.connect(self.update_conversation)
        self.input_conversation.setStyleSheet("""
QLineEdit {
        background-color: white;
        color: black;
        font-size: 25px;
        padding: 10px;
        border: 2px solid gray;
        border-radius: 5px;
    }
""")
        self.setWindowTitle("French Practice Application")
        #choose language
        self.language_combo_box = QComboBox(self)
        self.language_combo_box.addItems(["Chinese", "English", "French", "Japanese"])
        self.language_combo_box.currentIndexChanged.connect(self.change_language)
        self.language_combo_box.setStyleSheet("""
    QComboBox {
        background-color: white;
        color: black;
        padding: 5px;
        border: 1px solid gray;
        border-radius: 3px;
        min-width: 6em;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left-width: 1px;
        border-left-color: darkgray;
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }
    QComboBox::down-arrow {
        image: url(down_arrow.png);
    }
    QComboBox QAbstractItemView {
        background-color: white;
        border: 1px solid gray;
        selection-background-color: lightgray;
    }
""")
        
        self.setFixedSize(800, 900)

        # Create the text edit widget
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
    QTextEdit {
        background-color: white;
        background-image: url(/test.jpg);
        color: black;
        font-size: 16px;
        padding: 10px;
        border: 1px solid gray;
        border-radius: 3px;
    }
""")

        # Create the "Speak" button
        self.speak_button = QPushButton("Speak", self)
        self.speak_button.clicked.connect(self.speak)
        self.speak_button.setStyleSheet("QPushButton { background-color: grey; border-radius: 20px; padding: 10px; color:white; font-size:20px;} QPushButton:hover { background-color: red; } QPushButton:pressed { background-color: green; }")
        # Create the "Clear" button
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_text)
        # creat bubble
        self.user_bubble = None
        self.ai_bubble = None
        # Create the layout and add the widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.input_conversation)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.language_combo_box)
        button_layout.addWidget(self.speak_button)
        button_layout.addWidget(self.clear_button)

        self.layout.addLayout(button_layout)

        # Create the central widget and set the layout
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
    
        #for side windows
        self.side_window = QDockWidget("suggestion", self)       
        self.side_window.setGeometry(self.x() + self.width(), self.y(), 400, 400)
        #self.side_window.setAllowedAreas(Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.TopDockWidgetArea, self.side_window)
        
        self.side_widget = QWidget(self.side_window) #set layout
        layout = QVBoxLayout(self.side_widget)
        self.side_widget.setLayout(layout)
        self.side_window.setWidget(self.side_widget)
        self.tips_action = QAction("Suggestion", self)
        self.tips_action.setCheckable(True)
        self.tips_action.toggled.connect(self.toggle_side_window)
        self.toolbar.addAction(self.tips_action)
        self.label = QLabel(self.side_window)
        self.side_widget.layout().addWidget(self.label)
        
        # Update the label text
        #self.label.setText("New Text")
        
        #mode selector
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["high Intelligence", "medium Intelligence", "low Intelligence"])
        self.mode_selector.currentIndexChanged.connect(self.mode_changed)

        self.toolbar = self.addToolBar("Intelligence")
        self.toolbar.addWidget(self.mode_selector)
        self.respond_mod="text-davinci-003"
        self.sugg_mod="text-davinci-003"

    def mode_changed(self, index):
        if index==0:
            self.respond_mod="text-davinci-003"
            self.sugg_mod="text-davinci-003"
        elif index==1:
            self.respond_mod="text-davinci-003"
            self.sugg_mod="text-curie-001"
        else:
            self.respond_mod="text-curie-001"
            self.sugg_mod="text-curie-001"
    def toggle_side_window(self):
        if not self.side_window.isVisible():
            self.side_window.show()
            

    def display_author_info(self):
        QMessageBox.information(self, "Author Information", "Author: Bowen ZHU\nEmail: bowen.zhu@student-cs.fr")
    def closeEvent(self, event):
        QApplication.quit()
    @pyqtSlot()
    def update_conversation(self):
        self.conversation1 = self.input_conversation.text()
    @pyqtSlot()
    def change_language(self):
        current_language = self.language_combo_box.currentText()
        if current_language == "Chinese":
            self.lang = "zh-CN"
        elif current_language == "English":
            self.lang = "en-US"
        elif current_language == "French":
            self.lang = "fr-FR"
        elif current_language == "Japanese":
            self.lang = "ja-JP"
    @pyqtSlot()
    def append_text(self, text, color):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertBlock()
        charFormat = cursor.charFormat()
        charFormat.setForeground(QBrush(QColor(color)))
        font = QFont()
        font.setPointSize(14)
        font.setFamily("Arial")
        charFormat.setFont(font)
        cursor.setCharFormat(charFormat)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
    @pyqtSlot()
    def speak(self):
        if not self.is_conversation_set:
            self.conversation=self.conversation1
        new_me=recognize_from_mic(self.lang,self.azureapi)
        self.conversation=concatenate_me(self.conversation,new_me)
        print(self.conversation)
        self.append_text("You said: " + new_me, "blue")
        # self.user_bubble = bubbleLabel(text="Me: " + new_me, color='blue')
        # user_bubble_layout = QHBoxLayout()
        # user_bubble_layout.addWidget(self.user_bubble)
        # self.central_widget.layout().addLayout(user_bubble_layout)
        # self.layout.addLayout(user_bubble_layout)
        new_you=respond(self.conversation,self.respond_mod, self.openaiapi )
        self.append_text("AI: " + new_you.replace('\n', ''), "green")
        synthesize_to_speaker(new_you,self.lang,self.azureapi)
        
        self.conversation=concatenate_you(self.conversation,new_you)
        self.is_conversation_set = True
        time.sleep(0)
        old_layout = self.side_widget.layout().takeAt(0)
        if old_layout is not None:
            old_widget = old_layout.widget()
            
            if old_widget is not None:
                old_widget.deleteLater()
        self.conversation_sugg=self.conversation+'\nME:'
        sugg=suggestion(self.conversation_sugg,self.sugg_mod, self.openaiapi )
        self.ai_bubble = bubbleLabel(text=sugg.replace('\n', ''), color='green')
        ai_bubble_layout = QHBoxLayout()
        ai_bubble_layout.addWidget(self.ai_bubble)
        self.side_widget.layout().addLayout(ai_bubble_layout)
        # print(sugg)
        # self.label.setText(str(sugg))
        
    @pyqtSlot()
    def clear_text(self):
        self.text_edit.clear()
        self.conversation=''
        self.is_conversation_set = False

app = QApplication(sys.argv)
#app.setStyleSheet("QMainWindow {background-color: #2b2b2b; color: white;}")
window = MainWindow()
window.show()
app.quit()
sys.exit(app.exec_())
sys.exit(0)
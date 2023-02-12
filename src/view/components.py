from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QTextCursor, QFont, QBrush, QColor
from PyQt5.QtWidgets import QDockWidget, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QLineEdit, QToolBar, QAction

from . import qt_style_sheet



class BubbleLabel(QLabel):
    def __init__(self, parent=None, text='', color='white', alignment=Qt.AlignLeft):
        super().__init__(parent)
        self.setText(text)
        self.setWordWrap(True)
        self.setAlignment(alignment)
        self.setStyleSheet(f'background-color: {color};  color: white;font: bold 25px Arial; padding: 25px; border-radius: 25px;')



# Toolbar

class ToolBar(QToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.author_action = QAction("Author", self)
        self.addAction(self.author_action)

        self.text_vis = QAction("Text visibility", self)
        self.addAction(self.text_vis)

        self.mode_selector = QComboBox(self)
        self.mode_selector.addItems(["high Intelligence", "medium Intelligence", "low Intelligence"])
        self.addWidget(self.mode_selector)

        self.suggestion_action = QAction("Suggestion", self)
        self.suggestion_action.setCheckable(True)
        self.addAction(self.suggestion_action)


# Suggestion Bubble

class SuggestionDockWidget(QDockWidget):
    def __init__(self, *args, **kwargs):
        super().__init__("suggestion", *args, **kwargs)

        self.suggestion_widget = QWidget(self) #set layout
        layout = QVBoxLayout(self.suggestion_widget)
        self.suggestion_widget.setLayout(layout)
        self.setWidget(self.suggestion_widget)
        
        self.label = QLabel(self)
        self.suggestion_widget.layout().addWidget(self.label)

        self.suggestion_label = BubbleLabel(color='green')
        self.suggestion_label_layout = QHBoxLayout()
        self.suggestion_label_layout.addWidget(self.suggestion_label)

        self.suggestion_widget.layout().addLayout(self.suggestion_label_layout)
        self.hide() # initial hide the suggestion



# Central text window

class TextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setReadOnly(True)
        size_policy = self.sizePolicy()
        size_policy.setRetainSizeWhenHidden(True)
        self.setSizePolicy(size_policy)
        self.setStyleSheet(qt_style_sheet.text_edit)
    
    @pyqtSlot()
    def append_text(self, text, color):
        cursor = self.textCursor()
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
        self.setTextCursor(cursor)
        self.ensureCursorVisible()



# Background input

class BackgroundInput(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPlaceholderText("Enter the initial setting")
        self.setStyleSheet(qt_style_sheet.background_input)



# Lower buttons

class LanguageBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.language_list = ["Chinese", "English", "French", "Japanese"]
        self.addItems(self.language_list)
        self.setStyleSheet(qt_style_sheet.language_box)

class SpeakButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__("Speak", *args, **kwargs)
        self.setStyleSheet(qt_style_sheet.speak_button)

class ClearButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__("Clear", *args, **kwargs)

class LowerLayout(QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.language_box = LanguageBox(parent=parent)
        self.speak_button = SpeakButton(parent=parent)
        self.clear_button = ClearButton(parent=parent)
        self.addWidget(self.language_box)
        self.addWidget(self.speak_button)
        self.addWidget(self.clear_button)

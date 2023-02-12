from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QFont, QBrush, QColor
from PyQt5.QtWidgets import QSizePolicy, QFormLayout, QDialogButtonBox, QDialog, QApplication, QDockWidget, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QLineEdit, QToolBar, QAction, QMessageBox

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
        # self.side_widget = QWidget(self.side_window)  # set layout
        
        # self.suggestion_dock_widget = QDockWidget("suggestion", self)       
        # self.side_window.setGeometry(self.x() + self.width(), self.y(), 400, 400)
        #self.side_window.setAllowedAreas(Qt.RightDockWidgetArea)
        # self.addDockWidget(Qt.TopDockWidgetArea, self.side_window)
        
        self.suggestion_widget = QWidget(self) #set layout
        layout = QVBoxLayout(self.suggestion_widget)
        self.suggestion_widget.setLayout(layout)
        self.setWidget(self.suggestion_widget)

        # self.tips_action = QAction("Suggestion", self)
        # self.tips_action.setCheckable(True)
        # self.tips_action.toggled.connect(self.toggle_side_window)
        
        self.label = QLabel(self)
        self.suggestion_widget.layout().addWidget(self.label)

    # def toggle_side_window(self):
    #     if not self.isVisible():
    #         self.show()



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

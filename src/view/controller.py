from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import pyqtSlot

from model.core import suggestion
from view.components import BubbleLabel



class Controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._connect_signals()
    
    
    # ToolBar
    def _display_author_info(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self._view, "Author Information", "Author: Bowen ZHU\nEmail: bowen.zhu@student-cs.fr\nContributor: Chuanqi XU\nEmail: chuanqi.xu@yale.edu")
    
    def _change_text_vis(self):
        self._view.text_edit.setVisible(not self._view.text_edit.isVisible())

    def _change_mode(self, index):
        if index == 0:
            self._model.respond_mod = "text-davinci-003"
            self._model.sugg_mod = "text-davinci-003"
        elif index == 1:
            self._model.respond_mod = "text-davinci-003"
            self._model.sugg_mod = "text-curie-001"
        else:
            self._model.respond_mod = "text-curie-001"
            self._model.sugg_mod = "text-curie-001"
    
    # Background input
    @pyqtSlot()
    def _update_background(self):
        self._model.conversation = self.background_input.text()
        self._model.is_background_set = True

    # Lower Buttons
    # @pyqtSlot()
    def _speak(self):
        # old_layout = self.side_widget.layout().takeAt(0)
        # if old_layout is not None:
        #     old_widget = old_layout.widget()

        #     if old_widget is not None:
        #         old_widget.deleteLater()
        my_paragraph, ai_respond = self._model.forward()
        self._view.text_edit.append_text("You: " + my_paragraph, "blue")
        self._view.text_edit.append_text("AI: " + ai_respond, "green")

        self._model.conversation_sugg = self._model.conversation + '\nYou:'
        sugg = suggestion(self._model.conversation_sugg, self._model.sugg_mod, self._model.settings.openai_api)
        ai_bubble = BubbleLabel(text=sugg.replace('\n', ''), color='green')
        ai_bubble_layout = QHBoxLayout()
        ai_bubble_layout.addWidget(ai_bubble)

        # self._view.suggestion_window.setLayout(ai_bubble_layout)
        # self._view.central_widget.setLayout(ai_bubble_layout)
    
    def _clear_text(self):
        self._model.conversation=''
        self._model.is_background_set = False
        self._view.text_edit.clear()
    
    def _connect_signals(self):
        # ToolBar
        self._view.toolbar.author_action.triggered.connect(self._display_author_info)
        self._view.toolbar.text_vis.triggered.connect(self._change_text_vis)
        self._view.toolbar.mode_selector.currentIndexChanged.connect(self._change_mode)

        # Background input

        # Lower Buttons
        self._view.lower_layout.speak_button.clicked.connect(self._speak)
        self._view.lower_layout.clear_button.clicked.connect(self._clear_text)


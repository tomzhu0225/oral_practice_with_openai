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
    
    def _change_suggestion(self):
        self._model.is_suggestion = not self._model.is_suggestion
        if self._model.is_suggestion:
            self._view.suggestion_window.show()
        else:
            self._view.suggestion_window.hide()

    def _change_settings(self):
        self._model.settings._update_settings()


    
    # Background input
    # @pyqtSlot()
    def _update_background(self):
        self._model.conversation = self._view.background_input.text()
        self._model.is_background_set = True



    # Lower Buttons
    # @pyqtSlot()
    def _speak(self):
        my_paragraph, ai_respond, sugg = self._model.forward()
        self._view.text_edit.append_text("You: " + my_paragraph, "blue")
        self._view.text_edit.append_text("AI: " + ai_respond, "green")

        if self._model.is_suggestion:
            self._view.suggestion_window.suggestion_label.setText(sugg.replace('\n', ''))
    
    def _clear_text(self):
        self._model.conversation=''
        self._model.is_background_set = False
        self._view.text_edit.clear()
        self._view.background_input.clear()
        if self._model.is_suggestion:
            self._view.suggestion_window.suggestion_label.setText("")
    


    # Connect all signals when creating the objects

    def _connect_signals(self):
        # ToolBar
        self._view.toolbar.author_action.triggered.connect(self._display_author_info)
        self._view.toolbar.text_vis.triggered.connect(self._change_text_vis)
        self._view.toolbar.mode_selector.currentIndexChanged.connect(self._change_mode)
        self._view.toolbar.suggestion_action.triggered.connect(self._change_suggestion)
        self._view.toolbar.settings_action.triggered.connect(self._change_settings)

        # Background input
        self._view.background_input.textChanged.connect(self._update_background)

        # Lower Buttons
        self._view.lower_layout.speak_button.clicked.connect(self._speak)
        self._view.lower_layout.clear_button.clicked.connect(self._clear_text)


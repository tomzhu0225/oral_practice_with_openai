from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QWaitCondition, QMutex
from PyQt5.QtWidgets import QMessageBox



class Controller:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._default_settings()
        self._connect_signals()
    
    # ToolBar
    def _display_author_info(self):
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

    def _change_language(self):
        self._model.lang_tag = self._view.lower_layout.language_box.currentText()

    # @pyqtSlot()
    def _speak(self):
        if self._model.start_recording:
            self._model.start_recording = False
            my_paragraph, ai_respond, sugg = self._model._stop_speak()

            self._view.text_edit.append_text("\n\nAI: " + ai_respond, "green")

            if self._model.is_suggestion:
                self._view.suggestion_window.suggestion_label.setText(sugg.replace('\n', ''))
        else:
            self._model.start_recording = True
            self._model._start_speak()
            self._view.text_edit.append_text("\n\nYou: ", "blue")
    
    def _clear_text(self):
        self._model.conversation=''
        self._model.is_background_set = False
        self._view.text_edit.clear()
        self._view.background_input.clear()
        if self._model.is_suggestion:
            self._view.suggestion_window.suggestion_label.setText("")



    # Default settings when creating the objects
    def _default_settings(self):
        self._view.suggestion_window.hide()
        self._view.lower_layout.language_box.setCurrentText(self._model.lang_tag)



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
        self._view.lower_layout.language_box.currentIndexChanged.connect(self._change_language)
        
        self._view.lower_layout.speak_button.clicked.connect(self._speak)

        print_recognized = PrintRecognized(self._view)
        def _print_recognized(evt):
            print_recognized.run(evt)
            
        self._model.speech_recognizer.recognized.connect(_print_recognized)
        
        self._view.lower_layout.clear_button.clicked.connect(self._clear_text)



class PrintRecognized(QObject):
    # PyQt5 requires only the main thread controls the GUI
    # So speech_recognizer.recognized signals can not be directly send to control the GUI
    # To solve this, the signal from other threads can be transformed into pyqtSignal
    # 
    # The process is:
    # 1. speech_recognizer.recognized triggered
    # 2. call _print_recognized()
    # 3. inside _print_recognized(), call PrintRecognized.run()
    # 4. pyqtSignal signals, which then calls the function connected in PrintRecognized.__init__
    # 5. call self._view.text_edit.append_text() to print the text

    signal = pyqtSignal(str) # pyqtSignal needs to be defined on the class level

    def __init__(self, view):
        super().__init__()
        self._view = view
        self.signal.connect(lambda recognized_message: self._view.text_edit.append_text(recognized_message, "blue"))
    
    @pyqtSlot()
    def run(self, evt):
        self.signal.emit(evt.result.text)

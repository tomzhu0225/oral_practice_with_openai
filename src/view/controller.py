import threading
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QTextCursor



class CurrentThread(QObject):

    _on_execute = pyqtSignal(object, tuple, dict)

    def __init__(self):
        super(QObject, self).__init__()
        self._on_execute.connect(self._execute_in_thread)

    def execute(self, f, args, kwargs):
        self._on_execute.emit(f, args, kwargs)

    def _execute_in_thread(self, f, args, kwargs):
        f(*args, **kwargs)

main_thread = CurrentThread()

def run_in_main_thread(f):
    def result(*args, **kwargs):
        main_thread.execute(f, args, kwargs)
    return result



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
        self._model.change_mode(index)
    
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
            self._model.stop_speak()
            self._model.start_recording = False
            self.append_text(f"\n\n{self._model.ai_name}: generating...", "green")
        else:
            self._model.start_recording = True
            self._model.start_speak()
            self.append_text(f"\n\n{self._model.user_name}: ", "blue")
    
    def _append_recognized(self, evt):
        self.append_text(evt.result.text, "blue")

    def _response(self, evt):
        if not self._model.start_recording:
            my_paragraph, ai_response, sugg = self._model.respond()

            self.append_text(f"{ai_response}", "green", offset_length = len("generating..."))

            if self._model.is_suggestion:
                print("Start generating suggestion")
                print(sugg)
                self._view.suggestion_window.suggestion_label.setText(sugg.replace('\n', ''))
                print("Finish generating suggestion")
    
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



    # Connect all signals when creating the object
    def _connect_signals(self):
        # ToolBar
        self._view.toolbar.author_action.triggered.connect(self._display_author_info)
        self._view.toolbar.text_vis.triggered.connect(self._change_text_vis)
        self._view.toolbar.mode_selector.currentIndexChanged.connect(self._change_mode)
        self._view.toolbar.suggestion_action.triggered.connect(self._change_suggestion)
        self._view.toolbar.settings_action.triggered.connect(self._change_settings)

        # Text edit
        # change to QObject multithread
        self.append_text = run_in_main_thread(self._view.text_edit.append_text)

        # Background input
        self._view.background_input.textChanged.connect(self._update_background)

        # Lower Buttons
        self._view.lower_layout.language_box.currentIndexChanged.connect(self._change_language)
        
        self._view.lower_layout.speak_button.clicked.connect(self._speak)

        self._model.speech_recognizer.recognized.connect(self._append_recognized)
        self._model.speech_recognizer.session_stopped.connect(self._response)

        self._view.lower_layout.clear_button.clicked.connect(self._clear_text)


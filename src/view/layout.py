from PyQt5.QtWidgets import QHBoxLayout
from view.components import LanguageBox, SpeakButton, ClearButton


class LowerLayout(QHBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.language_box = LanguageBox(parent=parent)
        self.speak_button = SpeakButton(parent=parent)
        self.clear_button = ClearButton(parent=parent)
        self.addWidget(self.language_box)
        self.addWidget(self.speak_button)
        self.addWidget(self.clear_button)

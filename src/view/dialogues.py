from PyQt5.QtWidgets import QFormLayout, QDialog, QPushButton, QLineEdit



class SettingsDialog(QDialog):
    def __init__(self, azure_api=None, azure_region=None, openai_api=None, default_lang=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Settings")

        self.azure_api = azure_api
        self.azure_region = azure_region
        self.openai_api = openai_api
        self.default_lang = default_lang

        layout = QFormLayout()

        self.openai_api_edit = QLineEdit(self.openai_api)
        layout.addRow("OpenAI API Key:", self.openai_api_edit)

        self.default_lang_edit = QLineEdit(self.default_lang)
        layout.addRow("Default Language:", self.default_lang_edit)

        self.azure_api_edit = QLineEdit(self.azure_api)
        layout.addRow("Azure API Key:", self.azure_api_edit)

        self.azure_region_edit = QLineEdit(self.azure_region)
        layout.addRow("Azure Region:", self.azure_region_edit)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button)
        self.setLayout(layout)

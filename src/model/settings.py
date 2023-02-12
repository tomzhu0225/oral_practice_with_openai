from view.dialogues import SettingsDialog
import json

class Settings():
    def __init__(self):
        self.has_settings = False
        self._settings = self._load_settings()
    
    @property
    def openai_api(self):
        return self._settings["openai_api"]
    
    @property
    def default_lang(self):
        return self._settings["default_lang"]
    
    @property
    def azure_api(self):
        return self._settings["azure_api"]
    
    @property
    def azure_region(self):
        return self._settings["azure_region"]

    def _update_settings(self):
        api_dialog = SettingsDialog()
        if self.has_settings:
            api_dialog.openai_api_edit.setText(self._settings["openai_api"])
            api_dialog.default_lang_edit.setCurrentText(self._settings["default_lang"])
            api_dialog.azure_api_edit.setText(self._settings["azure_api"])
            api_dialog.azure_region_edit.setText(self._settings["azure_region"])
            settings = self._settings
        if api_dialog.exec_() == api_dialog.Accepted:
            settings = {}
            settings["openai_api"] = api_dialog.openai_api_edit.text().strip()
            settings["default_lang"] = api_dialog.default_lang_edit.currentText()
            settings["azure_api"] = api_dialog.azure_api_edit.text().strip()
            settings["azure_region"] = api_dialog.azure_region_edit.text().strip()

            with open("settings.json", 'w') as f:
                json.dump(settings, f, indent=4)
        return settings
    
    def _load_settings(self):
        # load settings
        try:
            with open("settings.json", 'r') as f:
                settings = json.load(f)
            self.has_settings = True
        except FileNotFoundError:
            settings = self._update_settings()
        
        return settings

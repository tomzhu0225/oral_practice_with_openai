from view.components import SettingsDialog
import json, langcodes

class Settings():
    def __init__(self):
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
        if api_dialog.exec_() == api_dialog.Accepted:
            # TODO: check LookupError
            input_lang = api_dialog.default_lang_edit.text().strip()
            default_lang = langcodes.find(input_lang).display_name()

            settings = {}
            settings["openai_api"] = api_dialog.openai_api_edit.text().strip()
            settings["default_lang"] = default_lang
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
        except FileNotFoundError:
            settings = self._update_settings()
        
        return settings

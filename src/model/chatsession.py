from model.core import recognize_from_mic, synthesize_to_speaker, respond, concatenate, concatenate, suggestion
from model.settings import Settings



class ChatSession:
    def __init__(self, print_cmd = True, *args, **kwargs):
        self.settings = Settings()
        self.lang_tag = self.settings.default_lang

        self.conversation = ""
        self.is_background_set = False

        self.respond_mod = "text-davinci-003"

        self.is_suggestion = False
        self.sugg_mod = "text-davinci-003"

        self.print_cmd = print_cmd
    
    def _speak(self):
        if not self.is_background_set:
            self.conversation = ""
        
        if self.print_cmd:
            print("Speak into your microphone.\n")
        
        my_paragraph = recognize_from_mic(self.lang_tag, self.settings.azure_api, self.settings.azure_region)
        self.conversation = concatenate(self.conversation, "You: ", my_paragraph)

        if self.print_cmd:
            print(f"You: {my_paragraph}\n")
        
        return my_paragraph

    def _respond(self):
        ai_respond = respond(self.conversation, self.respond_mod, self.settings.openai_api)
        synthesize_to_speaker(ai_respond, self.lang_tag, self.settings.azure_api, self.settings.azure_region)
        self.conversation = self.conversation + ai_respond
        self.is_background_set = True

        if self.print_cmd:
            print(f"AI: {ai_respond}\n")
        
        return ai_respond

    def _suggestion(self):
        self.conversation_suggestion = self.conversation+'\nYou: '
        sugg = suggestion(self.conversation_suggestion, self.sugg_mod, self.settings.openai_api)
        if self.print_cmd:
            print(f"Suggestion: {sugg}")
        return sugg
    
    def forward(self):
        my_paragraph = self._speak()
        ai_respond = self._respond()

        suggestion = None
        if self.is_suggestion:
            suggestion = self._suggestion()
        return (my_paragraph, ai_respond, suggestion)

    def mode_changed(self, index):
        if index == 0:
            self.respond_mod = "text-davinci-003"
            self.sugg_mod = "text-davinci-003"
        elif index == 1:
            self.respond_mod = "text-davinci-003"
            self.sugg_mod = "text-curie-001"
        else:
            self.respond_mod = "text-curie-001"
            self.sugg_mod = "text-curie-001"


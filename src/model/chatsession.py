from model.core import synthesize_to_speaker, respond, concatenate, concatenate, suggestion
from model.settings import Settings

import azure.cognitiveservices.speech as speechsdk


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

        self.speech_config = speechsdk.SpeechConfig(subscription=self.settings.azure_api, region=self.settings.azure_region, speech_recognition_language=self.lang_tag)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
        self.start_recording = False
        self.speech_recognizer.recognized.connect(self._append_recognized_text)
        self.speech_recognizer.session_stopped.connect(self._print_paragraph)
        self.my_paragraph = ""

        self.debug = False # only for debug
    
    def _start_speak(self):
        if not self.is_background_set:
            self.conversation = ""
        
        if self.print_cmd:
            print("Speak into your microphone.\n")
        
        self.speech_recognizer.start_continuous_recognition_async()
    
    def _append_recognized_text(self, evt):
        self.my_paragraph += evt.result.text
        if self.debug:
            print('RECOGNIZED inside: {}'.format(evt))
    
    def _stop_speak(self):
        self.speech_recognizer.stop_continuous_recognition_async()
        self.conversation = concatenate(self.conversation, "You: ", self.my_paragraph)

        return self.forward()
    
    def _print_paragraph(self, evt):
        if self.print_cmd:
            print(f"You: {self.my_paragraph}\n")
    
    def _respond(self):
        ai_respond = respond(self.conversation, self.respond_mod, self.settings.openai_api)
        synthesize_to_speaker(ai_respond, self.lang_tag, self.settings.azure_api, self.settings.azure_region)
        self.conversation = self.conversation + ai_respond
        self.is_background_set = True

        if self.print_cmd:
            print(f"AI: {ai_respond}\n")
        
        return ai_respond

    def _suggestion(self):
        sugg = suggestion(self.conversation + '\nYou: ', self.sugg_mod, self.settings.openai_api)
        if self.print_cmd:
            print(f"Suggestion: {sugg}")
        return sugg
    
    def forward(self):
        # my_paragraph = self._speak()

        ai_respond = self._respond()

        suggestion = None
        if self.is_suggestion:
            suggestion = self._suggestion()

        if self.debug:
            print(f"Current sentence: {self.conversation}")
        
        my_paragraph = self.my_paragraph
        self.my_paragraph = ""
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


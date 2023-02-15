import azure.cognitiveservices.speech as speechsdk
import openai

from model.settings import Settings



class ChatSession:
    def __init__(self, print_cmd = True, *args, **kwargs):
        self.settings = Settings()
        self.lang_tag = self.settings.default_lang
        self.print_cmd = print_cmd

        self.user_name = "You"
        self.ai_name = "AI"

        self.my_paragraph = ""
        self.conversation = ""
        self.is_background_set = False

        self.respond_mod = "text-davinci-003"

        self.is_suggestion = False
        self.sugg_mod = "text-davinci-003"

        self.speech_config = speechsdk.SpeechConfig(subscription=self.settings.azure_api, region=self.settings.azure_region)
        self.speech_config.speech_recognition_language = self.lang_tag
        self.speech_config.speech_synthesis_language = self.lang_tag
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=self.audio_config)
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=self.audio_config)

        self.start_recording = False
        self.speech_recognizer.recognized.connect(self._append_recognized_text)
        if self.print_cmd:
            self.speech_recognizer.session_stopped.connect(self._print_paragraph)

        # only for debug
        self.debug = False
        if self.debug:
            self.speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED {}'.format(evt)))
            self.speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
            self.speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    
    def start_speak(self):
        self.start_recording = True
        if not self.is_background_set:
            self.conversation = ""
        
        if self.print_cmd:
            print("Speak into your microphone.\n")
        
        self.speech_recognizer.start_continuous_recognition_async()
    
    def _append_recognized_text(self, evt):
        self.my_paragraph += evt.result.text

    def stop_speak(self):
        self.speech_recognizer.stop_continuous_recognition_async()
        self.conversation += f"\n{self.user_name}: {self.my_paragraph}\n\n{self.ai_name}:"
        self.start_recording = False
    
    def _print_paragraph(self, evt):
        print(f"{self.user_name}: {self.my_paragraph}\n")

    def suggestion(self):
        openai.api_key = self.settings.openai_api
        sugg = openai.Completion.create(
            model=self.sugg_mod,
            prompt=self.conversation + f'\n{self.user_name}: ',
            temperature=1,
            max_tokens=150,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0.1,
            stop=[f"{self.user_name}:", f"{self.ai_name}:"]
        ).choices[0].text

        if self.print_cmd:
            print(f"Suggestion: {sugg}")
        
        return sugg
    
    def respond(self):
        openai.api_key = self.settings.openai_api
        ai_response = openai.Completion.create(
            model=self.respond_mod,
            prompt=self.conversation,
            temperature=1,
            max_tokens=150,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=0.1,
            stop=[f"{self.user_name}:", f"{self.ai_name}:"]
        ).choices[0].text

        self.synthesizer.speak_text_async(ai_response)

        self.conversation = self.conversation + ai_response
        self.is_background_set = True

        if self.print_cmd:
            print(f"{self.ai_name}: {ai_response}\n")
        
        my_paragraph = self.my_paragraph
        self.my_paragraph = ""

        suggestion = None
        if self.is_suggestion:
            suggestion = self.suggestion()
        
        return (my_paragraph, ai_response, suggestion)
    
    def change_mode(self, index):
        if index == 0:
            self.respond_mod = "text-davinci-003"
            self.sugg_mod = "text-davinci-003"
        elif index == 1:
            self.respond_mod = "text-davinci-003"
            self.sugg_mod = "text-curie-001"
        else:
            self.respond_mod = "text-curie-001"
            self.sugg_mod = "text-curie-001"


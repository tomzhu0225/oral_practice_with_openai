# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 21:44:21 2023

@author: tomkeen
"""
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import os
import openai
import requests
import json



def recognize_from_mic(lang, key, region):
	#Find your key and resource region under the 'Keys and Endpoint' tab in your Speech resource in Azure Portal
	#Remember to delete the brackets <> when pasting your key and region!
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.speech_recognition_language = lang
    # audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)    
    #Asks user for mic input and prints transcription result on screen
    result = speech_recognizer.recognize_once()

    # Check the result
    # if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    #     print("Recognized: {}".format(result.text))
    # elif result.reason == speechsdk.ResultReason.NoMatch:
    #     print("No speech could be recognized: {}".format(result.no_match_details))
    # elif result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = result.cancellation_details
    #     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         print("Error details: {}".format(cancellation_details.error_details))

    return result.text

def synthesize_to_speaker(text,lang,key,region):
	#Find your key and resource region under the 'Keys and Endpoint' tab in your Speech resource in Azure Portal
	#Remember to delete the brackets <> when pasting your key and region!
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.speech_synthesis_language = lang
    #In this sample we are using the default speaker 
    #Learn how to customize your speaker using SSML in Azure Cognitive Services Speech documentation
    audio_config = AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)


def respond(conversation,mod,key):
    openai.api_key = key
    response = openai.Completion.create(
        model=mod,
        #model="text-curie-001",
        prompt=conversation,
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0.1,
        stop=["YOU:", "AI:"]
    )
    return response.choices[0].text

def suggestion(conversation,mod,key):
    openai.api_key = key
    response = openai.Completion.create(
        model=mod,
        prompt=conversation,
        temperature=1,
        max_tokens=150,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0.1,
        stop=["YOU:", "AI:"]
    )
    return response.choices[0].text

def concatenate(original, person="You", paragraph=""):
    return f"{original}\n{person}: {paragraph}\n\nAI:"


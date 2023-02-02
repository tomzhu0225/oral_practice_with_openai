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
#lang="zh-CN"
lang="fr-FR"
def recognize_from_mic(lang,key):
	#Find your key and resource region under the 'Keys and Endpoint' tab in your Speech resource in Azure Portal
	#Remember to delete the brackets <> when pasting your key and region!
    speech_config = speechsdk.SpeechConfig(subscription=key, region="francecentral")
    speech_config.speech_recognition_language = lang
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)    
    #Asks user for mic input and prints transcription result on screen
    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    print('Me:'+result.text)
    return result.text

def synthesize_to_speaker(text,lang,key):
	#Find your key and resource region under the 'Keys and Endpoint' tab in your Speech resource in Azure Portal
	#Remember to delete the brackets <> when pasting your key and region!
    speech_config = speechsdk.SpeechConfig(subscription=key, region="francecentral")
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
    stop=["ME:", "YOU:"])
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
    stop=["ME:", "YOU:"])
    return response.choices[0].text
def concatenate_me(original,new):
    return original+'\nME:'+new+"\nYOU:"
def concatenate_you(original,new):
    return original+new

if __name__=="__main__":
    conversation="The following is a conversation happened in a restauraut in france. you will play the waiter."  
    while 1:
        new_me=recognize_from_mic(lang)
        conversation=concatenate_me(conversation,new_me)
        new_you=respond(conversation)
        print('OpenAI:'+new_you)
        synthesize_to_speaker(new_you,lang)
        conversation=concatenate_you(conversation,new_you)
        user_input = input("Enter 'y' to continue or 'n' to break: ")
        if user_input == 'n':
            break
        elif user_input != 'y':
            print("Invalid input, please enter 'y' or 'n'.")

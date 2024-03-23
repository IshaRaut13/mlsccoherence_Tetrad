from gtts import gTTS
import os
from googletrans import Translator

def text_to_speech(text, language='en'):
    if language == 'hi':
        tts = gTTS(text, lang='hi')  # Generate Hindi speech
        tts.save("output_hi.mp3")    # Save as output_hi.mp3 for Hindi
    else:
        tts = gTTS(text, lang='en')  # Generate English speech
        tts.save("output_en.mp3")    # Save as output_en.mp3 for English

def play_audio(filename):
    os.system(f"start {filename}")

def translate_text_to_hindi(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='hi')
    return translation.text

if __name__ == "__main__":
    input_text = input("Enter the text you want to translate and convert to speech (English): ")
    print("Input English Text:", input_text)
    
    hindi_text = translate_text_to_hindi(input_text)
    print("Translated Hindi Text:", hindi_text)
    
    text_to_speech(input_text, language='en')  # Convert input text to English speech
    text_to_speech(hindi_text, language='hi')  # Convert translated Hindi text to Hindi speech

    # Play English speech
    play_audio("output_en.mp3")
    input("Press Enter to play Hindi speech...")
    
    # Play Hindi speech
    play_audio("output_hi.mp3")



import speech_recognition as sr
from googletrans import Translator

r = sr.Recognizer()
translator = Translator()

def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
                audio = r.listen(source, timeout=5)  # Set a timeout for listening
                print("Recognizing...")
                # Recognize speech in both Hindi and English
                hindi_text = r.recognize_google(audio, language='hi-IN')
                english_text = r.recognize_google(audio, language='en-US')
                return hindi_text, english_text
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")

def translate_to_english(hindi_text):
    translation = translator.translate(hindi_text, src='hi', dest='en')
    english_text = translation.text
    return english_text

def output_text(text):
    with open("output.txt", "a", encoding='utf-8') as f:
        f.write(text + "\n")

if __name__ == "__main__":
    while True:
        hindi_text, english_text = record_text()
        print("Hindi Text:", hindi_text)
        print("English Text:", english_text)
        translated_text = translate_to_english(hindi_text)
        print("Translated Text:", translated_text)
        output_text(translated_text)
        print("Wrote text:", translated_text)

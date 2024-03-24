import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
import speech_recognition as sr
import pyttsx3

# Load resources once
intents = json.loads(open(r'C:\Users\bausk\Desktop\CO\intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot.h5')

# Initialize speech recognizer and TTS engine
r = sr.Recognizer()
text_speech = pyttsx3.init()

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

def record_text(r):
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)  
            audio = r.listen(source, timeout=5)  
            print("Recognizing...")
            # Attempt to recognize speech in both Hindi and English
            try:
                hindi_text = r.recognize_google(audio, language='hi-IN')
            except:
                hindi_text = None
            english_text = r.recognize_google(audio, language='en-US')
            return hindi_text, english_text
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
    return None, None

def voice_output(text):
    text_speech.say(text)
    text_speech.runAndWait()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        if w in words:
            bag[words.index(w)] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [(i, r) for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])
    return "I don't understand."

print("GO! Bot is running!")

while True:
    hindi_text, english_text = record_text(r)
    if english_text:
        print(english_text)
        predicted_intents = predict_class(english_text)
        response = get_response(predicted_intents, intents)
        voice_output(response)
    else:
        voice_output("I didn't catch that. Could you please repeat?")

import random
import json
import pickle
import numpy as np
import nltk
import requests
import speech_recognition as sr
import pyttsx3

from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# Load intents and model for the existing chatbot
intents = json.loads(open(r'C:\Users\bausk\Desktop\CO\intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot.h5')

# Initialize speech recognizer
r = sr.Recognizer()

# Initialize text to speech engine
text_speech = pyttsx3.init()

# Initialize lemmatizer for text processing
lemmatizer = WordNetLemmatizer()

# Define Mistral LLM function
def llm_model(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Authorization": "Bearer YOUR_API_KEY", "Content-Type": "application/json"}
    
    conversation_history = []
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)
    full_prompt += ". Give shortest possible answer."
    
    data = {"model": "mistral:7b", "stream": False, "prompt": full_prompt}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response
    else:
        return "I'm sorry, I couldn't understand that. Can you please rephrase?"

# Define functions for text processing
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Define function to predict intent
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Define function to get response based on intent
def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("GO! Bot is running!")

# Main loop to process user input
while True:
    print("Listening...")
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            user_input = r.recognize_google(audio)
            print("Heard:", user_input)

            # Predict intent and decide response
            predicted_intents = predict_class(user_input)
            if float(predicted_intents[0]['probability']) < 0.5:
                response = llm_model(user_input)
            else:
                response = get_response(predicted_intents, intents)
            print("Response:", response)
            text_speech.say(response)
            text_speech.runAndWait()

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Unknown error occurred")

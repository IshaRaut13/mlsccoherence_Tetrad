import speech_recognition as sr
import pyttsx3
import requests
import json

r = sr.Recognizer()

def llm_model(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {'Content-Type': 'application/json'}
    data = {"model": "mistral", "stream": False, "prompt": prompt}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.json()
        actual_response = response_text.get("response", "No response found")
        print(actual_response)
        return actual_response
    else:
        print("Error:", response.status_code, response.text)
        return None

def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
                print("Processing...")
                text = r.recognize_google(audio)
                print("You said:", text)
                return text
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("Unknown error occurred")

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + "\n")

while True:
    user_input = record_text()
    if user_input.lower() == "exit":
        print("Exiting the program...")
        break

    model_output = llm_model(user_input)
    if model_output:
        output_text(model_output)

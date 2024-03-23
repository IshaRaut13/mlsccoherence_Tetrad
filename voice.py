import speech_recognition as sr
import pyttsx3
import requests
import json

r = sr.Recognizer()

def llm_model(prompt):
    url="http://localhost:11434/api/generate"

    headers = {
        'Content-Type' : 'application/json',
    }

    prompt+=". Give shortest possible answer."

    data={
        "model":"mistral",
        "stream":False,
        "prompt":prompt
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        print(actual_response)
        return actual_response  
    else:
        print("Error:", response.status_code, response.text)

def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")

def voice_output(text):
    text_speech = pyttsx3.init()
    text_speech.say(text)
    text_speech.runAndWait()

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + "\n")

while True:
    text = record_text()
    output = llm_model(text)
    voice_output(output) 
    output_text(output)
    print("Wrote text")

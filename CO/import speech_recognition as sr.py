import speech_recognition as sr
import pyttsx3
import requests
import json

r = sr.Recognizer()

def voice_output(text):
    text_speech = pyttsx3.init()
    text_speech.say(text)
    text_speech.runAndWait()

def llm_model(prompt):
    start="You're a CVA (Customer Virtual Assistant) called Sophia.Do not introduce yourself. Your job is to streamline user experience. Extract the following information as and when it comes - name"
    url="http://localhost:11434/api/generate"

    headers = {
        'Content-Type' : 'application/json',
    }
    prompt=start+prompt
    prompt+=". Give shortest possible answer."

    data={
        "model":"mistral:7b",
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
        print("Listening...")
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.2)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                print("Done")
                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")

def output_text(text):
    with open("output.txt", "a") as f:
        f.write(text + "\n")


def first():
    voice_output("Hi, this is Sophia, your smart solutions assistant. How are you?")
    text=record_text()
    llm_model(text)
    output = llm_model(text)
    #output_text(output)
    voice_output(output) 

first()




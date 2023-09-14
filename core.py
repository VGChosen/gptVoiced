import speech_recognition as sr
import g4f
import time
import pyttsx3
import asyncio 
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

engine = pyttsx3.init()
instruction_path = "instruction.txt"

def rewrite_line(_file, line_number, new_content):
    with open(_file, "r") as file:
        lines = file.readlines()

    if 0 < line_number <= len(lines):
        lines[line_number - 1] = f"{new_content}\n"  # Adjust index to match the line number

        with open(_file, "w") as file:
            file.writelines(lines)


def setCurrentDateTime():

    current_date = time.strftime('Date: %B %d, %Y')
    current_time = time.strftime("Time: %I:%M %p")
    current_day = time.strftime("Day: %A")

    rewrite_line(instruction_path, 17, current_date)
    rewrite_line(instruction_path, 18, current_time)
    rewrite_line(instruction_path, 19, current_day)
        

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from a microphone."""
    
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be a `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be a `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise for 1 second
        try:
            audio = recognizer.listen(source, timeout=5)  # Set a 5-second timeout for audio input
        except sr.WaitTimeoutError:
            return {"success": False, "error": "Audio input timed out", "transcription": None}

    ques_trans = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        ques_trans["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        ques_trans["success"] = False
        ques_trans["error"] = "API unavailable"
    except sr.UnknownValueError:
        ques_trans["error"] = "Unable to recognize speech"

    return ques_trans


# Create recognizer and microphone instances
recognizer = sr.Recognizer()
microphone = sr.Microphone()
microphone.energy_threshold = 4000
engine = pyttsx3.init()



def say_res_after_gen(ask):
    response_collection = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        provider=g4f.Provider.DeepAi,
        messages=[{"role": "user", "content": ask}],
        stream=True,
    )

    for message in response_collection:
        engine.say(message)
        engine.runAndWait()


def create_question(ques):
    setCurrentDateTime()
    rewrite_line(instruction_path, 23, ques)
    with open(instruction_path, "r+") as doc:
        return doc.read()
    
setCurrentDateTime()
        
        

from core import *

while True:
    print("Listening...")
    question_asked = recognize_speech_from_mic(recognizer, microphone)
    question_received = create_question(question_asked["transcription"])

    say_res_after_gen(question_received)

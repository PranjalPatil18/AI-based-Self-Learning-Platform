import speech_recognition as sr

# Record audio from default microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak now...")
    audio = r.listen(source)

# Convert audio to text using Google's speech recognition API
try:
    text = r.recognize_google(audio)
    print("You said: {}".format(text))
    
    # Compare text to given sentence
    given_sentence = "The quick brown fox jumps over the lazy dog"
    non_recognized_words = set(given_sentence.split(" ")).difference(set(text.split(" ")))
    print(non_recognized_words)
except sr.UnknownValueError:
    print("Sorry, I could not understand what you said.")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

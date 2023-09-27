from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from app.auth import authentication
from app.models import sentences, speech_result
from .form import sentence_form
from app.record import sentence_compare, translate_marathi
import random
import speech_recognition as sr
import json
import pyttsx3

# Create your views here.
def index(request):
    # return HttpResponse("This is Home page")    
    return render(request, "index.html",{'navbar' : 'home'})


def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return HttpResponseRedirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    # return HttpResponse("This is Home page")    
    return render(request, "log_in.html", {'navbar' : 'log_in'})

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(fname, contact_no, ussername)
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
            # return HttpResponse("This is Home page")
    return render(request, "register.html", {'navbar' : 'register'})
    
@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    random_sen = random.randint(0, sentences.objects.count() - 1)
    sen = sentences.objects.all()[random_sen]
    context = {
        'fname': request.user.first_name,
        'sen' : sen
        }
    name = request.user.first_name + ' ' + request.user.last_name
    sentence_for_record = speech_result(para = sen.qus, student_name= name)
    sentence_for_record.save()

    return render(request, "dashboard.html",context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard_record(request):
    store_para = speech_result.objects.last()
    data = {
        'labels': ['Red', 'Blue', 'Yellow'],
        'data': [10, 20, 30],
        'backgroundColor': [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
        ]
    }
    context = {
        'fname': request.user.first_name,
        'store_para' : store_para,
        'data' : json.dumps(data)
        }
    # Record audio from default microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    # Convert audio to text using Google's speech recognition API
    try:
        text = r.recognize_google(audio)
        print("You said: {}".format(text))
        
        original_sentence = store_para.para
        given_sentence = ""

        # convert the original sentence to lowercase
        original_sentence = original_sentence.lower()
        for char in original_sentence:
            # check if the character is a letter or a space
            if char.isalpha() or char.isspace():
                given_sentence += char
        # Compare text to given sentence
        list1 = given_sentence.split()
        list2 = text.split()
        different_words = sentence_compare(list1, list2)
        
        # calculate the average
        total_words = max(len(list1), len(list2))
        match_avg = (total_words - len(different_words)) / total_words
        match_avg = match_avg * 100
        match_avg = round(match_avg, 2)
        diff_words = " ".join(different_words)

        #translate in marathi
        marathi_meaning = translate_marathi(different_words)
        # marathi_words = " ".join(marathi_meaning)

        speech_result.objects.filter(student_name = store_para.student_name).update(not_recognized_words = diff_words, progress = match_avg, meaning = marathi_meaning)
        return redirect('result')
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return render(request, "dashboard_record.html",context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def result(request):
    store_para = speech_result.objects.last()
    meaning = eval(store_para.meaning)
    context = {
        'fname': request.user.first_name,
        'store_para' : store_para,
        'meaning' : meaning
        }
    if request.method == "POST":
        button_name = request.POST.get('key')
        print(button_name)
        text_speech = pyttsx3.init()
        text_speech.say(button_name)
        text_speech.runAndWait()
    else:
        print("Sorry")
    return render(request, "result.html",context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def add_sentences(request):
    sen = sentences.objects.all()
    context = {
        'fname': request.user.first_name,
        'sen' : sen,
        'form' : sentence_form(),
        }
    if request.method == "POST":
        form = sentence_form(request.POST)
        if form.is_valid():
            qus = form.cleaned_data['sentence']
            qus_data = sentences(qus = qus)
            qus_data.save()
            messages.success(request, 'Sentence Added Successfully!!!')
    return render(request, "add_sentences.html",context)


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

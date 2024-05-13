from django.shortcuts import render,redirect
from django.contrib import messages
from . models import *
import random 
from django.db.models import Sum, Count
from django.db import connection
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
import os
import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import operator
import datetime
import speech_recognition as sr
import time
def takeCommand():     
    r = sr.Recognizer()     
    with sr.Microphone() as source:         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   		
        print("Unable to Recognize your voice.")     
    return query
	
def speak(audio):
	engine = pyttsx3.init('sapi5')
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	engine.say(audio)
	engine.runAndWait()
def home(request):
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak("Good Morning!")
		speak("Welcome")
		time.sleep(3)
		speak("Please Login Using Your Quiz ID")
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Listening...")
			r.pause_threshold = 1
			audio = r.listen(source)
			print("Recognizing...")   
			query = r.recognize_google(audio, language ='en-in')
			crt=UserDetail.objects.filter(quiz_id=query)
			if crt:
				request.session['username']=query
				ids=UserDetail.objects.only('id').get(quiz_id=query).id
				request.session['user_id']=ids
				return redirect('exam')
			else:
				speak("Invalid QuizID")
				return render(request,'home.html',{})
	elif hour>= 12 and hour<18:
		speak("Good Afternoon!")  
		speak("Welcome")
		time.sleep(3)
		speak("Please Login Using Your Quiz ID")
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Listening...")
			r.pause_threshold = 1
			audio = r.listen(source)
			print("Recognizing...")   
			query = r.recognize_google(audio, language ='en-in')
			crt=UserDetail.objects.filter(quiz_id=query)
			if crt:
				request.session['username']=query
				ids=UserDetail.objects.only('id').get(quiz_id=query).id
				request.session['user_id']=ids
				return redirect('exam')
			else:
				speak("Invalid QuizID")
				return render(request,'home.html',{})
	else:
		speak("Good Evening!")
		speak("Welcome")
		time.sleep(3)
		speak("Please Login Using Your Quiz ID")
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Listening...")
			r.pause_threshold = 1
			audio = r.listen(source)
			print("Recognizing...")   
			query = r.recognize_google(audio, language ='en-in')
			crt=UserDetail.objects.filter(quiz_id=query)
			if crt:
				request.session['username']=query
				ids=UserDetail.objects.only('id').get(quiz_id=query).id
				request.session['user_id']=ids
				return redirect('exam')
			else:
				speak("Invalid QuizID")
				return render(request,'home.html',{})
	return render(request,'home.html',{})
def student_login(request):
	return render(request,'login.html',{})

def student_dashboard(request):
	if request.session.has_key('user_id'):
		return render(request,'student_dashboard.html',{})
	else:
		return render(request,'student_login.html',{})
def logout(request):
    try:
        del request.session['user_id']
    except:
     pass
    return render(request, 'student_login.html', {})

def exam(request):
	if request.session.has_key('user_id'):
			uid = request.session['user_id']
			user_id = UserDetail.objects.get(id=int(uid))
			questions = list(Quiz_Question.objects.all())		
			r_num =  random.randrange(1000,9999)
			num = r_num+int(uid)
			if Answer_Detail.objects.filter(rand_num=num).exists():
				s_num = random.randrange(1000,9999)
				num=num+s_num			
			speak('Start Quiz')
			print('Start Quiz')			
			time.sleep(2)
			for idx, question in enumerate(questions):
				ques = question.question
				q1 = question.option1
				q2 = question.option2
				q3 = question.option3
				q4 = question.option4
				speak(f"Question {idx+1}: {ques}")
				print(f"Question {idx+1}: {ques}")				
				time.sleep(2)
				speak("The Options Are")
				time.sleep(1)
				speak("a"+q1)
				print(q1)
				time.sleep(1)
				speak("b"+q2)
				print(q2)
				time.sleep(1)
				speak("c"+q3)
				print(q3)
				time.sleep(1)
				speak("d"+q4)
				print(q4)
				r = sr.Recognizer()
				with sr.Microphone() as source:
					print("Listening...")
					r.pause_threshold = 2
					audio = r.listen(source)
					print("Recognizing...")  
					try: 
						ans_quiz = r.recognize_google(audio, language ='en-in')
						crt = Answer_Detail.objects.create(question=question.id, rand_num=num,ans=ans_quiz,user_id=user_id)				
					except:
						speak("Sorry! Answer Does not recognize")								
			if crt:
				return redirect('answer_view',num=num)
			return render(request,'exam.html',{'question':question})
	else:
		return render(request,'student_login.html',{})

def answer_view(request,num):
	if request.session.has_key('user_id'):
			uid = request.session['user_id']
			user_id = UserDetail.objects.get(id=int(uid))
			user_answers = Answer_Detail.objects.filter(rand_num=num)
			quiz_questions = Quiz_Question.objects.all()
			correct_count = 0
			for user_answer in user_answers:
				question = quiz_questions.filter(id=user_answer.question).first()
				if question and user_answer.ans == question.answer:
					correct_count += 1
					count = str(correct_count)
	print("You answered correctly "+count+" out of "+str(len(user_answers)))
	speak("You answered correctly "+count+" out of "+str(len(user_answers)))
	return redirect('result_exam_data')

'''def answer_view(request, num):
    if 'user_id' in request.session:
        try:
            uid = int(request.session['user_id'])
            user_id = UserDetail.objects.get(id=uid)
            user_answers = Answer_Detail.objects.filter(rand_num=num)
            quiz_questions = Quiz_Question.objects.all()
            correct_count = 0
            for user_answer in user_answers:
                question = quiz_questions.filter(id=user_answer.question).first()
                if question and user_answer.ans == question.answer:
                    correct_count += 1
            count = str(correct_count)
            print("You answered correctly " + count + " out of " + str(len(user_answers)))
            # Assuming `speak` is a function that communicates with some text-to-speech engine
            speak("You answered correctly " + count + " out of " + str(len(user_answers)))
            return redirect('result_exam_data')  # Redirect user to appropriate page
        except UserDetail.DoesNotExist:
            return HttpResponse("User does not exist.")  # Handle case where user ID is invalid
    else:
        return HttpResponse("User session not found.") 
'''
	
		
def result_exam_data(request):
	if request.session.has_key('user_id'):
		speak("You Have Completed Your Quiz")
		return render(request,'result_exam_data.html',{})
	else:
		return render(request,'student_login.html',{})






#!/usr/bin/env python

import webapp2
import jinja2
import os
import time

from models.objects import Question
from models.objects import Answer
from models.objects import AnsweredQuestion
from models.objects import EstimationCredentials
from models.objects import globalInstances

from models.dbhelper import fetchGlobal
from models.dbhelper import update_or_Insert

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import db

jinjaEnv=jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname("views/")))

class TestModule(webapp2.RequestHandler):
	def post(self):
		user=users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		currUser=fetchGlobal(user)
		questionNumberToGive=int(currUser.questionNumberToGive)
		TotalQuestions=int(currUser.TotalQuestions)
		TotalQuestions=TotalQuestions-1
		if self.request.get('option',"") is not "":
			if self.request.get('option') == self.request.get('answer'):
				questionNumberToGive=questionNumberToGive+5
			elif self.request.get('option') != self.request.get('answer'):
				questionNumberToGive=questionNumberToGive+1
		else:
			questionNumberToGive=questionNumberToGive+2
		questionTimerEnd=round(time.time()+30.5)
		update_or_Insert(user, str(TotalQuestions), str(questionNumberToGive), str(questionTimerEnd))
		time.sleep( 2 )
		self.redirect("/test")
	
	def get(self):
		user=users.get_current_user()
		if not user:
			self.redirect(users.create_login_url(self.request.uri))
		currUser=fetchGlobal(user)
		questionNumberToGive=int(currUser.questionNumberToGive)
		TotalQuestions=int(currUser.TotalQuestions)
		questionTimerEnd=currUser.questionTimerEnd
		if TotalQuestions>0:
			f = open('db.txt')
			lines = f.readlines()
			f.close()
			questionNumber=10-TotalQuestions
			question= lines[questionNumberToGive]
			vals=question.split(",")
			qNo=str(questionNumber+1)
			CorrectOption=str(int(float(vals[5])))
			
			#make the vals
			vals={'title':qNo,'endTime':questionTimerEnd,'question':vals[0],'answer1':vals[1],'answer2':vals[2],'answer3':vals[3],'answer4':vals[4],'correctOption':CorrectOption,'current_user':user}
			#render to the template
			template=jinjaEnv.get_template('testQuestion.html')
			#write it to the handler's output stream
			self.response.out.write(template.render(vals))
		else:
			htmlSnippet='<form id="myForm" action="/" method="GET"><input type="submit" value="Goto Home"></form>'
			self.response.write("You Have finished giving the test, kindly press Take Test Button to redo the test!!!<br><br>%s"%htmlSnippet)

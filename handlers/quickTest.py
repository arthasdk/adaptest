#!/usr/bin/env python
import webapp2
import jinja2
import os
import time
import logging
import math
import globals
import string
from random import randint
from testmodule import *


jinjaEnv=jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname("views/")))







def getSolutionOfAnswerSet(str):
	params=[]
	currentTheta=2.5
	# a->question.a
	# b->question.b
	# c->question.c
	# d->u value :D
	a,b,c,d=0,0,0.25,0
	for x in range(0, 9):
		ch=str[x]
		#should be constant for testing purposes!
		a=0.8
		
		if(ch=='c' or ch=='r'):	#correct or right /pass or skip / incorrect or wrong
			b=currentTheta*(1.1665290394)
			d=globals.correctAnswer
		elif (ch=='p' or ch=='s'):
			b=currentTheta-(.4)
			d=globals.passAnswer
		else:
			b=currentTheta-(.625)
			d=globals.incorrectAnswer
		
		currentTheta=b
		if currentTheta<0 or currentTheta>10:
			return 'FAILURE, out of bounds reached at %s'%(x+1)
		params.append(a)
		params.append(b)
		params.append(c)
		params.append(d)
		
	theta_S=1.0
	while True:
		#time.sleep(1) #since db operations are going to happen its beneficial to waste some time here #notWorthIt
		theta_S_1=getNewTheta(params,theta_S)
		if math.fabs(theta_S_1-theta_S) <=0.2:
			break
		else:
			theta_S=theta_S_1
	return 'The Score for [%s] is %s'%(str,theta_S)



class quickTest(webapp2.RequestHandler):
	def post(self):
		QSET=self.request.get('QuestionSet')
		QSET=string.lower(QSET)
		if len(QSET) != 10:
			vals={'message':'Need to give 10 and exactly 10 choices!'}
		else:
			temp=getSolutionOfAnswerSet(QSET)
			vals={'message':'%s'%temp}
		template=jinjaEnv.get_template('message.html')
		self.response.out.write(template.render(vals))
	
	def get(self):
		template=jinjaEnv.get_template('QuickTesting.html')
		self.response.out.write(template.render())
		
from flask import Flask, url_for, request, render_template 

from app import app

import redis

# Here we are simply connecting our app to the data store
# r = redis.StrictRedis('localhost',6379,0) }All these are the same in writing the redis function
# r = redis.StrictRedis()  } This too is the same as the two ontop
r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

## SERVER/
@app.route('/')
def hello():      
	create_link = "<a href='" +  url_for('create') + "' >Create a question</a>"
	return """<html>
	               <head>
	                   <title>kukikotechindustries</title>
	               <head>

	                  <body>
	                     """ + create_link + """

	                   </body>
           
                </html>"""

## SERVER/CREATE
@app.route('/create', methods=['GET', 'POST'])
def create():
	# we are simply sending the form to the user
	if request.method == 'GET':
		return render_template('CreateQuestion.html')

	# we are simply taking the data from the user and saving it
	elif request.method == 'POST':
 		title=request.form['title']
 		question=request.form['question']
 		answer=request.form['answer']
 		# store the data in the data store
 		# Key name will be the title entered by the user in : Question
 		# Example for question: music:question,  countries:question
 		# # Example for answer: music:answer,  countries:answer
 		r.set(title + ':question', question)
 		r.set(title + ':answer', answer)

 		return render_template('CreatedQuestions.html', question=question)

	else: 
		return "<h2>INVALID REQUEST!</h2>"

## SERVER/QUESTION/<TITLE>
@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title): 
	# send user the form
	if request.method == 'GET':
		#Read data from the data store
		question = r.get(title+':question')
		return render_template('AnswerQuestion.html', question = question)

	elif request.method == 'POST':
	# the user has submitted the anwer, so check if the answer is correct
		submittedAnswer=request.form['submittedAnswer'] 

	# read answer from the data store
		answer=r.get(title + ':answer')
		if submittedAnswer == answer:
			return render_template('Correct.html')
		else:
			return render_template('Incorrect.html', submittedAnswer=submittedAnswer, answer=answer)
	else:
		return "<h2>INVALID REQUEST!<h2>"
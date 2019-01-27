from flask import Flask
from flask import request
from PIL import Image
import io
import os
import datetime
import json
import csv
import random

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

#add conversion to png regardless of image type
#Some globals for storing flags
#0 means not relevant
#1 means no parking
#2 means only during set time


@app.route('/', methods=['POST'])
def shit():
	#Variable init
	IsASign = 0
	CurrentTime = 0
	CurrentDT = 0
	HoursLeftParking = 0
	MinutesLeftParking = 0
	
	#cloud stuff
	client = vision.ImageAnnotatorClient()
	content = Image.open(request.files['image'])
	imgByteArr = io.BytesIO()
	content.save(imgByteArr, format='PNG')
	content = imgByteArr.getvalue()
	b = bytearray(content)	

	image = types.Image(content=content)
	response = client.text_detection(image=image)
	texts = response.text_annotations
	
	#contains list of text elements
	print('Texts:')
	for text in texts:
		print('\n"{}"'.format(text.description))
	
	#Get logo tags to make sure it's an image
	response = client.logo_detection(image=image)
	logos = response.logo_annotations
	print('Logos:')
	
	for logo in logos:
		if (logo.description == "bad religion"):
			IsASign = 1
		print(logo.description)
	#Get labels to also tell if it's an image
	response = client.label_detection(image=image)
	labels = response.label_annotations
	print('Labels:')
	
	for label in labels:
		if (label.description == "Street sign"):
			IsASign = 1
		print(label.description)	
	
	#Actual Guessing of signs meaning
	currentDT = datetime.datetime.now()
	print('Is a sign')
	print(IsASign)
	#Extract conditions start time
	FirstTime = texts[0].description.find('h')
	FirstTimeText = texts[0].description[(FirstTime-2):(FirstTime)]
	print('First time')
	print(FirstTimeText)
	#Extract conditions end time
	SecondTime = texts[0].description[FirstTime+1:].find('h')
	SecondTimeText = texts[0].description[(FirstTime+SecondTime-1):FirstTime+SecondTime+1]
	print('Second time')
	print(SecondTimeText)
	#Code for no parking
	#Calculate hours left to park
	if (int(FirstTimeText) > (currentDT.hour - 5)):
		HoursLeftParking = int(FirstTimeText) - currentDT.hour - 5
	else:
		HoursLeftParking = currentDT.hour - int(FirstTimeText) - 5
	#Calculate days left to park
	print('Hours left')
	print(HoursLeftParking-1)
	#Calculate minutes left to park
	if (int(FirstTimeText) > currentDT.minute):
		MinutesLeftParking = 60 - currentDT.minute
	else:
		MinutesLeftParking = 60 - currentDT.minute
	print('Minutes left')
	print(MinutesLeftParking-1)
	#Calculate days left
	ExpiryDate = datetime.date(2019,4,1)
	CurrentDate = datetime.date(2019,currentDT.month,currentDT.day)
	print("Days Left")
	print((ExpiryDate-CurrentDate).days)
	
	#Final prints
	mainWindowReturn = 0
	TitleReturnWindowReturn = 0
	
	mainWindowReturn = "You can park for " + str((ExpiryDate-CurrentDate).days) + " days, " + str(HoursLeftParking) + " hours" + " and " + str(MinutesLeftParking) + " minutes."
	
	if (IsASign != 0):
		TitleReturnWindowReturn = 'You can park here!'
	else:
		TitleReturnWindowReturn = 'You cannot park here!'
		mainWindowReturn = "This is not a valid sign"
	
	#quickly integrate some parking data triva from montreal
	parkingTrivia = 0
	with open("BornesSurRueV21.csv") as f:
		reader = csv.reader(f)
		chosen_row = random.choice(list(reader))
	print("Random crap")
	print(chosen_row)
	parkingTrivia = "If you have a type: " + chosen_row[3] + " parking permit, you can park on " + chosen_row[2] + " street."
	mainWindowReturn = mainWindowReturn + "\n" + parkingTrivia
	print(mainWindowReturn)
	#Json stuff
	data = {}
	data['Title'] = TitleReturnWindowReturn
	data['Text'] = mainWindowReturn
	json_data = json.dumps(data)	
	#end of json stuff
	print('Something')
	return json_data

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

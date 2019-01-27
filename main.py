from flask import Flask
from flask import request
from PIL import Image
import io
import os
import datetime
import json

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

#add conversion to png regardless of image type
#Some globals for storing flags
#0 means not relevant
#1 means no parking
#2 means only during set time
IsASign = 0
CurrentTime = 0
CurrentDT = 0


@app.route('/', methods=['POST'])
def shit():
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
	#Actual Guessing of signs meaning
	currentDT = datetime.datetime.now()
	print('Is a sign')
	print(IsASign)
	#Extract conditions start time
	FirstTime = texts[0].description.find('h')
	print('Start time')
	print(texts[0].description[(FirstTime-2):(FirstTime)])
	#Extract conditions end time
	#Code for no parking
	#SecondTime = texts[0].description[(FirstTime):].description.find('h')
	#print('End time')
	#print(texts[0].description[(SecondTime-2):(SecondTime)])
	
	
	#Json stuff
	data = {}
	data['Title'] = 'Image Result'
	data['Text'] = 'The main windows text'
	json_data = json.dumps(data)	
	#end of json stuff
	print('Something')
	return json_data

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

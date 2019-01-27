from flask import Flask
from flask import request
from PIL import Image
import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

#add conversion to png regardless of image type

@app.route('/', methods=['POST'])
def shit():
	client = vision.ImageAnnotatorClient()
	content = Image.open(request.files['image'])
	imgByteArr = io.BytesIO()
	content.save(imgByteArr, format='PNG')
	content = imgByteArr.getvalue()
	b = bytearray(content)	

	image = types.Image(content=content)
	response = client.label_detection(image=image)
	labels = response.label_annotations

	print('Labels:')
	for label in labels:
		print(label.description)
	
	print('Something')
	#img = Image.open(request.data)
	return 'Done'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

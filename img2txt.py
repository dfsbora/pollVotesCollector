# -*- coding: utf-8 -*-
import cv2 
import pytesseract 
import glob
import os
import sys


# Tesseract-OCR path 
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


imgspath = os.getcwd() +  "/" + sys.argv[1]
imgssearch = imgspath + "/*g"
filepath = sys.argv[1] + ".txt"


if os.path.exists(imgspath):

	images = [cv2.imread(file) for file in glob.glob(imgssearch)]
	#print(str(len(images))+" imagens encontradas.\n")

	# A text file is created and flushed 
	file = open(filepath, "w+") 
	file.write("") 
	file.close() 

	# Open the file in append mode 
	file = open(filepath, "a") 
	
	i=0		
	for image in images:
		i=i+1
		print("Foto" + str(i))


		# Pre processamento
		img = image[40:1215, 0:590]
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
		# OTSU threshold 
		ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
		# Specify structure shape and kernel size. 
		rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
		dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
		contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
		im2 = img.copy() 


		# Looping through the identified contours 
		# Then rectangular part is cropped and passed on 
		# to pytesseract for extracting text from it 
		# Extracted text is then written into the text file 

		# Comida
		lenc = len(contours) -2
		x, y, w, h = cv2.boundingRect(contours[lenc]) 
		rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
		cropped = im2[y:y + h, x:x + w] 
		comida = pytesseract.image_to_string(cropped) 
		print(comida + "\n")


		for j in range(0,lenc): 
			x, y, w, h = cv2.boundingRect(contours[j]) 
			rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
			cropped = im2[y:y + h, x:x + w] 
			text = pytesseract.image_to_string(cropped) 
			textfinal=text.split("\n")		
			if(textfinal[0] != ""):
				if(len(textfinal[0].split(" "))<3):
					line = textfinal[0] + ";" + comida
					file.write(line.encode("utf8"))
					file.write("\n")
					
	# Close the file 
	file.close 
	print("\nArquivo finalizado\n")

else:
	print("Error: Path does not exist")

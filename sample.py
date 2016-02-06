# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 13:14:31 2016

@author: David
"""
from projectoxford import Client
import urllib, cStringIO
from PIL import Image

client = Client.Face('113bf51955964f02a2215d74f9b3078b') #API KEY
file = cStringIO.StringIO(urllib.urlopen("http://172.18.141.55:8080/photo.jpg").read())
img = Image.open(file)
loc = "C:\\Users\\David\\Pictures\\test2.jpg"
img.save(loc,"JPEG") #saving image
#result1 = client.detect({'path': loc})
#result2 = client.detect({'url': 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'})
#print (result)
#test = client.verify('894a908c-6f38-48cd-a951-ee7dbde813d8', 'efedfac6-243e-4829-8502-3b2b932fe976')
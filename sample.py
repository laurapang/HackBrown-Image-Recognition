# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 13:14:31 2016

@author: David
"""
from projectoxford import Client
import urllib, cStringIO, json
from PIL import Image

client = Client.Face('113bf51955964f02a2215d74f9b3078b') #API KEY
#file = cStringIO.StringIO(urllib.urlopen("http://172.18.141.55:8080/photo.jpg").read())
#img = Image.open(file)
loc = "C:\\Users\\David\\Pictures\\laura_pang.jpg"
#img.save(loc,"JPEG") #saving image
snapId = client.detect({'path': loc})
print snapId
#result2 = client.detect({'url': 'https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg'})
#print (result)
#test = client.verify('894a908c-6f38-48cd-a951-ee7dbde813d8', 'efedfac6-243e-4829-8502-3b2b932fe976')

with open("Data.json") as data_file:
	data = json.load(data_file)

urls = {}

for person in data["contacts"]:
	urls[person["name"]] = person["profile_image_url"]

names = ['Aryan Chhabria','Laura Pang','Minah Seo','Daniel Yu']
dic = {}
#dic['name'] = str(result2[0]['faceId'])
#for friend in names:
#    dic[friend]= client.detect({'url': urls[friend]})[0]['faceId']
#    print "%s %s" %(friend,dic[friend])
for friend in names:
    friend_id = client.detect({'url': urls[friend]})[0]['faceId']
    ver = client.verify(snapId[0]['faceId'], str(friend_id))
    dic[friend]=ver
    #print ver
for name in dic:
    print "%s %s %s" %(name,dic[name]['isIdentical'],dic[name]['confidence'])
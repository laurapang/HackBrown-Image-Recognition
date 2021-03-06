# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 13:14:31 2016
@author: David
"""
#names = ['Aryan Chhabria','Laura Pang','Minah Seo','Daniel Yu','Aaron Gokaslan']
names = ['Joshua Drew', 'Anand Lalwani', 'Birol Senturk','Aaron Gokaslan']

from projectoxford import Client
import urllib, cStringIO, json
from PIL import Image

def match():
    client = Client.Face('113bf51955964f02a2215d74f9b3078b') #API KEY
    file = cStringIO.StringIO(urllib.urlopen("http://10.38.42.133:8080/photo.jpg").read())
    img = Image.open(file)
    img = img.rotate(270)
    loc = "cur_pic.jpg"
    img.save(loc,"JPEG") #saving image   
    snapId = client.detect({'path': loc})
    if not snapId:
        return 'cannot find a face'
    #print snapId
    
    with open("Data.json") as data_file:
        data = json.load(data_file)
     
    urls = {}
    for person in data["contacts"]:
        urls[person["name"]] = person["profile_image_url"]
    
    dic = {}
    for friend in names:
        friend_id = client.detect({'url': urls[friend]})[0]['faceId']
        ver = client.verify(snapId[0]['faceId'], str(friend_id))
        dic[friend]=ver
        #print ver
    
    ls = []
    for name in dic:
        if (dic[name]['isIdentical'] ==True):
            ls.append((name, dic[name]['confidence']))
        print "%s %s %s" %(name,dic[name]['isIdentical'],dic[name]['confidence'])
    print ls
    if len(ls)!=0:
        ls.sort(key=lambda x: x[1])
        sim_person = ls[-1]
        return str(sim_person)
    return 'no similar matches found'

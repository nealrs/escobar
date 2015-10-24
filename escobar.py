#!/usr/bin/python
import json, requests, textwrap
from PIL import Image, ImageDraw, ImageFont

# DATA
p = 'distractedness'
u = 'http://devpost.com/software/' + p
a = 'https://iii3mdppm7.execute-api.us-east-1.amazonaws.com/prod/ProjectEndpoint/' + p

resp = requests.get(url=a)
data = resp.json()

title = data['title']
tagline = data['tagline']
team = []
tags = []

for i,j in enumerate(data['collaborators']):
    #print i, j['screen_name']
    team.append( j['screen_name'] );

for k,v in enumerate(data['built_with']):
    #print k, v['name']
    tags.append( v['name'] );

#print title, tagline, team, tags

# Image

img = Image.open("back.png")
draw = ImageDraw.Draw(img)
W = img.size[0]
H = img.size[1]

# load fonts & set sizes.
f1 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 30)
f2 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 15)
f3 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 20)
c1 = "white"


# calculate size of title & center it
if ((f1.getsize(title)[0]) <= 350):
    ft = f1
else:
    ft = f3

tw, th = draw.textsize(title, font=ft)
tx = (W-tw)/2
ty = 10
draw.text((tx, ty), title, fill=c1, font=ft)


# calculate size of tagline & draw it
taglineM = textwrap.wrap(tagline, width=55)
y_text = ty+ft.getsize(title)[1]+10
for line in taglineM:
    tagw, tagh = f2.getsize(line)
    draw.text(((W - tagw) / 2, y_text), line, font=f2, fill=c1)
    y_text += tagh

#draw.text((20, 120), team)
#draw.text((20, 160), tags)

img.save("o.png", "PNG")

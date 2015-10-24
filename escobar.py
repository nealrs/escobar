#!/usr/bin/python
import json, requests, textwrap, unicodedata, click
from PIL import Image, ImageDraw, ImageFont

@click.command()
@click.argument('slug', required=True)
def escobar(slug):
    # DATA
    p = slug
    #p = 'infraudio-nuc8df'
    u = 'http://devpost.com/software/' + p
    a = 'https://iii3mdppm7.execute-api.us-east-1.amazonaws.com/prod/ProjectEndpoint/' + p

    resp = requests.get(url=a)
    data = resp.json()

    title = data['title']
    tagline = data['tagline']
    team = "TEAM: "
    tags = "STACK: "
    wins = 0

    # determine if winner, who's on the team, and what's in the stack
    for a,b in enumerate(data['submitted_to']):
        #print b['prizes_won']
        if (b['prizes_won']):
            wins = wins +1

    for i,j in enumerate(data['collaborators']):
        team += j['name'] + u" \u00B7 "
    team = team[:-3] #trim it!

    for k,v in enumerate(data['built_with']):
        tags += "#"+ v['name'] + " "
    tags = tags[:-1] #trim it!

    #print title, tagline, team, tags, wins

    # IMAGE

    #  load base images
    img = Image.open("img/base.png")
    banner = Image.open("img/banner.png")
    draw = ImageDraw.Draw(img)
    W, H = img.size

    # add banner if it's a winner
    if (wins > 0):
        img.paste(banner, (0, 0), banner.convert('RGBA'))

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
    # stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image
    taglineM = textwrap.wrap(tagline, width=55)
    y_text = ty+ft.getsize(title)[1]+5
    for line in taglineM:
        tagw, tagh = f2.getsize(line)
        draw.text(((W - tagw) / 2, y_text), line, font=f2, fill=c1)
        y_text += tagh

    # calculate size of team & tags & draw them
    teamM = textwrap.wrap(team, width=55)
    y_text = y_text + 10
    for line in teamM:
        tagw, tagh = f2.getsize(line)
        draw.text((10, y_text), line, font=f2, fill=c1)
        y_text += tagh

    tagsM = textwrap.wrap(tags, width=55)
    y_text = y_text + 10
    for line in tagsM:
        tagw, tagh = f2.getsize(line)
        draw.text((10, y_text), line, font=f2, fill=c1)
        y_text += tagh

    # save to disk bro!
    img.save(p+".png", "PNG")
    print "that's a wrap on " +title+ "!"

##########################
if __name__ == '__main__':
    escobar()

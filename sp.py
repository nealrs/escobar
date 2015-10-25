#!/usr/bin/python


# THIS VERSION IS FOR CREATING STAFF PICKS GIFS & MP4S.
# (It's also pretty friggin neat!)

import json, requests, textwrap, unicodedata, click, os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

@click.command()
@click.argument('slugs', required=True, nargs=4)
def escobar(slugs):
    """Create share-ready images & gifs & videos for Devpost staffpicks"""

    # load fonts & set sizes.
    f1 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 60)
    f2 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 30)
    f3 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 40)
    c1 = "white"
    f=0 # frame #

    # TITLE FRAME
    img = Image.open("img/baseSP.jpg")
    draw = ImageDraw.Draw(img)
    logo = Image.open("img/logo.png")
    #heart = Image.open("img/heart.png")
    W, H = img.size

    # add logo & heart
    img.paste(logo, ((W-logo.size[0])/2, 20), logo.convert('RGBA'))
    #i0.paste(heart, ((W-heart.size[0])/2, 20 + logo.size[1] ), heart.convert('RGBA'))

    # calculate size of title & center it
    #if ((f1.getsize("Staff picks ")[0]) <= 700):
        #ft = f1
    #else:
        #ft = f3

    tw, th = draw.textsize("Staff picks", font=f1)
    tx = (W-tw)/2
    ty = 20 + logo.size[1] + 10
    draw.text((tx, ty), "Staff picks", fill=c1, font=f1)

    img.save("0.png", "PNG")

    # ITERATE THROUGH INDIVIDUAL PROJECTS
    for s in slugs:
        f = f+1
        fn = str(f)+".png"

        # GET DATA
        p = s
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
        img = Image.open("img/base.jpg")
        banner = Image.open("img/banner.png")
        draw = ImageDraw.Draw(img)
        W, H = img.size

        # add banner if it's a winner
        if (wins > 0):
            img.paste(banner, (0, 0), banner.convert('RGBA'))

        # calculate size of title & center it
        if ((f1.getsize(title)[0]) <= 7000):
            ft = f1
        else:
            ft = f3

        tw, th = draw.textsize(title, font=ft)
        tx = (W-tw)/2
        ty = 20
        draw.text((tx, ty), title, fill=c1, font=ft)

        # calculate size of tagline & draw it
        # stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image
        taglineM = textwrap.wrap(tagline, width=50)
        y_text = ty+ft.getsize(title)[1]+10
        for line in taglineM:
            tagw, tagh = f2.getsize(line)
            draw.text(((W - tagw) / 2, y_text), line, font=f2, fill=c1)
            y_text += tagh

        # calculate size of team & tags & draw them
        teamM = textwrap.wrap(team, width=53)
        y_text = y_text + 20
        for line in teamM:
            tagw, tagh = f2.getsize(line)
            draw.text((20, y_text), line, font=f2, fill=c1)
            y_text += tagh

        tagsM = textwrap.wrap(tags, width=53)
        y_text = y_text + 20
        for line in tagsM:
            tagw, tagh = f2.getsize(line)
            draw.text((20, y_text), line, font=f2, fill=c1)
            y_text += tagh

        img.save(fn, "PNG")
        print title+" -- COMPLETE"

    # COMPILE VIDEO & GIF
    FPS = .4
    clip = ImageSequenceClip(["0.png", "1.png", "2.png", "3.png", "4.png"], fps=FPS)
    clip.write_videofile("staffpicks.mp4", fps=FPS)
    clip.write_gif("staffpicks.gif",fps=FPS)

    # CLEAN UP
    for x in [0,1,2,3,4]:
        os.remove(str(x)+".png")

    print "OK!"

if __name__ == '__main__':
    escobar()

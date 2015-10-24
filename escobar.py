#!/usr/bin/python
import json, requests, textwrap, unicodedata, click, os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

@click.command()
@click.argument('slug', required=True)
@click.option('--gif', default=False, type=bool, help='Do you want to create gif frames? (True / False)')
@click.option('--video', default=False, type=bool, help='Do you want to create a video? (True / False)')
def escobar(slug, gif, video):
    """Create share-ready images & gifs & videos for your Devpost projects"""
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

    # load fonts & set sizes.
    f1 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 60)
    f2 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 30)
    f3 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 40)
    c1 = "white"

    #  MAIN FRAME
    img = Image.open("img/base2.jpg")
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
    taglineM = textwrap.wrap(tagline, width=55)
    y_text = ty+ft.getsize(title)[1]+10
    for line in taglineM:
        tagw, tagh = f2.getsize(line)
        draw.text(((W - tagw) / 2, y_text), line, font=f2, fill=c1)
        y_text += tagh

    # calculate size of team & tags & draw them
    teamM = textwrap.wrap(team, width=55)
    y_text = y_text + 20
    for line in teamM:
        tagw, tagh = f2.getsize(line)
        draw.text((20, y_text), line, font=f2, fill=c1)
        y_text += tagh

    tagsM = textwrap.wrap(tags, width=55)
    y_text = y_text + 20
    for line in tagsM:
        tagw, tagh = f2.getsize(line)
        draw.text((20, y_text), line, font=f2, fill=c1)
        y_text += tagh

    # OH SNAP, LET'S GET ANIMTED!
    if (gif is True or video is True):
        print "Generating frames"
        img.save("1.png", "PNG")

        # LOGO FRAME
        img = Image.open("img/base2.jpg")
        draw = ImageDraw.Draw(img)
        logo = Image.open("img/logo2.png")
        heart = Image.open("img/heart2.png")
        W, H = img.size

        # add logo & heart
        img.paste(logo, ((W-logo.size[0])/2, 20), logo.convert('RGBA'))
        img.paste(heart, ((W-heart.size[0])/2, 20 + logo.size[1] ), heart.convert('RGBA'))

        # calculate size of title & center it
        if ((f1.getsize(title)[0]) <= 700):
            ft = f1
        else:
            ft = f3

        tw, th = draw.textsize(title, font=ft)
        tx = (W-tw)/2
        ty = 20 + logo.size[1] + 140
        draw.text((tx, ty), title, fill=c1, font=ft)

        img.save("0.png", "PNG")
        FPS = .5
        clip = ImageSequenceClip(["0.png", "1.png"], fps=FPS)

        # write output gif / video
        if (video is True):
            clip.write_videofile(p+".mp4", fps=FPS)

        if (gif is True):
            clip.write_gif(p+".gif",fps=FPS)

        # let's clean up after ourselves, no?
        os.remove("0.png")
        os.remove("1.png")

    else:
        # if GIF is false, just save the original slide as a PNG
        img.save(p+".png", "PNG")

    print "that's a wrap on " +title+ "!"

if __name__ == '__main__':
    escobar()

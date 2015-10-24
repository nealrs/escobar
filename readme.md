![](https://github.com/nealrs/escobar/blob/master/examples/distractedness.png?raw=true)

## Inspiration

1. I want hackers to be proud of their work on Devpost and share it.
2. Twitter cards expand automatically on mobile, but not desktop.
3. Twitter _images_ expand automatically on all platforms.
4. Facebook prioritizes native video over youtube embeds + hates gifs
5. Gifs are awesome.
6. Twitter's now deprecated [product cards](https://dev.twitter.com/cards/types/product), which we used to list team & stack.
7. Buffer's [Pablo](https://buffer.com/pablo) image generator for social sharing.
8. A desire to learn how to build images programmatically.

## What it is

Escobar takes Devpost URL slugs and creates a pretty, Twitter-optimized, image with key project details: title, tagline, team, and tags. I hope it'll encourage people to share their projects more via social.

Oh, and it can also generate videos, which will autoplay on Facebook, and gifs for Twitter.

### How to use it:

This will create a gif, and a mp4 vide clip of my Summer Jam landing page project, (`sj` is the url slug). For a static PNG, don't set the `--gif` or `-video` flags.

```bash
$  python escobar.py --gif=True --video=True sj
```

![](http://i.imgur.com/RVRPWd8.gif)

### A quick note: screw you node
>
>I originally tried doing this whole project in node. Getting the data from Devpost's API was easy in node (thanks zombie!), but the imaging portion was a total fail. I couldn't get `node-gd`, `cairo`, and 3 other C & npm packages to install correctly. But I'm a maverick, so I changed up. Only real dev language my ass.

>![](http://i.imgur.com/WuPCom7.jpg)

## Getting the data

I &#9829;`requests` &amp; Python. This is all it took to get the JSON data:

```python
p = 'infraudio-nuc8df'
u = 'http://devpost.com/software/' + p
a = 'https://iii3mdppm7.execute-api.us-east-1.amazonaws.com/prod/ProjectEndpoint/' + p

resp = requests.get(url=a)
data = resp.json()

#title = data['title']
#tagline = data['tagline']
```

Next, I iterated through the `collaborators` & `built_with` dicts to compile strings of the team members & stack tags. I also added a check to see if the project had ever won a hackathon. I used that to overlay a conditional "winner" banner.

![](https://github.com/nealrs/escobar/blob/master/examples/1.gif?raw=true)

Later, I setup an argument parser to get the url slug (`p`) via the command line using `click`.

## Building the image

After the node debacle, using `Pillow` was a dream.

First, I compiled some assets:
- 800x400 background image
- truetype font files for Roboto
- winner banner

Next, I started compositing my image by opening up the background, calculating the size, setting some default font sizes & colors, and overlaying the winner banner if this project is a winner:

```python
img = Image.open("img/base2.jpg")
banner = Image.open("img/banner.png")
draw = ImageDraw.Draw(img)
W, H = img.size

# add banner if it's a winner
if (wins > 0):
    img.paste(banner, (0, 0), banner.convert('RGBA'))

# load fonts & set sizes.
f1 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 60)
f2 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 30)
f3 = ImageFont.truetype("roboto/Roboto-Regular.ttf", 40)
c1 = "white"
```

To add the title, I first had to calculate how big it'd be and the coordinates neccesary to center. And if it was wider than 700 pixels, I decreased the font size.

```python
if ((f1.getsize(title)[0]) <= 7000):
    ft = f1
else:
    ft = f3

tw, th = draw.textsize(title, font=ft)
tx = (W-tw)/2
ty = 20
draw.text((tx, ty), title, fill=c1, font=ft)
```

I did the same thing with the tagline, team members, and stack tags, but I had to deal with the multiline problem. `Pillow` supports multiline text, but expects you to have already inserted new lines in your text to force wrapping. Since I was starting with one long string, I had to inserting newlines manually. [I found a solution on Stack Overflow](http://stackoverflow.com/questions/7698231/python-pil-draw-multiline-text-on-image) that works really nicely.

Basically, it uses `textwrap` to insert newlines every X characters and then adds each line (as though it were a single line) iteratively using the line height to space them out.

```python
taglineM = textwrap.wrap(tagline, width=55)
y_text = ty+ft.getsize(title)[1]+10
for line in taglineM:
    tagw, tagh = f2.getsize(line)
    draw.text(((W - tagw) / 2, y_text), line, font=f2, fill=c1)
    y_text += tagh
```

Finally, we can save to disk:

```python
img.save(p+".png", "PNG")
```

## Feeling animated

After I got the basic script working, I thought to myself: what about creating an animated gifs and video? Easy.

Well, It was easy to create an additional/title slide with the Devpost logo, heart, and project title. You can review that code yourself.

It was not easy way to compile the animated gif within Python or via shell script though. I couldn't get subprocess to stop complaining about directories, and all the `Pillow` hacks I tried failed. Then I tried using `gifsicle`, which was great, but wasn't a complete solution (no video). So I switched to `moviepy` which uses `ffmpeg` and does it all!

After generating my two animation frames `0.png` & `1.png`, it's just a matter of telling `moviepy` what to do:

```python
# sequence images into a clip
FPS = .75
clip = ImageSequenceClip(["0.png", "1.png"], fps=FPS)

# write output gif or video
if (video is True):
  clip.write_videofile(p+".mp4", fps=FPS)

if (gif is True):
  clip.write_gif(p+".gif",fps=FPS)

# let's clean up after ourselves and remove our temporary files.
os.remove("0.png")
os.remove("1.png")
```

Das it!!

## Next steps

I dunno, I'd like to setup a script that generates & auto-tweets these bad jacksons whenever I set staff picks. Or I could cards to the gif for team avatars (For those that have one) / dedicate one just to the stack. I dunno, you tell me. I'd love to hear your feedback and suggestions.

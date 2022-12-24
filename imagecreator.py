from PIL import Image, ImageDraw, ImageSequence,ImageFont
import random
import os
import textwrap
gifs = os.listdir("gokugifs")



def writeText(gif, ruleid :int , text:str,filename:str = "rule.gif"):
    frames = []
    gif.seek(0) # go to the first frame of the gif
    frame = ImageDraw.Draw(gif) # create a draw object to draw on the gif
    font = ImageFont.truetype("impact.ttf", 20) # create a font object

    lines = textwrap.wrap(text, width=int(gif.width / 20)) #we wrap the text to fit the width of the gif
    _, _, ruleWidth, _ = frame.textbbox((0, 0), f"Kural {str(ruleid)}",font=font) # calculate the width and height of the text

    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        
        newImage = []
        for item in frame.getdata():
            if item[3] == 0:
                newImage.append((54, 57, 63, 100)) # discord background color
            else:
                newImage.append(item)

        frame.putdata(newImage)

        draw = ImageDraw.Draw(frame,"RGBA")

        width = frame.width
        height = frame.height

        draw.text(((width - ruleWidth) / 2 ,10), f"Kural {str(ruleid)}" , fill="white",font=font)
        for i, line in enumerate(lines[::-1]):
            _, _, descriptionWidth, descriptionHeight = draw.textbbox((0, 0), line,font=font) # calculate the width and height of the text

            draw.text(((width - descriptionWidth) / 2 ,height - 30 - i * descriptionHeight), line, fill="white",font=font)
        frame.background = frame.convert("RGBA")

        frames.append(frame)

    frames[0].save(filename + ".gif", save_all=True, append_images=frames[1:], duration=gif.info["duration"])
    return filename + ".gif"

#image = writeText(Image.open("gokugifs/" + random.choice(gifs)),1,"adsadlas")
#os.system("rule.gif")
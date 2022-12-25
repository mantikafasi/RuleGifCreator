from PIL import Image, ImageDraw, ImageSequence,ImageFont
import random
import os
import textwrap
gifs = os.listdir("gokugifs")
strings = {
    "en": {
        "rule": "Rule ",
    },
    "tr": {
        "rule": "Kural ",
    }
}


def writeText(gif, ruleid :int , text:str,filename:str = "rule",lang = "en"):
    frames = []
    gif.seek(0) # go to the first frame of the gif
    frame = ImageDraw.Draw(gif) # create a draw object to draw on the gif
    font = ImageFont.truetype("impact.ttf", int(gif.width / 10) ) # create a font object

    lines = textwrap.wrap(text, width=int(gif.width / 20)) #we wrap the text to fit the width of the gif
    _, _, ruleWidth, _ = frame.textbbox((0, 0), f"{strings[lang]['rule']} {str(ruleid)}",font=font) # calculate the width and height of the text

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

        for x,y in [(0,1),(0,-1),(1,0),(-1,0),(0,0)]:
            draw.text(((width - ruleWidth) / 2 + x ,10 + y), f"{strings[lang]['rule']} {str(ruleid)}" , fill="white" if x == 0 and y == 0 else "black" ,font=font)
        
        for i, line in enumerate(lines[::-1]):
            _, _, descriptionWidth, descriptionHeight = draw.textbbox((0, 0), line,font=font) # calculate the width and height of the text

            for x,y in [(0,1),(0,-1),(1,0),(-1,0),(0,0)]:
                draw.text(((width - descriptionWidth) / 2 + x ,height - 5 - ((i + 1) * descriptionHeight + y)), line, fill="white" if x == 0 and y == 0 else "black",font=font)

        if frame.mode == "RGBA":
            frame.info["background"] = (54, 57, 63,0)
        else:
            frame.info["background"] = (54, 57, 63) # we hate pillow & myself
        
        frames.append(frame)

    frames[0].save(filename + ".gif", save_all=True, append_images=frames[1:],duration=gif.info["duration"],optimize = True)
    return filename + ".gif"

if __name__ == "__main__":
    gif = random.choice(gifs)
    print(gif)
    writeText(Image.open("gokugifs/" +  gif),1,"adsadlas",lang="en")
    os.system("rule.gif")

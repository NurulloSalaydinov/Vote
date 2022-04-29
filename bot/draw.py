from PIL import Image, ImageDraw, ImageFont
import random
def drawimg():
    symbols = "qw1er2ty3ui4op5asd6fgh7jkl8zxc9vbnm0"
    text = "".join(random.sample(symbols, 5))
    newimg = Image.new("RGB", (400, 150), (255, 255, 255))
    img = ImageDraw.Draw(newimg)
    font = ImageFont.truetype("font/Lemon-Regular.ttf", 70)
    img.text((75, 27), text, font=font, fill=("#184aa6"), align="center")
    # for i, z in zip(text, range(0, 11)):
    #     d.text((40 + z * 45, 20), i, font=fnt, fill=("#184aa6"), align="center")
    newimg.save("img/test.png")
    return text
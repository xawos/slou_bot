from PIL import ImageFont, Image, ImageDraw
import dbutils


def craft(topString, bottomString, filename):
    filename = "./images/" + filename
    img = Image.open(filename)
    imageSize = img.size
    fontSize = int(imageSize[1] / 5)
    # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
    font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0] - 20 or bottomTextSize[0] > imageSize[0] - 20:
        fontSize = fontSize - 1
        # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)
    topTextPositionX = (imageSize[0] / 2) - (topTextSize[0] / 2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)
    bottomTextPositionX = (imageSize[0] / 2) - (bottomTextSize[0] / 2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)
    draw = ImageDraw.Draw(img)
    outlineRange = int(fontSize / 15)
    # for x in range(-outlineRange, outlineRange+1):
    #        for y in range(-outlineRange, outlineRange+1):
    #                draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString.upper(), (0,0,0), font=font)
    #                draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString.upper(), (0,0,0), font=font)
    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)
    img.save("./images/temp.png")
    return True


def saveTemplate(templateName, filename, user):
    try:
        img = Image.open("./images/" + filename)
        img.save("./images/templates/" + templateName + ".png")
        dbutils.addMemeTemplate(img.filename, user)
        return True
    except Error as e:
        return False
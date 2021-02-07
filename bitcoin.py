# /usr/bin/python3
# bitcoin_ticker v1.0
# Naviavia - https://github.com/naviavia/bitcoin_ticker

import requests
import json
from time import sleep
from inky import InkyPHAT
import argparse
from PIL import Image, ImageFont, ImageDraw
import os
from font_fredoka_one import FredokaOne
import datetime

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

# Parsing flip arguments
parser = argparse.ArgumentParser()
parser.add_argument('--flip', '-n', type=str, help="true = screen is flipped")
args, _ = parser.parse_known_args()

#Variables
CURR_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
RESOURCES = CURR_DIR + "resources/"
TIME = datetime.datetime.now()
COURIER_FONT = RESOURCES + "fonts/Courierprime.ttf"
    
# Get bitcoin price from bitstamp API
def getBitcoinPrice():
    URL = "https://www.bitstamp.net/api/ticker/"
    try:
        r = requests.get(URL)
        priceFloat = float(json.loads(r.text)["last"])
        return priceFloat
        print(response.status_code)
    except requests.ConnectionError:
        print("API - ERROR")
        
#Check for file, if it doesn't exist create, otherwise read file
file_exists = os.path.isfile(CURR_DIR + "/" + "previousprice")

if file_exists:
    ObjRead = open(CURR_DIR + "previousprice", "r")
    PREVIOUS_PRICE = ObjRead.read();
    f = open(CURR_DIR + "previousprice", "w")
    f.write(str(getBitcoinPrice()))
    ObjRead.close()
else:
    #print ("price file not found")
    f = open(CURR_DIR + "previousprice", "w")
    f.write(str(getBitcoinPrice()))
    PREVIOUS_PRICE = str(getBitcoinPrice())

# Get price and format
BITCOINPRICE = float(getBitcoinPrice())
NUMBER_WITH_COMMAS = "{:,}".format(BITCOINPRICE)

#Flip screen is true arguement passed
if str(args) == "Namespace(flip='true')":
    inky_display.h_flip = True
    inky_display.v_flip = True

# get BTC logo
BTCLOGO = RESOURCES + "btc.png"
btcimg = Image.open(BTCLOGO)

#Compare current and previous prices & build price to display
if (float(BITCOINPRICE) >= float(PREVIOUS_PRICE)):
    BITCOINPRICE = "$" + NUMBER_WITH_COMMAS
    ICON = RESOURCES + "icon-up.png"
    iconimg = Image.open(ICON)
else:
    BITCOINPRICE = "$" + NUMBER_WITH_COMMAS
    ICON = RESOURCES + "icon-down.png"
    iconimg = Image.open(ICON)

# Create a new canvas to draw on
img = Image.open(RESOURCES + "backdrop.png").resize(inky_display.resolution)
draw = ImageDraw.Draw(img)

# load the fonts, and text size
font = ImageFont.truetype(FredokaOne, 32)
font2 = ImageFont.truetype(COURIER_FONT, 12)
font3 = ImageFont.truetype(COURIER_FONT, 24)

# Text to display and location
img.paste(btcimg, (25, 0)) 
img.paste(iconimg, (150, 7))
draw.text((72, 10), "Price", inky_display.BLACK, font=font3)
draw.text((37.5, 90), TIME.strftime('%Y-%m-%d %H:%M:%S'), inky_display.BLACK, font=font2)
message = BITCOINPRICE
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 1.5) - (h / 1.5)

# Display the text
draw.text((x, y), message, inky_display.RED, font)
inky_display.set_image(img)
inky_display.show()
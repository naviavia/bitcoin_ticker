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
COIN = "btcusdc"
CURRENCYSYMBOL = "$"
    
# Get bitcoin price from bitstamp API
def getBitcoinPrice():
    URL = "https://www.bitstamp.net/api/v2/ticker/" + COIN + "/"
    try:
        r = requests.get(URL)
        lastpriceFloat = float(json.loads(r.text)["last"])
        return lastpriceFloat
        print(response.status_code)
    except requests.ConnectionError:
       print("API - ERROR")
       
def getBitcoinPrice24Low():
    URL = "https://www.bitstamp.net/api/v2/ticker/" + COIN + "/"
    try:
        r = requests.get(URL)
        openpriceFloat = float(json.loads(r.text)["open"])
        return openpriceFloat
        print(response.status_code)
    except requests.ConnectionError:
       print("API - ERROR")

#Calculate the 24hour percentage change
def percent(a, b) : 
    result = int(((b - a) * 100) / a) 
    return result 
  
if __name__ == "__main__" : 
    a, b = float(getBitcoinPrice24Low()),float(getBitcoinPrice())
    PERCENTAGE = percent(a, b)
      
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
    BITCOINPRICE = CURRENCYSYMBOL + NUMBER_WITH_COMMAS
    ICON = RESOURCES + "icon-up.png"
    iconimg = Image.open(ICON)
else:
    BITCOINPRICE = "$" + NUMBER_WITH_COMMAS
    ICON = RESOURCES + "icon-down.png"
    iconimg = Image.open(ICON)

print("The price has changed " + str(PERCENTAGE) + "% in last 24h's")
print("The current price is " + str(CURRENCYSYMBOL) + str(NUMBER_WITH_COMMAS))

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
draw.text((80, 33), str(PERCENTAGE) + "%" + "(24h)", inky_display.BLACK, font=font2)
draw.text((20, 45), str(BITCOINPRICE), inky_display.RED, font=font)
draw.text((37.5, 90), TIME.strftime('%d-%m-%Y %H:%M:%S'), inky_display.BLACK, font=font2)


# Display the text
inky_display.set_image(img)
inky_display.show()
# /usr/bin/python3
# bitcoin_ticker v1.1
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
parser.add_argument('--flip', '-f', type=str, help="true = screen is flipped")
parser.add_argument('--pair', '-p', type=str, help="enter currency pair")
args, _ = parser.parse_known_args()

#Variables
CURR_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
RESOURCES = CURR_DIR + "resources/"
TIME = datetime.datetime.now()
COURIER_FONT = RESOURCES + "fonts/Courierprime.ttf"
API_ENDPOINT = "https://api.kraken.com/0/public/Ticker"
COIN = "XXBTZUSD"
CURRENCYEXTRACT = "USD"

#If currency pair is entered extract info
if args.pair is not None:
    COIN = str.upper(args.pair)
    CURRENCYEXTRACT = str.upper(args.pair)[-3:]
    
#Select currency based on currency pair input
if CURRENCYEXTRACT == "GBP":
    CURRENCYSYMBOL = "£"
elif CURRENCYEXTRACT == "USD":
    CURRENCYSYMBOL = "$"
elif CURRENCYEXTRACT == "EUR":
    CURRENCYSYMBOL = "€"
elif CURRENCYEXTRACT == "CAD":
    CURRENCYSYMBOL = "$"
elif CURRENCYEXTRACT == "AUD":
    CURRENCYSYMBOL = "$"

# Get current COIN price from Kraken API
def getCoinPrice():
    TICKER = API_ENDPOINT + "?pair=" + COIN
    try:
        r = requests.get(TICKER)
        json_data = r.text
        fj = json.loads(json_data)
        lastpriceFloat = fj["result"][COIN]["c"][0]
        return float(lastpriceFloat)
    except requests.ConnectionError:
        print("API - ERROR")
    
# Get low COIN price from Kraken API
def getCoinPriceLow():
    TICKER = API_ENDPOINT + "?pair=" + COIN
    try:
        r = requests.get(TICKER)
        json_data = r.text
        fj = json.loads(json_data)
        lastpriceFloat = fj["result"][COIN]["l"][0]
        return float(lastpriceFloat)
    except requests.ConnectionError:
        print("API - ERROR")

#Calculate the 24hour percentage change
def percent(a, b) : 
    result = int(((b - a) * 100) / a) 
    return result 
  
if __name__ == "__main__" : 
    a, b = float(getCoinPriceLow()),float(getCoinPrice())
    PERCENTAGE = percent(a, b)
      
#Check for file, if it doesn't exist create, otherwise read file
file_exists = os.path.isfile(CURR_DIR + "/" + "previousprice")

if file_exists:
    ObjRead = open(CURR_DIR + "previousprice", "r")
    PREVIOUS_PRICE = ObjRead.read();
    f = open(CURR_DIR + "previousprice", "w")
    f.write(str(getCoinPrice()))
    ObjRead.close()
else:
    #print ("price file not found")
    f = open(CURR_DIR + "previousprice", "w")
    f.write(str(getCoinPrice()))
    PREVIOUS_PRICE = float(getCoinPrice())

# Get price and format
COINPRICELOW = float(getCoinPriceLow())
COINPRICE = float(getCoinPrice())
NUMBER_WITH_COMMAS = "{:,}".format(COINPRICE)

#Flip screen is true arguement passed
if args.flip == "true":
    inky_display.h_flip = True
    inky_display.v_flip = True

# get BTC logo
BTCLOGO = RESOURCES + "btc.png"
btcimg = Image.open(BTCLOGO)

#Compare current and previous prices & build price to display
if (float(COINPRICE) >= float(PREVIOUS_PRICE)):
    COINPRICE = CURRENCYSYMBOL + NUMBER_WITH_COMMAS
    ICON = RESOURCES + "icon-up.png"
    iconimg = Image.open(ICON)
else:
    COINPRICE = CURRENCYSYMBOL + NUMBER_WITH_COMMAS
    ICON = RESOURCES + "icon-down.png"
    iconimg = Image.open(ICON)

print("The selected pair is " + COIN)
print("The selected currency " + CURRENCYSYMBOL + "(" + CURRENCYEXTRACT + ")")
print("The price has changed " + str(PERCENTAGE) + "% in last 24h's")
print("The low price is " + CURRENCYSYMBOL + "{:,}".format(COINPRICELOW))
print("The previous price is " + CURRENCYSYMBOL + PREVIOUS_PRICE)
print("The current price is " + str(COINPRICE))

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
draw.text((30, 45), str(COINPRICE), inky_display.RED, font=font)
draw.text((37.5, 90), TIME.strftime('%d-%m-%Y %H:%M:%S'), inky_display.BLACK, font=font2)

# Display the text
inky_display.set_image(img)
inky_display.show()
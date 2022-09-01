# bitcoin_ticker
The bitcoin ticker has been configured with the Kraken API, and refreshes the screen based on a CRON job.

## Table of contents
* [Requirements](#requirements)
* [Setup](#setup)
* [Config](#config)


## Requirements
- Raspberry Pi (all models up to Pi Zero 2 Supported as of 08/2022)
- Inky pHAT e-ink display

## Setup
- SSH/HDMI onto Pi
- Install the Inky pHAT library on the command line
```
curl https://get.pimoroni.com/inky | bash
```
- Reboot the Pi
- Download the bitcoin_ticker code to a directory
```
git clone https://github.com/naviavia/bitcoin_ticker.git
```
- Edit cron jobs
```
crontab -e
```
- Add the below entry (5 represents the frequency of the task e.g. updating to 1 will run every minute, add running variables if required to switch currencies or keep the screen flipped)
```
*/5 * * * * python3 /home/pi/bitcoin_ticker/bitcoin.py
```
Make sure the above path is pointing to the folder you've downloaded the code to

## Config
- To flip the display add the below argument;

```
--flip true
```

- To use an alternative Coin/Currency enter the pair & currency below e.g. ADA - GBP. This is based on available pairs on Kraken.

```
--pair adagbp
```
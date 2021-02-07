# bitcoin_ticker
The bitcoin ticker has been configured with the Bitstamp BTC API, and refreshes the screen based on a CRON job.

## Table of contents
* [Requirements](#requirements)
* [Setup](#setup)

## Requirements
- Raspberry Pi
- Inky pHAT e-ink display

## Setup
- SSH onto Pi
- Install the Inky pHAT libary on the command line
```
curl https://get.pimoroni.com/inky | bash
```
- Reboot the Pi
- Download the bitcoin_ticker code to any directory
```
https://github.com/naviavia/bitcoin_ticker.git
```
- Edit cron jobs
```
crontab -e
```
- Add the below entry (5 represents the frequency of the task e.g. updating to 1 will run every minute)
```
*/5 * * * * python3 /home/pi/bitcoin_ticker/bitcoin.py
```

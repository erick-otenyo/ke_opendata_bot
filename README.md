# Kenya Open Data Search Telegram Bot
A Telegram bot that lets you search data from Kenya Open Data, www.opendata.go.ke

## Requirements
* [Python 3.5](http://www.python.org)
* [Telepot](https://github.com/nickoala/telepot)
* [aiohttp](https://github.com/KeepSafe/aiohttp)


## Configuration
You must edit `opendata.py` before running the bot.

You need to provide:
* a valid [Telegram Bot](https://core.telegram.org/bots) authentication token

## Quick Start

When the configuration is complete you can install the dependencies with:

    $ pip install  aiohttp telepot

And run the bot with:

    $ python bot.py
    
 ## Usage
With the bot running you can send him a text of the title of the dataset to search, and it will respond with a list of the datasets found.

Then it provides buttons for downloading a CSV copy of the data. A download shapefile button  will aslo appear if the dataset is a spatial dataset, for mapping purposes.

I only tested with a few dataset and it works fine. Future improvements and fixes to follow. Cheers

## License
This project is licensed under the terms of the **MIT** license.

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import requests
import asyncio
import json
import numpy as np
import pandas as pd
from datetime import timedelta, date, datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#import tracemalloc

#import iexdiscordbot.helper.closingpricehelper as cphelp

from iexdiscordbot.helper.indicators.volatility.bollingerbands import LowerBand, MiddleBand, HigherBand
#from iexdiscordbot.helper.movingaverage import typicalPriceHelper
#from iexdiscordbot.helper.indicators.volatility.bollingerbands import MiddleBand
"""IEX Variables[Sandbox/Stable]"""

load_dotenv()
IEX_API_KEY = os.getenv('IEX_API_KEY')
base_url = 'https://sandbox.iexapis.com/'
version = 'stable/'

"""Asyncio Declaration"""
loop = asyncio.get_event_loop()

"""This is the long way of writing commands"""
class bb(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('BB Command Loaded')

#Calculate RSI Here
    @commands.command()
    async def bb(self, ctx, *, message):

        #CCI = ([(highest + lowest + close)/3] - n Moving Average of M) / (0.015 * mean deviation between the mean price and moving average of mean prices)
        api_call = f'{base_url+version}stock/{message}/chart/3m?token={IEX_API_KEY}'
        requestHistoricalPrices = requests.get(api_call)
        dataHistoricalPrices = requestHistoricalPrices.json()
        data = pd.DataFrame(dataHistoricalPrices)

        #print(f'{data}')

        sma = 'sma'
        ema = 'ema'
        smoothtype = sma
        method = 'hlc3'
        n = 10
        #typicalPrice = typicalPriceHelper(data, method)
        #print(f'cogs/bollingerbands typicalPrice: {typicalPrice}')
        lowerband = LowerBand(data, smoothtype, n, method)
        middleband = MiddleBand(data, smoothtype, n, method)
        higherband = HigherBand(data, smoothtype, n, method)
        # LowerBand(data, ema, 10)
        # MiddleBand(data, ema, 10)
        # HigherBand(data, ema, 10)
        print(f'lowerband: {lowerband[0:30]}\n middleband: {middleband[0:30]}\n higherband: {higherband[0:30]}')

        date = data['date']
        lenDate = len(date)
        lenLower = len(lowerband)
        lenMiddle = len(middleband)
        lenHigher = len(higherband)
        print(f'date length = {lenDate}')
        print(f'lowerband length = {lenLower}')
        print(f'middleband length = {lenMiddle}')
        print(f'higherband length = {lenHigher}')
        plt.plot(date[9:], lowerband[9:], label = 'lowerband')
        plt.plot(date[9:], middleband[9:], label = 'middleband')
        plt.plot(date[9:], higherband[9:], label = 'higherband')
        plt.ylabel('bollingerbands')
        plt.xlabel('Date')
        plt.savefig('bollingerbands.jpg')
        plt.close()
        file = discord.File('bollingerbands.jpg')





        #BOLD = pd.Series(typicalPrice.rolling(20).mean() - )
        #data = data.join(CCI)
        #print(f'{typicalPrice} \n {BOLU} \n {BOLD}')
        embed = discord.Embed(
            title=message,
            #description=f'latest price: {latestPrice}.join, changePercent : {changePercent}',
            description=''.join(f'lowerband: {lowerband[-5:]}\n middleband: {middleband[-5:]}\n higherband: {higherband[-5:]}'),
            colour=discord.Color.green()
            )
        embed.set_image(url='attachment://bollingerbands.jpg')
        #await ctx.send(embed=embed)
        await ctx.send(file = file, embed=embed)

def setup(client):
    client.add_cog(bb(client))

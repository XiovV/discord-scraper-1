#! /usr/bin/python3
from discord.ext import tasks, commands
from discord import Webhook, AsyncWebhookAdapter
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import asyncio
import discord
import json
import time 
import os
import aiohttp

# pylint: disable=E0602

# This checks for the config.json file and handles it accordingly.
try:
    config = open("config.json")
except FileNotFoundError:
    print("ERROR: The config.json not accessible. Check README.md")
    exit()
finally:
    config = json.load(config)
    globals().update(config)

# pylint: disable=E0602
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background.start()
        self.runs = 0

    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="fit.ba/student"))
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        
    @tasks.loop(seconds=120)
    async def background(self):
        global data, headers, channelID
        self.runs += 1

        # Gets the dynamic header data.
        with requests.Session() as r:
            r = r.get('https://www.fit.ba/student/login.aspx')
            soup = BeautifulSoup(r.text, "lxml")
            data["__VIEWSTATE"] = soup.find("input", {"id": "__VIEWSTATE"})['value']
            data["__VIEWSTATEGENERATOR"] = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})['value']
            data["__EVENTVALIDATION"] = soup.find("input", {"id": "__EVENTVALIDATION"})['value']

        # Logs in and gets the title.
        with requests.Session() as s:
            s.post('https://www.fit.ba/student/login.aspx', headers=headers, data=data)
            s = s.get('https://www.fit.ba/student/default.aspx')
            soup = BeautifulSoup(s.text, "lxml")
            _title = soup.find("a", {"id": "lnkNaslov"})
            title = _title.text

        # Checks if there is a description preview.
        try:
            short_description = soup.find("div", {"class": "abstract"}).text
        except:
            short_description = False

        channel = await self.fetch_channel(channelID)
        msg = await channel.history(limit=1).flatten()
        msg = msg[0]
        embeds = msg.embeds
        for embed in embeds:
            old_embed = embed.to_dict()

        # Checks if it's the same post. If no, proceed.
        if old_embed["title"] != title:
            print(f"[{self.runs}] Different title. Posting new message...")
            article_url = f"https://www.fit.ba/student/{_title['href']}"
            with requests.Session() as o:
                o.post('https://www.fit.ba/student/login.aspx', headers=headers, data=data)
                o = o.get(article_url)
            soup = BeautifulSoup(o.text, "lxml")
            try:
                content = "".join([i.text for i in soup.find("div", {"id": "Panel1"}).find_all("p")])
            except:
                content = False
            author = soup.find("a", {"id": "linkNapisao"}).text
            date = soup.find("span", {"id": "lblDatum"}).text

            # Some fancy date formatting and OS checking.
            if os.name == "nt":
                date = datetime.strptime(date, '%d.%m.%Y %H:%M -').strftime('%#d. %B, %Y at %H:%M')
            else:
                date = datetime.strptime(date, '%d.%m.%Y %H:%M -').strftime('%-d. %B, %Y at %H:%M')

            # I didn't want to rewrite the code to adapt it to BS4, so I just kept it as a dict.
            postData = {"content": content,
                    "title": title, 
                    "author": author,
                    "article_url": article_url,
                    "short_description": short_description,
                    "date": date
                    }
            
            # This basically makes the bot do things.
            if "content" == False:
                noPostDescription = "Obavijest nema teksta. Kliknite na naslov da otvorite u browser-u."
                embed=discord.Embed(title=postData["title"], url=postData["article_url"], description=noPostDescription, color=0xf6f6f6)
            elif len(postData["content"])>2000:
                if "short_description" != False:
                    description = f"{postData['short_description']} \n\nPoruka preduga. Otvorite u browseru."
                else:
                    description = "\n\nPoruka preduga. Otvorite u browseru."

                embed=discord.Embed(title=postData["title"], url=postData["article_url"], description=description, color=0xf6f6f6)
            else:
                embed=discord.Embed(title=postData["title"], url=postData["article_url"], description=postData["content"], color=0xf6f6f6)

            author = postData["author"].split()[0]
            if author in avatars:
                icon = avatars[author]
            else:
                 icon = avatars["default"]

            # Attribution. Please keep it here, thanks.
            embed.set_footer(text=f"Posted on {postData['date']}  |  github.com/omznc/discord-scraper")

            if thumbnail:
                embed.set_thumbnail(url=thumbnail)
            
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
                await webhook.send(content="<@&796116996000579644>", embed=embed, username=postData["author"], avatar_url=icon)
            
            print("Message succesfully sent.")

        else:
            print(f"[{self.runs}] Same title, skipping...")
        
    @background.before_loop
    async def before_loop(self):
        print("Waiting until the bot initializes...")
        await self.wait_until_ready()

client = MyClient()
client.run(token)



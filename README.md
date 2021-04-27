# Just your normal scraping bot, written in Python.

<a href="https://discord.gg/vZRrpBXFNT"><img src="https://img.shields.io/discord/787773373748740128?label=Discord%20Server&style=for-the-badge"></img></a>
<br><br>

This is a bot that scrapes www.fit.ba/student/ and sends the latest post to a channel in our server.

## If for some reason you want to use it, this is how.

1. Run 
```sh
 git clone https://github.com/omznc/discord-scraper.git
```
2. Edit `/config/config.json`:
   * `token` - Bot token.
   * `channelID` - Channel to send the message to.
   * `txtBrojDosijea` - Username.
   * `txtLozinka` - Password.
   * `thumbnail` - (Optional) Embed photo.
3. Move `config.json` to the root directory.
4. Install requirements with:
```sh
pip install -r requirements.txt
```
5. Run using:
```sh
python3 bot.py
```
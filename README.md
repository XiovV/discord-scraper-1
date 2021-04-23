# Just your normal scraping bot, written in Python.

<a href="https://discord.gg/vZRrpBXFNT"><img src="https://img.shields.io/discord/787773373748740128?label=Discord%20Server&style=for-the-badge"></img></a>
<br><br>

This is a bot that scrapes www.fit.ba/student/ and sends the latest post to a channel in our server.

## If for some reason you want to use it, this is how.

1. Run 
```sh
 git clone https://github.com/omznc/discord-scraper.git
```
2. Go to <a href="https://www.fit.ba/student/login.aspx">fit.ba/student/</a>.
3. Get POST data:
   * Open the Network tab in Inspect Element, then log-in.
   * Right click on the first POST request, then copy as cURL.

4. Paste that boy in <a href="https://curl.trillworks.com/">curl.trillworks.com/</a>.
5. Edit `/config/config.json`:
   * Fill in `token`, `thumbnail`, `channelID`
   * Using step 4, do the same for `__VIEWSTATE`, `__VIEWSTATEGENERATOR`, `__EVENTVALIDATION`, `txtBrojDosijea`, and `txtLozinka`.
6. Move `config.json` to the root directory.
7. Install requirements with:
```sh
pip install -r requirements.txt
```
8. Run using:
```sh
python3 start.py
```
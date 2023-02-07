from webex_bot.webex_bot import WebexBot
from webex import checkStatus

import os

webex_token = os.environ["WEBEX_BOT_TOKEN"]
bot = WebexBot(webex_token, approved_domains=["hccs.edu"])

bot.add_command(checkStatus())

bot.run() 
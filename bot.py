from webex_bot.webex_bot import WebexBot
from webex import checkStatus

import os

# Add "WEBEX_BOT_TOKEN" to your Windows Environmental Variables. 
webex_token = os.environ["WEBEX_BOT_TOKEN"]

# Add whatever Domain you want to secure your bot to, in the "approved domains" field
bot = WebexBot(webex_token, approved_domains=["hccs.edu"])

bot.add_command(checkStatus())

bot.run() 
import json
import logging
import os
import requests
from webex_bot.models.command import Command
from webex_bot.models.response import Response
from adaptivecardbuilder import *


webex_token = os.environ["WEBEX_BOT_TOKEN"]
access_token = "ZTM5OTliZWMtNTM3MC00M2MwLWI2ODMtMzg5YTU0ZTYzN2EyNmM3MGYwNjMtNDgz_PF84_84afd2ff-3a95-48f3-8746-17a816f97a4f"
##print(webex_token)
log = logging.getLogger(__name__)

with open("./input-card.json", "r") as card:
    INPUT_CARD = json.load(card)

class checkStatus(Command):
    def __init__(self):
        super().__init__(
            command_keyword="check",
            help_message="Check if HCC Webex account exists",
            card=INPUT_CARD,
        )

    def execute(self, message, attachment_actions, activity):

        facultyEmail = attachment_actions.inputs['faculty_email']
        print(f"This is the {facultyEmail} being used")
        url = f"https://webexapis.com/v1/people?email={facultyEmail}"
        headers = {'Authorization' : 'Bearer ZTM5OTliZWMtNTM3MC00M2MwLWI2ODMtMzg5YTU0ZTYzN2EyNmM3MGYwNjMtNDgz_PF84_84afd2ff-3a95-48f3-8746-17a816f97a4f'}

        print(url)
        #Query Webex for user
        response = requests.request("GET", url, headers=headers)
        webexUser = response.json()
        print(webexUser)
        
        if len(webexUser['items']) == 0:
            firstName       =   "N/A"
            lastName        =   "N/A"
            displayName     =   "N/A"
            email           =   "N/A"
            created         =   "N/A"
            status          =   "N/A"
            lastActivity    =   "N/A"
            avatar          = "https://cdn0.iconfinder.com/data/icons/interface-set-vol-2/50/No_data_No_info_Missing-512.png"            
        else:
            firstName       =   webexUser['items'][0]['firstName']
            lastName        =   webexUser['items'][0]['lastName']
            displayName     =   webexUser['items'][0]['displayName']
            email           =   webexUser['items'][0]['emails'][0]
            created         =   webexUser['items'][0]['created']
            status          =   webexUser['items'][0]['status']
            try:
                lastActivity    =   webexUser['items'][0]['lastActivity']
            except KeyError:
                lastActivity    =   "NEVER"

            try:
                avatar          =   webexUser['items'][0]['avatar']           
            except KeyError:
                avatar          = "https://cdn0.iconfinder.com/data/icons/interface-set-vol-2/50/No_data_No_info_Missing-512.png"                  
        print("card Start")
        card = AdaptiveCard()
        card.add(TextBlock(text=f"HCC User: {displayName}", size="Medium", weight="Bolder"))
        card.add(ColumnSet())
        card.add(Column(width="stretch"))
        card.add(FactSet())
        card.add(Fact(title="First", value=f"{firstName}")) 
        card.add(Fact(title="Last", value=f"{lastName}"))
        card.add(Fact(title="Email", value=f"{email}"))
        card.add(Fact(title="Created", value=f"{created}"))
        card.add(Fact(title="Status", value=f"{status}"))
        card.add(Fact(title="Last Activity", value=f"{lastActivity}"))
        card.up_one_level()
        card.up_one_level()
        card.add(Column(width="automatic"))
        card.add(Image(url=avatar, size="medium"))
        card_data = json.loads(asyncio.run(card.to_json()))

        print("after Card Data")
        print("finally start")
        card_payload = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card_data,
        }

        # Build card response
        response = Response()
        # Fallback text
        response.text = "Test Card"
        # Attachments being sent to user
        response.attachments = card_payload

        return response

       #Query Webex for user
        response = requests.request("GET", url, headers=headers)
        webexUser = response.json()
        print(response.text)
        print(response.status_code)
        card = AdaptiveCard()
        try:
            #Pull out desired info
            firstName       =   webexUser['items'][0]['firstName']
            lastName        =   webexUser['items'][0]['lastName']
            displayName     =   webexUser['items'][0]['displayName']
            email           =   webexUser['items'][0]['emails'][0]
            created         =   webexUser['items'][0]['created']
            status          =   webexUser['items'][0]['status']
            lastActivity    =   webexUser['items'][0]['lastActivity']
            print("lastActivity")
            try:
                avatar          =   webexUser['items'][0]['avatar']
                print("avatar try")
            except KeyError:
                avatar = "https://cdn0.iconfinder.com/data/icons/interface-set-vol-2/50/No_data_No_info_Missing-512.png"
                print("avatar except")
            print("card Start")
            card.add(label(text=f"HCC User: {displayName}", size="Medium", weight="Bolder"))
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
        except Exception:
            print("exception start")
#           card2.add(TextBlock(text=f"HCC User: does Not Exist", size="Medium", weight="Bolder"))
#           card_data = json.loads(asyncio.run(card2.to_json()))
            print("exception end")
        finally:
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

#Made for finding collectibleItemInstanceId if you know the UIAD by api_cats :3
#I dont recommend this method if you want to mass send trades. There are easier and better ways (trades.roblox.com/v2/users/USERID/tradableitems?sortBy=CreationTime).

import aiohttp
import asyncio

#If you dont want to type itemID u can webscrape Rolimons UAID page :P
item_id = int(input("Enter Item ID: "))
looked_uaid = int(input("Enter UAID: "))

async def function():
    async with aiohttp.ClientSession() as session2:
        print(f"Checking: '{item_id}' For UAID: '{looked_uaid}'")
        cursor = None
        page_numer = 1
        try:
            async with session2.get(f"https://inventory.roblox.com/v2/assets/{item_id}/owners?limit=100&sortOrder") as ol_request: #?limit=100&sortOrder
                ol_json = await ol_request.json()
                if ol_json.get("data"):
                    print(f"Checking page: {page_numer}")
                    page_numer += 1
                    cursor = ol_json["nextPageCursor"]
                    data = ol_json["data"]
                    for item in data:
                        uaid = item["id"]
                        if uaid == looked_uaid:
                            print("FOUND!:", item["collectibleItemInstanceId"])
                            input("")
                            input("")
                            return
                    print("Not found")
                else:
                    print("### ERROR!",ol_json, ol_request)
                while True:
                    if cursor is not None:
                        try:
                            await asyncio.sleep(4)
                            async with session2.get(f"https://inventory.roblox.com/v2/assets/{item_id}/owners?limit=100&sortOrder&cursor={cursor}") as ol_request: 
                                ol_json = await ol_request.json()
                                print(f"Checking page: {page_numer}, Cursor: {cursor}")
                                page_numer += 1
                                if ol_json.get("data"):
                                    cursor = ol_json["nextPageCursor"]
                                    data = ol_json["data"]
                                    for item in data:
                                        uaid = item["id"]
                                        if uaid == looked_uaid:
                                            print("FOUND!:", item["collectibleItemInstanceId"])
                                            input("")
                                            input("")
                                            return
                                    print("Not found")
                                else:
                                    print("### ERROR!",ol_json, ol_request)
                                    await asyncio.sleep(15)
                        except Exception as e:
                            print("### ERROR!: ", e)
                            await asyncio.sleep(30)
                    else:
                        print("Cursor not found!")
                        break 
        except Exception as e:
            print("### ERROR!: ",e)
            await asyncio.sleep(30)

asyncio.run(function())

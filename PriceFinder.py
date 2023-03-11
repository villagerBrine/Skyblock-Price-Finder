import requests
total_price_of_instant_buy = 0
total_price_of_buy_order = 0
pages = 100
#add reforges as needed bc I dont want to
#gives current prices for certain items, may want different algorithms
# should have named it things_to_purge_from_name
list_of_removeable_items = [" ✪", "✪", "➊","➋", "➌", "➍", "➎", 
    "Hasty ", "Heroic ", "Suspicious ", "Ancient ", "Rapid ", "Fierce ", "Withered ", "Fabled ", "Necrotic ", "Giant ", 
    "Heavy ", "Warped ", "Gentle ", "Odd ", "Fast ", "Fair ", "Epic ", "Sharp ", "Heroic ", "Spicy ", "Legendary ", 
    "Dirty ", "Gilded ", "Bulky ", "Salty ", "Treacherous ", "Stiff ", "Lucky ", "Deadly ", "Fine ", "Grand ",
    "Rapid ", "Unreal ", "Awkward ", "Rich ", "Precise ", "Precise ", "Headstrong ", "Clean ", "Light ", "Mythic ",
    "Pure ", "Smart ", "Titanic ", "Wise ", "Perfect ", "Spiked ", "Renowned ", "Cubic ", "Hyper ", "Reinforced ", 
    "Loving ", "Ridiculous ", "Empowered ", "Jaded ", "Double-Bit ", "Lumberjack's ", "Great ", "Rugged ", "Lush ", "Green Thumb ",
    "Peasant's ", "Robust ", "Zooming ", "Unyielding ", "Prospector's ", "Excellent ", "Sturdy ", "Fortunate ", "Moil ", "Toil ", 
    "Blessed ", "Bountiful ", "Magnetic ", "Fruitful ", "Refined ", "Stellar ", "Mithraic ", "Auspicious ", "Fleet ", "Heated ",
    "Ambered", "Waxed ", "Fortified ", "Strengthened ", "Glistening ", "Enchanted Book Enchanted Book ", "§d§l", "§9", "§7",  "§l"]
#CREATES 200n SITUATION
pet_level = ["[Lvl " + str(x) + "] " for x in range(200)]
for i in pet_level:
    list_of_removeable_items.append(i)
color_code = "\033["
print(color_code + "0;32mvillagerBrine presents Money Maker!")
print(color_code + "0;31mCAUTION! PRICES MAY BE WRONG! PLEASE LOOK AT THE PRICES ON SKYBLOCK BEFORE DOING ANY FLIPS! ")
print("THIS TOOL IS TO BE USED TO FIND THE HIGHEST MONITARY GAIN FLIP!")

def prices_look_nice(price):
    if price >= 1000000000 or price <= -1000000000: 
        return str(round(float(price/1000000000), 2)) + "b coins"
    if price >= 1000000 or price <= -1000000: 
        return str(round(float(price/1000000), 2)) + "m coins"  
    if price >= 1000 or price <= -1000: 
        return str(round(float(price/1000), 2)) + "k coins"
    return str(round(price, 2)) + " coins"
    
def get_auction_format():
    data = requests.get( url = "https://api.hypixel.net/skyblock/auctions",  params = {"page":0}).json()
    for i in data:
        print("• " + str(i))
    for d in data['auctions'][0]:
        print("    ○ " + str(d))
def load_list():
    data = requests.get( url = "https://sky.shiiyu.moe/api/v2/bazaar").json()
    print(color_code + "2;0mLoaded " + str(len(data)) + " bazaar items!")
    return data
def simplify_api():
    api_data = load_list()
    simplified_data = {}
    for key in api_data:
        data = {}
        data["buy_price"] = api_data[key]["buyPrice"]
        data["sell_price"] = api_data[key]["sellPrice"]
        simplified_data[api_data[key]["name"]] = data
    return simplified_data
def total_price():
    global total_price_of_instant_buy
    global total_price_of_buy_order
    print("Instant Buy: " + prices_look_nice(total_price_of_instant_buy) + ": Buy Order: " + prices_look_nice(total_price_of_buy_order))
    total_price_of_buy_order = 0 
    total_price_of_instant_buy = 0
def load_auctions():
    global pages
    list_of_bin_auctions = []
    try:
        for i in range(pages):
            list_of_auctions = []
            data = requests.get( url = "https://api.hypixel.net/skyblock/auctions",  params = {"page":i}).json()
            auctions = data["auctions"]
            for auction in auctions:
                if (auction['bin']):
                    list_of_bin_auctions.append(auction)
        print("Change the pages variable to a higher number and restart the program")
        return ["this isnt working"]
    except KeyError:
        a_random_variable = 0
    print("Loaded " + str(len(list_of_bin_auctions)) + " bin auctions!")
    return list_of_bin_auctions
def check_auctions():
    global list_of_removeable_items
    list_of_bin_auctions = load_auctions()
    prices = {}
    list_of_lore = {}
    for bin_auction in list_of_bin_auctions:
        name = bin_auction['item_name']
        extra = bin_auction['extra']
        item_lore = bin_auction['item_lore']
        for item in list_of_removeable_items:
            if (item in bin_auction['item_name']):
                name = name.replace(item, "")
            if (item in bin_auction['extra']):
                extra = extra.replace(item, "")
            if (item in bin_auction['item_lore']):
                item_lore = item_lore.replace(item, "")
        if ('Enchanted Book' in bin_auction['item_name']):
            name = ""
            list_of_enchants = {" IV":4, " III":3, " II":2,  " I":1, " VIII":8, " VII":7, " VI":6, " V":5, " XI":9, " X":10}  
            lore = []
            for i in list_of_enchants:
                item_lore = item_lore.replace(i,  " " + str(list_of_enchants[i]) + "|")
            lore = [x for x in item_lore.splitlines()]
            for i in lore:
                if '|' in i: 
                    i = i.replace("|", "")
                    if (extra in i):
                        name = name + i
        if (not name in prices):
            list_of_lore[name] = []
            prices[name] = []
        list_of_lore[name].append("\n" + bin_auction['item_name'] + "\n\n"  + bin_auction['item_lore'])
        prices[name].append(bin_auction['starting_bid'])
    print("All bin auctions searched!")
    for name in prices:
        for i in range(len(prices[name])):
            for j in range(i + 1, len(prices[name])):
                 if prices[name][i] > prices[name][j]:
                    list_of_lore[name][i], list_of_lore[name][j] = list_of_lore[name][j], list_of_lore[name][i]
                    prices[name][i], prices[name][j] = prices[name][j], prices[name][i]
   #     print(name + ":" + str([prices_look_nice(x) for x in prices[name]]))
        
    return [prices, list_of_lore]
#LOADS BIN PRICES DO NOT DELETE
simplified_data = simplify_api()
test_bin_prices = check_auctions()
lowest_bin_prices = test_bin_prices[0]
lowest_bin_lore = test_bin_prices[1]
# make lore_of_item a list
def item_lore_search(name_of_item, lore_of_item):
    global lowest_bin_prices, lowest_bin_lore
    price_list = []
    for i in lowest_bin_prices[name_of_item]:
        price_list.append(i)
    for i, item in enumerate(lowest_bin_lore[name_of_item]):
        for j in lore_of_item:
            if not j in item and lowest_bin_prices[name_of_item][i] in price_list:
                price_list.remove(lowest_bin_prices[name_of_item][i])
    try:
        print(name_of_item + " " + str(lore_of_item) + ": " + prices_look_nice(price_list[0]))
    except:
        print("fatal error")
        
def price_of_all_items_in_market(name_of_item):
    price = 0
    for increase in range(len(lowest_bin_prices[name_of_item])):
        price += lowest_bin_prices[name_of_item][increase]
    print(name_of_item + ': Market Value: ' + prices_look_nice(price) + ": Amount: " + str(len(lowest_bin_prices[name_of_item])))
    return price

def request_player_auctions_prices(player_name):
    player_uuid = requests.get(url = "https://api.mojang.com/users/profiles/minecraft/" + player_name).json()['id']
    request = requests.get( url = "https://api.hypixel.net/skyblock/auction?key=2a119251-dde7-4c39-b720-f4aa6f643972&player=" + player_uuid).json()
    total_up = [request['auctions'][x]['starting_bid'] for x in range(len(request['auctions']))]
    total = 0;
    sold_up = [request['auctions'][x]['highest_bid_amount'] for x in range(len(request['auctions']))]
    for i in total_up:
        total += i;
    sold = 0;
    for i in sold_up:
        sold += i;
    print("Total: " + prices_look_nice(total) + ": Sold:" + prices_look_nice(sold))
def request_player_auctions(player_name):
    player_uuid = requests.get(url = "https://api.mojang.com/users/profiles/minecraft/" + player_name).json()['id']
    request = requests.get( url = "https://api.hypixel.net/skyblock/auction?key=2a119251-dde7-4c39-b720-f4aa6f643972&player=" + player_uuid).json()
    name_list = [request['auctions'][x]['item_name'] for x in range(len(request['auctions']))]
    bought_list = [not (request['auctions'][x]['bids'] == []) for x in range(len(request['auctions']))]
    print([name_list[x] + ': ' + str(bought_list[x]) for x in range(len(name_list))])
def request_item(name_of_item, amount_of_item, want_price = True, algorithm = False):
    global total_price_of_instant_buy
    global total_price_of_buy_order
    global simplified_data 
    global lowest_bin_prices
    if name_of_item in simplified_data:
        instabuy_price = simplified_data[name_of_item]["buy_price"] * amount_of_item
        buy_order_price = simplified_data[name_of_item]["sell_price"] * amount_of_item
        total_price_of_instant_buy += instabuy_price
        total_price_of_buy_order += buy_order_price
        if (want_price):
            print(name_of_item + ": Instant Buy: " + prices_look_nice(instabuy_price) + ": Buy Order: " + prices_look_nice(buy_order_price))
    elif name_of_item in lowest_bin_prices:
        price = 0
        if (algorithm):
            if (amount_of_item <= len(lowest_bin_prices[name_of_item])):
                for increase in range(amount_of_item):
                    price += lowest_bin_prices[name_of_item][increase]
            else:
                for increase in range(len(lowest_bin_prices[name_of_item])):
                    price += lowest_bin_prices[name_of_item][increase]
                price += lowest_bin_prices[name_of_item][-1] * (amount_of_item - len(lowest_bin_prices[name_of_item]))
                print('There are not enough of ' + name_of_item + ' on the auction house!')
        else:
            price += lowest_bin_prices[name_of_item][0] * amount_of_item
        total_price_of_instant_buy += price
        total_price_of_buy_order += price
        if (want_price):
            print(name_of_item + ": Price: " + prices_look_nice(price))
    else:
        print("Did not work! Either you wrote something thats not on the auction or this program is stupid.")
def get_bin_lore(name_of_item, n = 0):
    global lowest_bin_lore
    global lowest_bin_prices
    list_of_color_values = ["§6", "§c", "§d", "§8", "§8", "§k", "§r", "§e", "§b", "§a", "§3", "§4", "§5", "§f", "§l", "§7", "§9"]
    for i in list_of_color_values:
        lowest_bin_lore[name_of_item][n] = lowest_bin_lore[name_of_item][n].replace(i, "")
    print(lowest_bin_lore[name_of_item][n])
    print(prices_look_nice(lowest_bin_prices[name_of_item][n]))
def clear_price():
    global total_price_of_instant_buy
    global total_price_of_buy_order
    total_price_of_instant_buy = 0
    total_price_of_buy_order = 0
# Realistic prices are being tested, not just a multiplication of lb
# Use clear_price() to delete the prices up until then
# Use total_price() to get total price (both buy order and instant buy)
# Use request_item(Item, amount, display_price(bool), algorithm_type(bool)) to get price for a certain amount of goods
# print(thing_to_display) 
# price_of_all_items_in_market(item) gets value of all items in market
# get_lowest_bin_lore(item) gets lowest bin's lore/highest bin (get_highest_bin_lore(item))
# request_player_auctions(player_name) checks for all of the players auctions and detects if they have been bought or not
# item_lore_search(item_name, [needed lore])

request_item("Necron's Handle", 1)
request_item("Wither Shield", 1)
request_item("Shadow Warp", 1)
request_item("Implosion", 1)
total_price()
request_item("Gold Gift Talisman", 1)
request_item("Hegemony Artifact", 1)


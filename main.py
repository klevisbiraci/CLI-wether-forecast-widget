import os
import sys
import argparse
import requests
import time
import curses
from curses import wrapper
from dotenv import load_dotenv
#ascii art icons used to represend the wether
sunny = "  \   /\n\
   .-.\n\
--(   )--\n\
   '-'\n\
  /   \\"

mostlSunny ="  \__/\n\
 _/  \\.-.\n\
  \_ (   ).\n\
  / (___(__)"

cloudy = "    .-.   \__/\n\
  .(  .-. /  \_\n\
 (___(   ). _/\n\
    (___(__) \\"

overcast = "    .-.\n\
   (   ).\n\
  (___(__)"

fog = " _ \" _ \" _ \"\n\
  _ \" _ \" _ \" _\n\
 _ \" _ \" _ \"  "

rain = "    .-.\n\
  .(  .-. \n\
 (___(   ).\n\
 / /(___(__)\n\
 / / / / / /"

thunderStorm = "    .-.\n\
  .(  .-. \n\
 (___(   ).\n\
    (___(__)\n\
     /_ /\n\
       |/"

snow = "    .-.\n\
  .(  .-. \n\
 (___(   ).\n\
  * (___(__)\n\
 * * * * * "

night = "     _..._\n\
   /' .-'`\n\
  |  |\n\
  \  \\\n\
   '._'-._"

cloudyNight = "          _.._\n\
    .-..'  -'   \n\
  .(  .-. (\n\
 (___(   ).'-_\n\
    (___(__) "

rainyNight = "          _.._\n\
    .-..'  -'   \n\
  .(  .-. (\n\
 (___(   ).'-_\n\
 / /(___(__) \n\
 / / / / / "

NthunderStorm = "          _.._\n\
    .-..'  -'   \n\
  .(  .-. (\n\
 (___(   ).'-_\n\
    (___(__) \n\
      /_ /\n\
       |/ "

snowyNight = "          _.._\n\
    .-..'  -'   \n\
  .(  .-. (\n\
 (___(   ).'-_\n\
  * (___(__) \n\
 * * * * * "

current = "                                   __                   __  __   \n\
  _______  _______________  ____  / /_   _      _____  / /_/ /_  ___  _____ \n\
 / ___/ / / / ___/ ___/ _ \/ __ \/ __/  | | /| / / _ \/ __/ __ \/ _ \/ ___/ \n\
/ /__/ /_/ / /  / /  /  __/ / / / /_    | |/ |/ /  __/ /_/ / / /  __/ /     \n\
\___/\__,_/_/  /_/   \___/_/ /_/\__/    |__/|__/\___/\__/_/ /_/\___/_/       "

hourly = "    __                     __         ____                                __\n\
   / /_  ____  __  _______/ /_  __   / __/___  ________  _________ ______/ /_\n\
  / __ \/ __ \/ / / / ___/ / / / /  / /_/ __ \/ ___/ _ \/ ___/ __ `/ ___/ __/\n\
 / / / / /_/ / /_/ / /  / / /_/ /  / __/ /_/ / /  /  __/ /__/ /_/ (__  ) /_  \n\
/_/ /_/\____/\__,_/_/  /_/\__, /  /_/  \____/_/   \___/\___/\__,_/____/\__/  \n\
                         /____/"

daily = "                     __   __         ____                                __\n\
 _      _____  ___  / /__/ /_  __   / __/___  ________  _________ ______/ /_\n\
| | /| / / _ \/ _ \/ //_/ / / / /  / /_/ __ \/ ___/ _ \/ ___/ __ `/ ___/ __/\n\
| |/ |/ /  __/  __/ ,< / / /_/ /  / __/ /_/ / /  /  __/ /__/ /_/ (__  ) /_  \n\
|__/|__/\___/\___/_/|_/_/\__, /  /_/  \____/_/   \___/\___/\__,_/____/\__/  \n\
                        /____/"
#used by the --daily feature to reset the summary string after its done scrolling 
def reset(i, limit):
  if i % limit == 0:
    return 0
  
  else:
    return i 
#used to choose a wether icon corresponding to the wether information gotten by any request
def iconChooser(iconNR):
  icon = ""

  if iconNR == 2:
    icon = sunny

  elif iconNR == 3 or iconNR == 4:
    icon = mostlSunny

  elif iconNR == 5 or iconNR == 6:
    icon = cloudy

  elif iconNR == 7 or iconNR == 8:    
    icon = overcast

  elif iconNR == 9:
    icon = fog
    
  elif iconNR == 10 or iconNR == 11 or iconNR == 12 or iconNR == 13:
    icon = rain

  elif iconNR == 14 or iconNR == 15:
    icon = thunderStorm

  elif iconNR in range(16, 26):
    icon = snow

  elif iconNR == 26:
    icon = night

  elif iconNR in range(27, 32):
    icon = cloudyNight

  elif iconNR == 32:
    icon = rainyNight  

  elif iconNR == 33:
    icon = NthunderStorm

  elif iconNR in range(34, 37):
    icon = snowyNight

  else:
    icon = "not available"

  return icon  
#at index 0 is the url used to send a request to validate if the place entered is valid,
#at index 1 is the url used to actualy get wether forecast from the api
url = ["https://www.meteosource.com/api/v1/free/find_places", "https://www.meteosource.com/api/v1/free/point"]
#the api key should be stored to the sample.env file as shown
load_dotenv("sample.env")
APIkey = os.getenv("API_KEY") 

parameters = {"key": APIkey}
#initialize the parameters that the program needs 
parser = argparse.ArgumentParser(description="wether forecast aplication in the comfort of your terminal.\n\
                                 Note: searching by country or continent names may result in inaccurate information,\n\
                                 use city names instead")

parser.add_argument("city", help="specify the city", type=str)
parser.add_argument("-c","--current",action="store_true" ,help="Current weather situation")
parser.add_argument("-H","--hourly",action="store_true", help="Forecasts with hourly resolution")
parser.add_argument("-d","--daily",action="store_true", help="Forecasts for each whole day, morning, afternoon and evening(default)")

args = parser.parse_args()
#validate if the place entered is a valid place
placeID = requests.get(url[0] +  f"?text={args.city}&key={APIkey}").json()

try:
  parameters["place_id"] = placeID[0]["place_id"]
  parameters["units"] = "metric"

except:
  print("placeID not available")
  sys.exit(1)
#the block of code responible to get the current wether of the place added 
if args.current:
  parameters["sections"] = "current"

  data = requests.get(url[1],parameters).json()

  iconNR = int(data["current"]["icon_num"])
  icon = iconChooser(iconNR)
#using the curses module to place the information on the screen
  def currentWether(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    stdscr.clear()

    newLine = 1
    for line in current.split('\n'):
      stdscr.addstr(newLine ,2 ,line)
      newLine += 1

      stdscr.addstr(7 ,2, f"lat: {data['lat']}")
      stdscr.addstr(8 ,2, f"lon: {data['lon']}")
      stdscr.addstr(9 ,2, f"timezone: {data['timezone']}")
      stdscr.addstr(10 ,2, f"units: {data['units']}")

    newWin = curses.newwin(10, 45, 12, 2)
      
    newWin.border()
    newWin.addstr(0, 18, args.city)

    newLine = 2
    for line in icon.split('\n'):
      newWin.addstr(newLine ,2 ,line)
      newLine += 1    

    newWin.addstr(2 ,18, f"summary: {data['current']['summary']}")
    newWin.addstr(3 ,18, f"temperature: {data['current']['temperature']}°C")
    newWin.addstr(4 ,18, f"wind speed: {data['current']['wind']['speed']}m/s")
    newWin.addstr(5 ,18, f"wind angle: {data['current']['wind']['angle']}°")
    stdscr.addstr(24 ,2, "press 'q' to quit")    

    stdscr.refresh()
    newWin.refresh()

    while True:
      key = stdscr.getkey()

      if key == "q":
        break
  
  if icon == "not available" or icon == "":
    print("not available") 
    sys.exit(1)
#the curses module can throw an error if the data added on the screen overflows form the size of the terminal   
  else:
    try:
      wrapper(currentWether)  

    except:
      print("terminal size should be at least 90x20")
      sys.exit(1)
#the block of code responible to get the wether forecast with hourly resolution
elif args.hourly:
  parameters["sections"] = "hourly"

  data = requests.get(url[1],parameters).json()

  dataHourly = data["hourly"]["data"]

  def hourlyWether(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    stdscr.clear()

    newLine = 1
    for line in hourly.split('\n'):
      stdscr.addstr(newLine ,2 ,line)
      newLine += 1

    stdscr.addstr(7 ,2, f"lat: {data['lat']}")
    stdscr.addstr(8 ,2, f"lon: {data['lon']}")
    stdscr.addstr(9 ,2, f"timezone: {data['timezone']}")
    stdscr.addstr(10 ,2, f"units: {data['units']}")
    #where the data will start generating corresponding to the height(y) of the terminal and the lenght(x) 
    y = 5
    x = 2

    for i in range(0, len(dataHourly)):
      index = dataHourly[i]["date"].index("T") + 1
      hour = dataHourly[i]["date"][index:]

      iconNR = dataHourly[i]["icon"]
      icon = iconChooser(iconNR)

      if icon == "not available" or icon == "":
        print("not available") 
        sys.exit(1)
      #split the data in 4 rows and 6 colums
      if i % 6 == 0:
        y += 12
        x = 2

      newLine = y + 1
      for line in icon.split('\n'):
        stdscr.addstr(newLine ,x ,line)
        newLine += 1    

      summary = dataHourly[i]["summary"]
      #spliting the summary just for esthetic purposes
      if summary == "Local thunderstorms":
        index = summary.index(" ") + 1
        summary = summary[index:].capitalize()

      stdscr.addstr(y - 4, x - 1, summary)
      stdscr.addstr(y - 3, x - 1, hour)
      stdscr.addstr(y - 1, x - 1, str(dataHourly[i]["temperature"]) + "°C")
      stdscr.addstr(59 ,1, "press 'q' to quit")    

      x += 19

    stdscr.refresh()

    while True:
      key = stdscr.getkey()

      if key == "q":
        break

  try:
    wrapper(hourlyWether)

  except:
    print("terminal size should be at least half of the screen") 
    sys.exit(1)
#the block of code responible to get the wether forecast with hourly resolution
elif args.daily:
  parameters["sections"] = "daily"
  
  data = requests.get(url[1],parameters).json()

  dataWeekly = data["daily"]["data"]

  def weeklyWether(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()

    stdscr.nodelay(True)
    stdscr.clear()

    newLine = 1
    for line in daily.split('\n'):
      stdscr.addstr(newLine ,2 ,line)
      newLine += 1

    stdscr.addstr(7 ,2, f"lat: {data['lat']}")
    stdscr.addstr(8 ,2, f"lon: {data['lon']}")
    stdscr.addstr(9 ,2, f"timezone: {data['timezone']}")
    stdscr.addstr(10 ,2, f"units: {data['units']}")
    stdscr.addstr(59 ,2, "press 'q' to quit")    
    
    y = 3
    x = 2

    windows = []
    pads = []

    for i in range(0, len(dataWeekly)):
      iconNR = dataWeekly[i]["icon"]
      icon = iconChooser(iconNR)

      if icon == "not available" or icon == "":
        print("not available") 
        sys.exit(1)

      if i % 2 == 0:
        y += 10
        x = 2
      #using pads to store the long summary 
      pad = curses.newpad(1, 200)
      pad.addstr(dataWeekly[i]["summary"])

      newWin = curses.newwin(10, 45, y, x)
      newWin.border()

      newWin.addstr(0, 18, dataWeekly[i]["day"])
      newWin.addstr(3, 18, "temp: " + str(dataWeekly[i]["all_day"]["temperature"]) + "°C")
      newWin.addstr(4, 18, "temp min: " + str(dataWeekly[i]["all_day"]["temperature_min"]) + "°C")
      newWin.addstr(5, 18, "temp max: " + str(dataWeekly[i]["all_day"]["temperature_max"]) + "°C")
      newWin.addstr(6, 18, "wind speed: " + str(dataWeekly[i]["all_day"]["wind"]["speed"]) + "m/s")

      newLine = 2
      for line in icon.split('\n'):
        newWin.addstr(newLine ,1 ,line)
        newLine += 1

      x += 50

      windows.append(newWin)
      pads.append(pad)

    stdscr.refresh()

    for win in windows:
      win.refresh()
    #each element of the list keeps track of character displayed to give the scrolling effect
    scroll = [0, 0, 0, 0, 0, 0, 0]

    while True:
      #check if the end of the string has been reached  
      for i in range(0, 7):
        scroll[i] = reset(scroll[i],len(dataWeekly[i]["summary"]))   
      
      pads[0].refresh(0, scroll[0], 15, 20, 60 ,37)
      pads[1].refresh(0, scroll[1], 15, 70, 60 ,87)
      pads[2].refresh(0, scroll[2], 25, 20, 60 ,37)
      pads[3].refresh(0, scroll[3], 25, 70, 60 ,87)
      pads[4].refresh(0, scroll[4], 35, 20, 60 ,37)
      pads[5].refresh(0, scroll[5], 35, 70, 60 ,87)
      pads[6].refresh(0, scroll[6], 45, 20, 60 ,37)
      #delay the loop so the string is readeble
      time.sleep(0.3)

      for i in range(0, 7):
        scroll[i] += 1

      try:
        key = stdscr.getkey()

      except:
        key = None

      if key == "q":
        break  
      
  try:
    wrapper(weeklyWether)

  except:
    print("terminal size should be at least half of the screen") 
    sys.exit(1)

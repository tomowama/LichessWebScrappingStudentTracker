from bs4 import BeautifulSoup
import requests
import time
import datetime
def sendMessage(number, msg):
    resp = requests.post('https://textbelt.com/text', {
        'phone': f"{number}",
        'message': f"{msg}",
        'key': 'textbelt',
    })   
    print(resp.json())



def getGames(timeControl, user):
    timeControl = timeControl.lower()
    url = f"https://lichess.org/@/{user}/perf/{timeControl}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    games = soup.find_all("td")[0].text
    return int(games)

startBlitz, startRapid = getGames("blitz", "Revo81") - 3, getGames("rapid", "Revo81")


neededBlitz, neededRapid = 7, 3

while True:
    day = datetime.date.today().weekday()
    minute = int(datetime.datetime.now().minute)
    hour = (int(datetime.datetime.now().hour) + 17) % 24


    if day == 0 and minute == 0: # monday morning first minute reset weekly progress
        startBlitz, startRapid = getGames("blitz", "Revo81"), getGames("rapid", "Revo81")
        time.sleep(90)
    if hour == 13 and minute == 0: # first minute of 1 pm
        currBlitz, currRapid = getGames("blitz", "Revo81") - startBlitz, getGames("rapid", "Revo81") - startRapid # get current values
        string = "Make sure to do your tactics ~ 10-15 mins " 
        
        if currBlitz < neededBlitz:
            string += f"you still have {neededBlitz - currBlitz} blitz games to play this week "
        if currRapid < neededRapid:
            string += f"you still have {neededRapid - currRapid} rapid games to play this week"
        
        #send message
        sendMessage("number", string)
    
    time.sleep(45)




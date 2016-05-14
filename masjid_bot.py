from BotApi import BotApi
import signal
import json
import urllib2
import sys
import time

def Exit_gracefully(signal, frame):
        sys.exit(0)

def getSalaahTimes(masjidID):
    salaahTimes=""
    try:
        data = json.load(urllib2.urlopen('http://api.masjidsms.co.za/v1/Masjids/'+masjidID+'/SalaahTimeTable/Today'))
        salaahTimes="Fajr - Athaan: " + data['fajrAzaan']+", Iqaamah: "+data['fajrMasjid']+"\
        \r\nZuhr - Athaan: " + data['zuhrAzaan']+", Iqaamah: "+data['zuhrMasjid']+"\
        \r\nAsr - Athaan: " + data['asrAzaan']+", Iqaamah: "+data['asrMasjid']+"\
        \r\nMaghrib - Athaan + Iqaamah: "+data['maghrib']+"\
        \r\nEsha - Athaan: " + data['eshaAzaan']+", Iqaamah: "+data['eshaMasjid']
    except Exception as e:
        print(e)
    return salaahTimes

def getMasjidsNearby(location):
    masjids = "Masjids:\r\n"
    try:
        data = json.load(urllib2.urlopen("http://api.masjidsms.co.za/v1/Masjids/Nearest?locLat="+str(location.latitude)+"&locLong="+str(location.longitude)+"&km=10"))
        for item in data:
            masjids += item["masjid"]["name"]+", distance: "+str(item["distance"])[:5]+"km , /timetable_"+str(item["masjid"]["id"])+"\r\n"
    except Exception as e:
        print(e)
        print("Error")
    return masjids

def getMasjids(searchText=""):
    masjids = "Masjids:\r\n"
    try:
        data = json.load(urllib2.urlopen('http://api.masjidsms.co.za:80/v1/Masjids?term='+searchText))
        for item in data:
            masjids += item["name"]+", /timetable_"+str(item["id"])+"\r\n"
    except Exception as e:
        print(e)
    return masjids

def handle_message(msg,uid):
    if msg.startswith('/timetable'):
        if len(msg) < 11:
            return{"text":"Usage: /timetable <Masjid ID>"}
        else:
            return {"text":getSalaahTimes(msg[11:])}
    elif msg.startswith('/masjids'):
        return {"text":getMasjids(msg[9:])}
    elif msg.startswith('/nearby'):
        keyboardButton = {"text":"Send Location","request_location":True}
        keyboard = [[keyboardButton]]
        replyKeyBoardMarkup = {"keyboard":keyboard,"one_time_keyboard":True}
        return {"text":"Click \"Send Location\" to find Masaajid in your vicinity..","keyboard":replyKeyBoardMarkup}
    else: return {"text":"Unknown Command"}

def handle_location(msg):
    return getMasjidsNearby(msg)

def main():
    QUIT = False
    print("Starting...")
    keyFile = open('test_bot.key')
    key = keyFile.read()
    bot = BotApi(key.strip('\n'))
    print(bot.getMe())
    try:
        while not QUIT:  # loop for messages
            try:
                updates = bot.getUpdates(offset=bot.getLastFetchedId() + 1)
                for update in updates:
                    if update.message !=None:
                        if update.message.text != None:
                                if update.message.text.startswith("/"):
                                    reply = handle_message(update.message.text,update.message.msg_from.userid)
                                    if 'keyboard' in reply:
                                        bot.sendMessage(str(update.message.msg_from.userid), reply['text'],reply_markup=json.dumps(reply['keyboard']))
                                    else:
                                        bot.sendMessage(str(update.message.msg_from.userid), reply['text'])
                        if update.message.location != None:
                            bot.sendMessage(str(update.message.msg_from.userid), handle_location(update.message.location))
            except Exception as e:
                print(e)
                pass
            time.sleep(10)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    else:
        # the loop exited without exception, becaues _quit was set True
        pass

if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)
    main()

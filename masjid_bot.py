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

def getMasjids(searchText=""):
    masjids = ""
    try:
        data = json.load(urllib2.urlopen('http://api.masjidsms.co.za:80/v1/Masjids?term='+searchText))
        for item in data:
            masjids += item["name"]+", ID: "+str(item["id"])+"\r\n"
    except Exception as e:
        print(e)
    return masjids

def handle_message(msg,uid):
    if msg.startswith('/timetable'):
        if len(msg) < 11:
            return("Usage: /timetable <Masjid ID>")
        else:
            return getSalaahTimes(msg[11:])
    elif msg.startswith('/masjids'):
        return getMasjids(msg[9:])
    else: return("Unknown Command")

def main():
    QUIT = False
    print("Starting...")
    keyFile = open('bot.key')
    key = keyFile.read()
    bot = BotApi(key.strip('\n'))
    print(bot.getMe())
    try:
        while not QUIT:  # loop for messages
            try:
                updates = bot.getUpdates(offset=bot.getLastFetchedId() + 1)
                for update in updates:
                    if update.message.msg_from is not None:
                        if update.message.text is not None:
                            if update.message.text.startswith("/"):
                                bot.sendMessage(str(update.message.msg_from.userid), (handle_message(update.message.text,update.message.msg_from.userid)))
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

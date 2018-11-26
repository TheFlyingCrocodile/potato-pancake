import datetime
import TWT
import FB
import IG
import ConfigParser
############LOADING CONFIG FILES ##################
config = ConfigParser.ConfigParser()
config.read('Lib/blup.cfg')
TimeRange = config.get("calender", 'TimeRange')



def main(events):
    for event in events:
        GEvent = event['start'].get('dateTime', event['start'].get('date'))
        args = GEvent.split("T")
        d = args[0]
        t = args[1]
        Args = t.split("+")
        notimezone = Args[0]
        args1 = d.split("-")
        year = args1[0]
        month = args1[1]
        day = args1[2]
        args2 = notimezone.split(":")
        hour = args2[0]
        minute = args2[1]
        second = args2[2]
        GoogleDate = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
        Range = datetime.timedelta(minutes=int(TimeRange))
        CurrentTime = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        MinRange = CurrentTime - Range
        MaxRange = CurrentTime + Range
        print MinRange
        print GoogleDate
        print MaxRange
        if GoogleDate > MinRange and GoogleDate < MaxRange :
            print("True")
            EventCheck(event)
        else:
            print("False")


def EventCheck(event):
    Title = event['summary']
    args = Title.split("-")
    platform = args[0]
    company = args[1]
    print platform
    if platform.lower() == "twitter":
        print ("run TWT")
        TWT.main(event)
    elif platform.lower() == "facebook":
        print ("run FB")
        FB.main(event)
    elif platform.lower() == "instagram":
        print ("run IG")
        IG.main(event)
    else:
        ############WRITE CONFIG FILES ##################
        ###     Writes the event info to errors.cfg   ###
        #################################################
        print("ERROR : invalid platform")
        conf = ConfigParser.RawConfigParser()
        start = event['start'].get('dateTime', event['start'].get('date'))
        conf.add_section('Wrong Platform')
        info =  str(start)+"|"+str(event['summary'])+"|"+str(event['description'])
        conf.set('Wrong Platform', info)
        # Writing our configuration file to 'errors.cfg'
        with open('Lib/errors.cfg', 'wb') as configfile:
            conf.write(configfile)

from datetime import datetime

def getMonthLabels():
    pastMonth = []

    today = int(str(datetime.date(datetime.now()))[8:10])
    while today >= 1:
        pastMonth= ((str(datetime.date(datetime.now()))[:8] + f"{today:02d}") )
        today -= 1

    return pastMonth
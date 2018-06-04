import requests
from datetime import date, datetime, timedelta
import calendar
def coinHistory(id,begin_time, end_time, zero_time): #begin, end, and zero time should be unix timestamp INTEGERS * 1000
    max_time = int(unix_time(datetime.utcnow()))*1000 #current time
    #zero_time validation
    if type(zero_time) !=  type(1):
        print('ZERO TIME BAD INPUT::',zero_time)
        return False
    elif zero_time > begin_time or zero_time > end_time: #must be less than both
        print('INVALID ZERO TIME::', zero_time)
        return False
    else:
        print('VALID ZERO TIME::',zero_time)
    
    #begin_time validation
    if type(begin_time) != type(1):
        begin_time = zero_time
        print('setting begin time to zer0')
    elif begin_time < zero_time: #when placing the first boundary, it needs to be between the current time-1 day and minimum time only
        begin_time = zero_time
        print('setting begin time to zer1')
    elif begin_time > max_time:
        print('setting begin time to one day less than max')
        begin_time = calendar.timegm((datetime.utcnow() - timedelta(days=1)).timetuple()) #subtract a day from the time and turn back to unix
        print('',)
    else:
        print('VALID BEGIN TIME::',begin_time)
    
    #end_time validation
    if (type(end_time) != type(1)) or (end_time > max_time) or (end_time < begin_time):
        end_time = max_time
        print('setting end time to maximum')
    else:
        print('VALID END TIME::',end_time)
        end_time = end_time*1000 #API needs 3 zeroes on the end
        zero_time = zero_time*1000
        begin_time = begin_time*1000

    # Find specific coin wanted through id
    if id == '825':
        URL = "https://graphs2.coinmarketcap.com/currencies/tether/"+str(begin_time)+"/"+str(end_time)+"/"
    elif id == '1':
        URL = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"+str(begin_time)+"/"+str(end_time)+"/"
    else:
        URL = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"+str(begin_time)+"/"+str(end_time)+"/"
    print('TIMES::', begin_time,end_time)
    # Create GET request to API
    print('URL::', URL)
    response = requests.get(URL)
    if response.status_code != 200: #checks if get was successful
        print('BAD CODE::',response.status_code)
        return False
    # Translate to JSON
    data = response.json()
    print('JSON_LENGTH::', len(data))
    # Storing date and price into Object List
    max_len = int(len(data['price_usd']))
    datePrice = []
    for i in range(0,max_len): #organize data
        time = datetime.fromtimestamp(int((data['price_usd'][i][0])/1000))#.strftime('%Y-%m-%d')
        price = data['price_usd'][i][1]
        datePrice.append({'time': time,'price': price})
        # return the objectList
    print('ARRAY LENGTH::',len(datePrice))
    return datePrice

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    unix = int((dt - epoch).total_seconds())
    print('UNIX::', unix)
    return unix
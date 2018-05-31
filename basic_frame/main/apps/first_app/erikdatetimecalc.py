import requests
from datetime import date, datetime, timedelta
def coinHistory(id,begin_time, end_time, zero_time): #begin, end, and zero time should be unix timestamp INTEGERS
    max_time = int(unix_time(datetime.utcnow())) #current time
    #zero_time validation
    if type(zero_time) !=  type(1):
        print('ZERO TIME BAD INPUT::',zero_time)
        return False
    elif zero_time > begin_time or zero_time > end_time: #must be less than both
        print('INVALID ZERO TIME::', zero_time)
        return False
    else:
        pass
    
    #begin_time validation
    if type(begin_time) != type(1):
        begin_time = zero_time
    elif begin_time < zero_time: #when placing the first boundary, it needs to be between the current time-1 day and minimum time only
        begin_time = zero_time
    elif begin_time > max_time:
        begin_time = unix_time((datetime.now(pytz.utc) - (timedelta(days=1)))) #debug #subtract a day from the time and turn back to unix
    else:
        pass #valid placement, begin time is now for sure a valid input, and we can use it as a measurement below
    
    #end_time validation
    if type(end_time) != type(1):
        end_time = max_time
    elif end_time > max_time: #when placing the second boundary, it needs to be after begin_time and before max length
        end_time = max_time #max range
    elif end_time < begin_time:
        end_time = begin_time + int(timedelta(days=1)) #min range of one day #debug
    else:
        pass #valid placement, we now have all valid inputs
    
    # Find specific coin wanted through id
    if id == '825':
        URL = "https://graphs2.coinmarketcap.com/currencies/tether/"+str(begin_time)+"/"+str(end_time)+"/"
    elif id == '1':
        URL = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"+str(begin_time)+"/"+str(end_time)+"/"
    else:
        URL = "https://graphs2.coinmarketcap.com/currencies/bitcoin/"+str(begin_time)+"/"+str(end_time)+"/"
    print('TIMES::', begin_time,end_time)
    # Create GET request to API
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
    return (dt - epoch).total_seconds() * 1000
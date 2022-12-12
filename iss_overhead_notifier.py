import requests, os, smtplib, time
from datetime import datetime


#initilize global variables
EMAIL = os.getenv('SMTP_USER')
PW = os.getenv('SMTP_PASS')
MY_LAT = 37.2431
MY_LONG = 115.7930


def iss_within_range():
    '''If ISS is within a + or - 5 degrees of supplied lat/long then return True.'''
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()
    iss_lat = float(data['iss_position']['latitude'])
    iss_long = float(data['iss_position']['longitude'])

    if MY_LAT-5 <= iss_lat <= MY_LAT+5 and MY_LONG-5 <= iss_long <= MY_LONG+5:
        return True


def night_time():
    '''If it is night time at supplied lat/long then return True'''
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 0,
    }

    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


#while program is running this loop is endless and will notify when then ISS is overhead the given coordinates.
try:
    while True:
        time.sleep(60)
        if iss_within_range() and night_time():
            with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=PW)
                connection.sendmail(
                    from_addr=EMAIL,
                    to_addrs=EMAIL,
                    msg=f'Subject: Look up!\n\nLook up!')

except Exception:
    print('error caught:', Exception.__name__)
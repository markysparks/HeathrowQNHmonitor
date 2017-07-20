import sys
import re
import socket
import requests
from requests import exceptions

if sys.version_info[0] < 3:
    import tkMessageBox
else:
    from tkinter import messagebox as tkMessageBox

__author__ = 'Mark Baker  email: mark.baker@metoffice.gov.uk'


def get_qnh_data(icao_ident='EGLL'):
    """Get the latest METAR for EGLL from MetDB.
    """
    global root
    socket.setdefaulttimeout(5)

    obs_time = ''
    qnh = ''
    response = ''

    # Query to get the latest METAR web page result
    try:
        response = requests.get('http://mdbdb-prod/cgi-bin/moods/webret.pl?pageType=mainpage&subtype=METARS&'
                                'system=mdbdb-prod&idType=ICAO&stn01=EGLL&submit=Retrieve+Latest+Report')

    except requests.exceptions.RequestException as e:
        pass
        tkMessageBox.showerror('Communications Error',
                               'Error retrieving data from MetDB - will retry if monitoring on.')

    # Check we have a response to our query before proceeding
    if response is not None:

        # Extract the QNH reading from the web pagae
        if re.search('Q.*\n*\r*\d.*\n*\r*.*\d.*\n*\r*.*\d.*\n*\r*.*\d', response.text):
            qnh_str = re.search(r'Q.*\n*\r*\d.*\n*\r*.*\d.*\n*\r*.*\d.*\n*\r*.*\d', response.text).group()
            qnh_digits_str = qnh_str.replace(" ", "").replace("\n", "").replace("\r", "")
            qnh = int(re.search(r'\d+', qnh_digits_str).group())

        # Extract the date/time group from the web page response
        if re.search('EGLL \d\d\d\d\d\dZ', response.text):
            obs_time = re.search(r'\d\d\d\d\d\dZ', response.text).group()

    # return obs_time, qnh
    return obs_time, qnh


if __name__ == "__main__":
    print('EGLL QNH Data= ', get_qnh_data('EGLL'))

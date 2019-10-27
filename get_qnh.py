import sys
import re
import socket
import requests

if sys.version_info[0] < 3:
    import tkMessageBox
else:
    from tkinter import messagebox as tkMessageBox

__author__ = 'Mark Baker  email: mark.baker@metoffice.gov.uk'

regex_issue_time = re.compile('\d\d\d\d\d\dZ')
qnh_pattern = re.compile('Q[\d]+')


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
                                'system=mdbdb-prod&idType=ICAO&stn01=' + icao_ident + '&submit=Retrieve+Latest+Report')

    except requests.exceptions.RequestException as e:
        pass
        tkMessageBox.showerror('Communications Error',
                               'Error retrieving data from MetDB - will retry if monitoring on.')

    # Check we have a response to our query before proceeding
    if response is not '':

        metar = re.search(icao_ident + '\s\d\d\d\d\d\dZ[\s\S\d\D\w\W]+?\\n\s</pre>', response.text)
        if metar:
            metar = metar.group()
            # Strip out occurrences of 15 multiple spaces that occur when web page response line wraps
            metar = re.sub('               ', '', metar.strip())
            # Strip out any newlines and other cruft from web page response formatting
            metar = re.sub('\\n', '', metar).strip()
            metar = re.sub('\s</pre>', '', metar).strip()
            obs_time = re.search(regex_issue_time, metar).group()
            qnh = re.search(qnh_pattern, metar).group()

    return obs_time, qnh


if __name__ == "__main__":
    print('QNH time / value = ', get_qnh_data('EGLL'))

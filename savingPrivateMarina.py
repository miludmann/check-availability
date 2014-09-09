#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import bs4
import re
from datetime import date
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
import codecs

me = xxx
dest1 = xxx
dest2 = xxx
 
def build_msg(filename, subject):
    fp = codecs.open(filename, encoding='utf-8', mode='rb')
    # Create a text/plain message
    msg = MIMEText(fp.read().encode('utf-8'))
    fp.close()

    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = dest1
    return msg

msg_positive = build_msg('/home/mludmann/dev-vdi/email_positive.txt', u'/!\ Une nouvelle date est dispo sur le site de la préfecture \o/')
msg_negative = build_msg('/home/mludmann/dev-vdi/email_negative.txt', u':( (Pour l\'instant) Le site de la préfecture ne propose plus aucune date')

deadline = date(2014, 10, 20)
print "La deadline est le " + str(deadline)

response = requests.get('xxx')
soup = bs4.BeautifulSoup(response.text)
result = soup.find(id = "dtrv")

soup2 = bs4.BeautifulSoup(str(result))
regex = re.compile(".*(20\d\d)[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])")
dates = soup2.find_all('option', value=regex)

s = smtplib.SMTP('localhost:1025')
s.login('XXXX', 'XXXX')


if (len(dates) == 0): 
    print "Aucun créneau de disponible pour le moment. N'importe quoi !"
    #s.sendmail(me, [dest2, dest1], msg_negative.as_string())
    exit(0)

for dateItem in dates:
    date_str = str(dateItem)
    soupdate = bs4.BeautifulSoup(date_str)
    print date_str
    day = date(int(regex.search(date_str).group(1)), int(regex.search(date_str).group(2)), int(regex.search(date_str).group(3))) 
    print "Jour trouve : " + str(day)
    if day > deadline:
        print "C'est trop tard..."
    else:
        print u"La date est bonne !!! VITE, il faut réserver !!!"
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s.sendmail(me, [dest1, dest2], msg_positive.as_string().encode('utf-8'))
        s.quit()
    date = soupdate.get_text()
    print dateItem



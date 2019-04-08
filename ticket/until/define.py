#-*- coding: UTF-8 -*-
import datetime
import pytz
import time
import json
import urllib.request
import uuid
import hashlib
import urllib.parse

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

if (get_mac_address() == '00:50:56:82:19:40') :
    MEDIAURL = 'http://122.200.85.10:8090/media/'
else:
    print(get_mac_address())
    MEDIAURL = 'http://127.0.0.1:8000/media/'

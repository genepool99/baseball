#!/usr/bin/env python

import spynner
import os, codecs
import os.path
import time
from datetime import datetime
from pytz import timezone

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
log = open(dname + '/NotificationService.log', 'a')        # Open log file to append
now = datetime.now(timezone('US/Eastern'))
fmt = "%I:%M %p %b %d, %Y - %Z"
log.write("Log opened at " + str(dname))

def remove_bom_from_file(filename, newfilename):
    if os.path.isfile(filename):
        f = open(filename,'rb')
        header = f.read(4)      # read first 4 bytes
        bom_len = 0             # check if we have BOM...
        encodings = [ ( codecs.BOM_UTF32, 4 ),
            ( codecs.BOM_UTF16, 2 ),
            ( codecs.BOM_UTF8, 3 ) ]

        # ... and remove appropriate number of bytes    
        for h, l in encodings:
            if header.startswith(h):
                bom_len = l
                break
        f.seek(0)
        f.read(bom_len)

        # copy the rest of file
        contents = f.read() 
        nf = open(newfilename, "w")
        nf.write(contents)
        nf.close()

b = spynner.Browser()
#b.debug_level = spynner.DEBUG

urls = {
            "pZiPSPre":"http://www.fangraphs.com/projections.aspx?pos=all&stats=pit&type=zips&team=0&lg=all&players=0",
            "bZiPSPre":"http://www.fangraphs.com/projections.aspx?pos=all&stats=bat&type=zips&team=0&lg=all&players=0",
            "bZiPSRoS":"http://www.fangraphs.com/projections.aspx?pos=all&stats=bat&type=rzips&team=0&lg=all&players=0",
            "pZiPSRoS":"http://www.fangraphs.com/projections.aspx?pos=all&stats=pit&type=rzips&team=0&lg=all&players=0",
            "bDCRoS":"http://www.fangraphs.com/projections.aspx?pos=all&stats=bat&type=rfangraphsdc&team=0&lg=all&players=0",
            "pDCRoS":"http://www.fangraphs.com/projections.aspx?pos=all&stats=pit&type=rfangraphsdc&team=0&lg=all&players=0",
            "bActual":"http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2016&month=0&season1=2016&ind=0&team=&rost=&age=&filter=&players=",
            "pActual":"http://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season=2016&month=0&season1=2016&ind=0&team=0&rost=0&age=0&filter=&players=0",
            "bpActual":"http://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=0&type=8&season=2016&month=0&season1=2016&ind=0&team=0,ts&rost=0&age=0&filter=&players=0"
        }
      
for url in urls:
    b.wait(5)
    for attempt in range(10):
        try:
            b.load(urls[url])
            b.wait_load(10)
        except:
            continue
        else:
            break
    else:
        log.write(now.strftime(fmt) + " - CRON[uld]: [ERROR] unable to download " + filename + " - " + urls[url] + "\n")
        break
    
    filename = "data/" + url 
    log.write(now.strftime(fmt) + " - Getting " + filename + " - " + urls[url] + "\n")
    if "projections" in urls[url]:
        b.click("#ProjectionBoard1_cmdCSV", wait_load=True)
        b.wait(10)
    elif "leaders" in urls[url]:
        b.click("#LeaderBoard1_cmdCSV", wait_load=True)
        b.wait(10)
    
log.write(now.strftime(fmt) + " - CRON[uld]: Local DB Update Complete.\n")



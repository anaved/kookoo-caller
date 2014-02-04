#!/usr/bin/env python
from conf.app_settings import APP_LOGGER
from kook.models import Dump
import json
import kookoo
import os
import subprocess
import web

urls = (

  '/status', 'status',
  '/attempt_call', 'attempt_call',
  '/responses', 'responses',
 )
app = web.application(urls, globals())

SID={}
class status:
    def POST(self):
        i = web.input()
        Dump.objects.get_or_create(type='STATUS',data=json.dumps(i))
        APP_LOGGER.debug("KOOKOO SENT STATUS:"+json.dumps(i))
        return 'OK'

class responses:
    def GET(self):
        from datetime import datetime
        x=datetime.now()        
        data= Dump.objects.filter(type__in=['INTERESTED','CALL BACK'],timestamp__day=x.day,timestamp__year=x.year,timestamp__month=x.month).order_by('type','id')
        x='<html><head><script type="text/JavaScript">function timedRefresh(timeoutPeriod) {    setTimeout("location.reload(true);",timeoutPeriod);}  </script></head><body onload="JavaScript:timedRefresh(10000);"><table border="6">'       
        for e in data:
            x=x+"<tr><td>"+str(e.id)+"</td><td>"+e.type+"</td><td>"+e.data+"</td></tr>"
            
        return x+"</table> </body></html>"
            
        


class attempt_call:
    def GET(self):
        from conf.app_settings import LOCALT_PATH,AUDIO_FILE
        web.header('Content-Type', 'text/xml')
        input= web.input()
        APP_LOGGER.debug("KOOKOO CALLED ME:"+json.dumps(input))
#        Dump.objects.get_or_create(type="INPUT",data=json.dumps(input))
        if input.has_key('event'):
            if input['event']=='NewCall':
                SID[input['sid']]=input['cid']
                Dump.objects.get_or_create(type='NEW CALL',data=json.dumps(input))
                r = kookoo.Response()
                g = r.append(kookoo.CollectDtmf(maxDigits=1))
                g.append(kookoo.PlayAudio(LOCALT_PATH+'/static/'+AUDIO_FILE))
                return r
            if input['event']=='GotDTMF':
                digit=input['data']
                if digit=='1':
                    Dump.objects.create(type='INTERESTED',data=SID[input['sid']])
                    r = kookoo.Response()
                    r.addPlayText('Thank you, we will call you back in 5 minutes')
                    r.addHangup()
                    return r
                if digit=='2':
                    Dump.objects.create(type='CALL BACK',data=SID[input['sid']])
                    r = kookoo.Response()
                    r.addPlayText('Thank You')
                    r.addHangup()
                    return r
                if digit=='3':
                    Dump.objects.create(type='NOT INTERESTED',data=SID[input['sid']])
                    r = kookoo.Response()
                    r.addPlayText('Thank You')
                    r.addHangup()
                    return r
                if digit=='4':
                    Dump.objects.get_or_create(type='REPLAYED',data=SID[input['sid']])
                    r = kookoo.Response()
                    g = r.append(kookoo.CollectDtmf(maxDigits=1))
                    g.append(kookoo.PlayAudio(LOCALT_PATH+'/static/'+AUDIO_FILE))
                    return r
        else:
            return '<response>invalid call</response>'

def main():
    app.run()
    return 0

if __name__ == '__main__': 
        main()
        
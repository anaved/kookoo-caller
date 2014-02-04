#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="naved"
__date__ ="$10 Nov, 2011 1:49:54 PM$"
from conf.app_settings import APP_LOGGER
from excludes import EXCLUDES
from kook.models import Dump
from subprocess import Popen
import json
import re
import subprocess
import time
import urllib
def run_number(phone):
    from conf.app_settings import LOCALT_PATH
    e=phone         
    x='http://www.kookoo.in/outbound/outbound.php?phone_no=%s&api_key=KK522054d3f6a95b951e41aef291c9a5eb&url=%s/attempt_call&callback_url=%s/status'%(e,LOCALT_PATH,LOCALT_PATH)
    print x
    APP_LOGGER.debug("CALLING: "+x)        
    cmd = subprocess.Popen(["curl", x], stdout=subprocess.PIPE)
    res=''
    for line in cmd.stdout:
            res=e+" - "+line.rstrip("\n")
    APP_LOGGER.debug("RESPONSE: "+str(res))
    m=re.search('queued',res)
    if m:
        Dump.objects.get_or_create(type='QUEUED',data=res)
    m=re.search('DND',res)
    if m:
        Dump.objects.get_or_create(type='DND',data=res)
    time.sleep(3)


def check_mobile(orig):    
    chunks=orig.replace('+','').split('-')
    if chunks[0].startswith('91'):
        chunks[0]=chunks[0].replace('91','',1)
    number=''.join(chunks)
    if number.startswith(('9','8','7')):
            number=''.join(chunks)    
            if len(number)!=10:
                #not mobile
                return [0,number]
            else:
                #mobile
                return [1,number]
    if len(chunks[-1])>=10:
        number=chunks[-1][-10:]
        if number.startswith(('9','8','7')):
            return [1,number]
    #unsure   
    return [2,orig]

def check_landline(orig):
    number=orig.replace('91-','')
    number=number.replace('-','')
    if not number.startswith('0'):
        number='0'+number        
    if number[1] in ['9','8','7']:
        return number[1:]
          
    else:
        if len(number)>=9:
            return number
     

def process_number(orig):
    number= re.sub('\D','',orig)
    number=number.strip()       
    if not number.isdigit():
        return None
    result= check_mobile(number)
    if result[0]==2:
#disabled landline        
        land= check_landline(number)
        return land if land else None        
        return None   
    if result[0]==0:
        return None
    if result[0]==1:
        return result[1]        
    return None        

    
def clean_numbers():    
    in_f=open('in_numbers.txt','r')
    out_f=open('out_numbers.txt','w')
    for e in in_f.readlines():
        x= process_number(e)        
        out_f.write('%s|%s\n'%(e.strip(),x if x else ''))
    in_f.close()
    out_f.close()
    
def get_numbers():    
    numbers=set([])
    f=open('out_numbers.txt','r') 
    for e in f.readlines():
        e=e.strip()
        e=e.split('|')
        if len(e)>1 and e[1]:
            numbers.add(e[1])    
    for e in EXCLUDES:
        if numbers.__contains__(e):
            numbers.remove(e)        
    return numbers         
            
if __name__ == '__main__':
    clean_numbers()
    phones= get_numbers()
    print len(phones)
        
#    phones=[ 
#            '9860403685',
##            '9967460332'
#          ]
    for e in phones:
        run_number(e)

              

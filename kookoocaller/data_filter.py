# To change this template, choose Tools | Templates
# and open the template in the editor.


import ast
from django.core.management import setup_environ
import settings
import traceback
setup_environ(settings)
from datetime import datetime
import urllib2
from job.models import  *
from master.models import  *
import simplejson as  json
from django.core import serializers
import glob
import os
import subprocess
import re
import random
import urlparse
import sys

__author__ = "naved"
__date__ = "$31 Jul, 2011 3:40:41 PM$"


def filter_contact():
    jobs= ParsedJobs.objects.filter(manual_done=False,is_sent=False)    
    for job in jobs:
        data= job.all_text
        pat= '([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)'
        mat= re.search(pat,data,flags=re.DOTALL)
        if mat:
           job.contact_info=mat.group(0)
           job.save()

def filter_company_joburl():
    pat=['Indeed.com','vseindeed','indeed']
    jobs= ParsedJobs.objects.filter(company_joburl__icontains='indeed',manual_done=False,is_sent=False)
    for job in jobs:
        for p in pat:
            p = re.compile(p, re.IGNORECASE)
            mat= p.subn('',job.company_joburl)
            if mat[1]:
                  job.company_joburl=mat[0]
                  job.save()
                  break

def scale_parttime():
    pat=['hours per week','hours/week']
    for p in pat:
        jobs=ParsedJobs.objects.filter(all_text__icontains=p,full_parttime=True)
        for job in jobs:
            for x in job.all_text.split('\n'):
                if p.upper() in x.upper():
                    mat=re.findall('\d\d hours',x)
                    mat=mat[0].split()[0] if mat else None
                    if mat:
                        gpa=int(mat)
                        if  gpa<30:
                            job.full_parttime=False
                            job.save()
                            break
                        else:
                            job.full_parttime=True
                            job.save()
                            break
                    else:
                            job.full_parttime=False
                            job.save()
                            break


def filter_full_parttime():    
    #check full
    pat=['full time', 'fulltime','full-time',]
    
    for p in pat:
        ParsedJobs.objects.filter(all_text__icontains=p,manual_done=False,is_sent=False).update(full_parttime=True)
        
    #check part
    pat=['part time', 'parttime','part-time',]
    for p in pat:
        ParsedJobs.objects.filter(all_text__icontains=p,manual_done=False,is_sent=False).update(full_parttime=False)

    #test rigorous part
    scale_parttime()
        
  

def filter_paid_unpaid():
    pat=['unpaid','not paid','no compensation','not paying','non-paid']
    for p in pat:
      ParsedJobs.objects.filter(all_text__icontains=p,manual_done=False,is_sent=False).update(paid_unpaid=False)
      




def filter_gpa():
    pat=['gpa','g.p.a.','grade point average']
    for p in pat:        
        jobs=ParsedJobs.objects.filter(all_text__icontains=p,manual_done=False,is_sent=False)
        for job in jobs:
            for x in job.all_text.split('\n'):
                if p.upper() in x.upper():
                    mat=re.search('\d\.\d',x)
                    if mat:
                        gpa=float(mat.group(0))
                        if not gpa>=4.0:
                            gpa=float(int(gpa*2))/2
                            job.gpa=gpa
                            job.save()
                            break

            

def filter_year():
    pat=(
#    ('GR',' graduate'),
    ('SR',' senior'),
    ('JR',' junior'),
    ('SO',' sophomore'),
    ('FR',' freshman'),
    )
    for p in pat:
        ParsedJobs.objects.filter(all_text__icontains=p[1],manual_done=False,is_sent=False).update(year=p[0])



def filter_all():
    filter_contact();
#    filter_company_joburl();
    filter_full_parttime();
    filter_paid_unpaid();
    filter_gpa();
    filter_year();


if __name__ == "__main__":
    filter_all()
     

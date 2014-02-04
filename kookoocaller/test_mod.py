#! /usr/bin/python

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

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="naved"
__date__ ="$23 Aug, 2011 6:13:51 PM$"

#def filter_test():
#    pat=['hours per week','hours/week']
#    for p in pat:
#        jobs=ParsedJobs.objects.filter(all_text__icontains=p)
#        for job in jobs:
#            for x in job.all_text.split('\n'):
#                if p.upper() in x.upper():
#                    mat=re.findall('\d\d hours',x)
#                    mat=mat[0].split()[0] if mat else None
#                    if mat:
#                        gpa=int(mat)
#                        if  gpa<30:
#                            print "gotcha",job.id,gpa,x
#                        else:
#                            break
#                    else:
#                            job.
#
#
#if __name__ == "__main__":
#    filter_test()
#companies=[
#"accenture",
#"apple",
#"google",
#"bank of america",
#"bbc",
#"boeing",
#"cia",
#"cnn",
#"white house",
#"deloitte",
#"disney",
#"espn",
#"fbi",
#"goldman sachs",
#"ibm",
#"intel",
#"jp morgan",
#"merrill lynch",
#"national geographic",
#"kpmg",
#"mckinsey",
#"merrill lynch",
#"microsoft",
#"moma",
#"morgan stanley",
#"mtv",
#"nasa",
#"nbc",
#"nike",
#"nsa",
#"nylon",
#"vogue",
#"white house",
#"world bank",
#
#]
#
#for c in companies:
#    d= ParsedJobs.objects.filter(company__icontains=c)
#    print c,len(d)
f=open('logos.txt','r')
for e in f.readlines():
    company= e.split('|')[0]
    comp= ParsedJobs.objects.filter(company__icontains=company).distinct()
    if comp:
        print company,[e.company for e in comp]
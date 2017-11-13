from itertools import izip
from requests.packages.urllib3 import Retry
import requests
import time
from termcolor import colored
import datetime
import sys
import re
import subprocess
from multiprocessing import Process
import os
import json


#Extract script settings
max_sites = 3						# Number of FQDN in the incap account
page = 0                                                # since we can only extract the events 100 per 100, an incrementation of the page is needed
count = 0                                               # needed for the while function
max_page = 12	                                        # max page to fetch, 1 page = 100 events
script_name = "export_incap.py"			     	# input the script name here if you change it
#log_file = open("log.txt", "w+")

#api settings
url = 'https://my.incapsula.com/api/visits/v1'          # api URL , for the events extraction: visits/v1
api_id = 'Input your API ID here'
api_key = 'Input your API key here'
time_range = 'custom'                            	# for a custom time range
page_size = '100'                                       # Number of events you want to fetch in one page

#error display
input_site_error = "Wrong number ! Please input a number between 0 and 2"

#print site selector info
print_site_info = ("Please select a " + colored('number','yellow') + " corresponding to a website:\n"
+ colored('--------------------------------------------------','red') + "\n"
+ colored('all website!: 0','cyan') + "\n"
+ "www.website-1.com: " + colored('1','yellow') + "\n"
+ "www.website-2.com: " + colored('2','yellow') + "\n"
+ "www.website-3.com: " + colored('3','yellow') + "\n")

#site selector
def site_selector(num):
    if num == 1:
	name = '-website-1.json'                                   # script ouput Filename
	client = 'www.website-1.com'                     	   # FQDN for printing purpose
	site_id = 'INPUT THE SITE ID HERE'			   # Site id
    elif num == 2:
    	name = '-website-2.json'                               
	client = 'www.website-2.com'                             
	site_id = 'INPUT THE SITE ID HERE'
    elif num == 3:
        name = '-website-3.json'
        client = 'www.website-3.com'
        site_id = 'INPUT THE SITE ID HERE'
    else:
	pass
    try:
        return [name,client,site_id]
    except:
        pass

#Parsing settings
def uri(arg):
    if 'website-1.' in arg:                         
        dname = 'www.website-1.com'
    if 'website-2.' in arg:
        dname = 'www.website-2.com'
    if 'website-3.' in arg:
        dname = 'www.website-3.com'
    return dname


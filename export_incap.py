#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4  smartindent
from etc.config import *


     
  
        


print(
"					                   \n"
"                                                          \n"
"         _/_/_/    _/_/_/    _/_/_/_/                     \n"
"        _/    _/  _/    _/  _/                            \n"
"       _/_/_/    _/_/_/    _/_/_/                         \n"
"      _/    _/  _/    _/  _/                              \n"
"     _/_/_/    _/_/_/    _/_/_/_/                         \n"
" 		 			                   \n"	
"        Baptiste Bellecour 2017	                   \n"
"					                   \n"
"        incapsula extract script	                   \n"
" 					                   \n"
"					                   \n\n"
+ colored("For a precise extraction, please ensure that the local time of this terminal is set to your timezone UTC. \n","yellow") )

# contact : baptiste@bellecour.io


#checking date format, and site input exiting the script if incorrect

def validate(date_text):
    try:	
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:	
	raise ValueError("Incorrect date format, it must  be" + colored(" YYYY-MM-DD","green"))

def validate_site(number):
    if (number in xrange(0, max_sites + 1 )) != True:
        print input_site_error
        sys.exit("Program exited")

print print_site_info

#site selection
chose_site = raw_input("Website "+ colored('number','yellow') + ": ")
try:
    chose_site = int(chose_site)
except:
    print input_site_error
    sys.exit("Program exited")

validate_site(chose_site)

if chose_site != 0:
    name = site_selector(chose_site)[0]
    client = site_selector(chose_site)[1]
    site_id = site_selector(chose_site)[2]
    print ("\nYou have chosen " + colored(client , 'green') + "\n")



#date selection
    isdate = raw_input("enter the" + colored(" start date","yellow") + " and" + colored(" end date","yellow")+ " of the desired export range," +" date format must be" + colored(" YYYY-MM-DD.","green")+"\nFor example, if you want to extract the events of january 2017 you must input" + colored (" 2017-01-01","green") + " as the start date and" + colored (" 2017-02-01","green") + " as the end date." + "\n\nPlease, enter the" + colored(" start date: ","yellow"))
    validate(isdate)
    iedate = raw_input("\nEnter now the" + colored(" end date: ","yellow"))
    validate(iedate)

#converting input dates into epoch time (milliseconds)
    date = datetime.datetime.strptime(isdate, '%Y-%m-%d').strftime('%Y-%m-XX')
    pattern = '%Y-%m-%d'
    epochSt = int(time.mktime(time.strptime(isdate, pattern))) * 1000
    epochEn = int(time.mktime(time.strptime(iedate, pattern))) * 1000
    stEpoch = epochSt
    enEpoch = epochEn

#starting extraction

    print "\nThank you ! Connecting to the incapsula API, please wait a moment.\n"

    s = requests.Session()  				# session creation
    a = requests.adapters.HTTPAdapter(max_retries=20) 	# Creation of an HTTP Adapter with a retry logic
    b = requests.adapters.HTTPAdapter(max_retries=20) 	# Creation of an HTTPS Adapter with a Retry logic
    s.mount('http://', a) 			        # Replacing the original http adapter with the new one
    s.mount('https://', b) 				# Replacing the original https adapter with the new one
    filename = date + name

    f = open(filename, 'a')				# Creation of the extract file
    while count < max_page:	        		# While loop start , the integer here will indicate the number of page you want to fetch. 
        data = {					# The data we will snd to the API
        'api_id': api_id,                               # the api_id
        'api_key': api_key,                             # the api key
        'site_id': site_id,                             # the incapusla site id (can be found in the web ui url)
        'time_range': time_range,                       # for a custom time range
        'page_size': page_size,                         # max event for one page
        'start': stEpoch,                               # Start date of the extract (epoch time see :http://www.epochconverter.com/ )
        'end': enEpoch,                                 # End date of the extract (epoch time see :http://www.epochconverter.com/ )
        'page_num' : page
        } 

        response = s.post(url, data=data, timeout=21 )  
        f.write(response.content + '\n')	                            # Writing the data to the file
        timer = s.post(url, data=data, timeout=21 ).elapsed.total_seconds() # Timer variable
        print "Wrote", colored('successfully', 'green'), "incapsula events page", page, "| of", client, "| within:", timer, "seconds", "| will now try to write page", page + 1

        count = count + 1				# Incrementation of the count Value
        page = page + 1					# Incrementation of the page Value
        time.sleep(0.2)					# Wait 0.2 sec, since the API is very slow to respond

    else:
        f.close()									# Closing extract file
        print colored('DONE !','green'),"filename is", colored(filename,'yellow')	# Print status


    #count events and incidents
    count_event = 0
    count_incident = 0
    total = []
    total_f = 0
    with open(filename, 'r') as r:
        read_f = r.read()
        count_event = read_f.count('{\"id\":')
        count_incident = re.findall('\":([1-9][0-9]{0,2}|1000)},', read_f)
        total = total + count_incident
    for n in total:
        total_f = total_f + int(n)
    print "there is " + str(count_event) + " events and " + str(total_f) + " incidents"
    if count_event >= 1000:
        print colored('\n/!\\WARNING/!\\','red' ) + " there is more than 1000 events, please relaunch the script 2 times or more with different time range." + colored(' /!\\WARNING/!\\','red' ) + "\n\n1): Please delete " + colored(filename, 'yellow') + "\n2): relaunch the script one time with for example" + colored (" 2017-01-01","green") + " as the start date and" + colored (" 2017-01-15 ","green") + "as the end date. \n3): launch the script a second time with for example" + colored (" 2017-01-15","green") + " as the start date and" + colored (" 2017-02-01","green") + " as the end date."

#begin fetching all websites
else:

#date selection
    isdate = raw_input("enter the" + colored(" start date","yellow") + " and" + colored(" end date","yellow")+ " of the desired export range," +" date format must be" + colored(" YYYY-MM-DD.","green")+"\nFor example, if you want to extract the events of january 2017 you must input" + colored (" 2017-01-01","green") + " as the start date and" + colored (" 2017-02-01","green") + " as the end date." + "\n\nPlease, enter the" + colored(" start date: ","yellow"))
    validate(isdate)
    iedate = raw_input("\nEnter now the" + colored(" end date: ","yellow"))
    validate(iedate)
    
    def run_all():
        sitec = 1
        procs = []
        for i in xrange(0, max_sites):
            proc = subprocess.Popen([sys.executable, script_name], stdin=subprocess.PIPE)#, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            procs.append(proc.stdin.write(str(sitec) + "\n" + isdate + "\n" + iedate + "\n")) #and (proc.stdout.write(log_file)))
            proc.stdin.close()
            print("Website " + str(sitec) + " -> ")
            sitec = sitec+1
        for proc in procs:
            try:
                proc.wait()
            except:
                pass

    run_all()

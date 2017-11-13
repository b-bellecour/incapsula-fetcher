#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4  smartindent

from etc.config import *

print(
"                                                          \n"
"                                                          \n"
"         _/_/_/    _/_/_/    _/_/_/_/                     \n"
"        _/    _/  _/    _/  _/                            \n"
"       _/_/_/    _/_/_/    _/_/_/                         \n"
"      _/    _/  _/    _/  _/                              \n"
"     _/_/_/    _/_/_/    _/_/_/_/                         \n"
"                                                          \n"
"        Baptiste Bellecour 2017                           \n"
"                                                          \n"
"        incapsula parser script                           \n"
"                                                          \n"
"                                                          \n\n")


# contact/dev : baptiste@bellecour.io



#defining date filename and URI
ddate =  (time.strftime("%Y-%m-%d"))
filename = (sys.argv[-1].replace('.json','.txt'))
dname = uri(sys.argv[-1])

#checking arguments, print usage if args is not written

if len(sys.argv[1:])==0:
    print "Script usage : ./parse-fitos.py" + colored(" File.json","green") + " -->  Exemple: ./parse-fitos.py" + colored( " 201702XX-raw-extract-fitos.json\n\n", "green")
    sys.exit()

print "Parsing data from JSON file :"

#load file, deleting unnecessary carriage return, count the file lines

g = open('page.txt', 'w')
with open(sys.argv[-1],'r') as f:
    insert = f.read()
    deline = insert.replace('\n\n','\n')
    g.write(deline)
g.close()
num_lines = sum(1 for line in open('page.txt'))

#Parse the created JSON dict to text file that splunk/excel can easily read

g = open('monthlyLogShort.txt', 'w')
with open('page.txt','r') as f:
    data = f.readlines()
    countp = 0
    page = 0
    while countp < num_lines:
	parse = json.loads(data[page])	# load the JSON dict
	field_list = parse["visits"]
	for fields in field_list:	# extract the the following field
	    try:
	        print >> g , "visit_id=",(fields["id"]),",","src_country=",(fields["country"]),",", "event_timestamp=",(fields["startTime"]),",","src_ip=",(fields["clientIPs"]),",","dest_name=", dname,",","dest_id=",(fields["siteId"]),",","signature=",(fields['securitySummary'])
	    except KeyError:
	        pass
		print colored("API responded that some event(s) contained signature(s) with an empty value" , "red")
	countp = countp + 1
        page = page + 1
    else:
	g.close()

print "Parsing the created JSON dict to text file that splunk/excel can easily read.", colored('OK!','green')

f = open('monthlyLogShort.txt','r')
fread = f.read()
kirei = fread.replace('= ','=').replace('[u\'','').replace('[{u\'','').replace('u\'','').replace('\'','').replace('\']','').replace(' , ',', ').replace('GET ','').replace('[u','').replace(']','').replace(': ','=').replace(':','=').replace('endTime', 'event_endtime').replace('clientIPs' , 'src_ip')  # delete / rename replace strings 
f.close()		
f = open('monthlyLogShort.txt','w')
f.write(kirei)

f.close()

print "Counting and parsing the threats, adding a carriage return for each of them.", colored('OK!','green')
# implementation of the threat count function

f = open('monthlyLogShort.txt','r')
kensu = f.readlines()
f.close()
sig_str = 'signature={'
f = open('flog.txt','w')
for line in kensu:
    record, signature = line.split(sig_str)		
    threats = signature.split('}')[0]
    for counts in threats.split(','):
	if '=' in counts:
	    threat, count = tuple(counts.split('='))
	    for i in range(int(count)):
	        print >> f, '%s%s%s}' % (record, sig_str, threat.strip())
f.close()

print "Converting epoch time into human friendly date.", colored('OK!','green')
				
#formating lines if a missing signature is present

f = open('flog.txt','r')
fread2 = f.read()
kir = fread2.replace('signature=vi','signature=\nvi') # delete / rename replace strings
f.close()
f = open('flog.txt','w')
f.write(kir)


# extract the timestamp and write it to tstamp.txt

f = open('flog.txt','r')
g = open("tstamp.txt", 'w')
date = f.readlines()
f.close()
for tline in date:
    tst = tline.find('event_timestamp=')
    tend = tline.find(' src_ip')
    tunprecise = tline[tst:tend+1]
    stamp = str(re.search(r'\d+', tunprecise).group())
    stamp = stamp[:-3]
    print >> g, stamp
g.close()
f.close()


#convert epoch time into human friendly date

g = open("conv.txt", 'w')
f = open("tstamp.txt", 'r')
fdate = f.readlines()
f.close()
fdate2 =[float(con) for con  in fdate]
for fline in fdate2:
    conv = time.ctime(float(fline))
    print >> g, conv
g.close()

#write the readable date in the file monthlyLogShort.txt

h = open("monthlyLogShort.txt",'w')
with open("flog.txt") as tmp1, open("conv.txt") as tmp2:
    for xt, yt in izip(tmp1, tmp2):
        xt = xt.strip()
        yt = yt.strip()
        print >> h,("{0}\t{1}".format (yt, xt))
h.close()

print "Writing the readable date on each lines.", colored('OK!','green')

#deleting lines contraining empty signature

k = open('monthlyLogShort.txt','r')
sigDel = k.readlines()
k.close()
l = open('monthlyLogShort.txt','w')
for line in sigDel:
    if not "signature=\n" in line:
        print >> l, line
l.close ()

print "Searching and deleting lines with an empty signature", colored('OK!','green')

# Formating last imperfections

f = open('monthlyLogShort.txt','r')
finalread = f.read()
kirei2 = finalread.replace('        isit',' visit').replace('api.threats.illegal_resource_access','Illegal Resource Access').replace('api.threats.bot_access_control','Bad Bots').replace('{','').replace('}','').replace('api.threats.sql_injection','SQL Injection').replace('api.threats.cross_site_scripting','Cross Site Scripting').replace('api.threats.remote_file_inclusion','Remote File Inclusion').replace('api.threats.customRule','IncapRules').replace('api.threats.ddos','DDoS').replace('api.threats.backdoor','Backdoor Protect').replace('\n\n','\n').replace('\n',', \n').replace('[','N/A').replace('api.acl.blacklisted_ips','REQ_BLOCKED_ACL')
f.close()
f = open(filename,'w')
f.write(kirei2)

f.close ()

print "Formating last imperfections.", colored('OK!','green')

#Cleaning the folder
#Comment the line below for debuf purpose
os.remove("flog.txt"), os.remove("conv.txt"), os.remove("page.txt"), os.remove("tstamp.txt"), os.remove("monthlyLogShort.txt")

print "Cleaning the folder, deleting temp files.", colored('OK!','green')

print  colored('DONE!','green')," Filename is", colored(filename, 'yellow')

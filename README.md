# Incapsula event fetcher

## Prerequisite

- Linux / Unix kernel
- Python 2.7
- pip
- pip install -U requests[security]
- pip install -U termcolor

## Usage

### 1 - configuring the etc/config.py
- set the api_id
- set the api_key
- set the site_id(s)
- set the "print site selector info"
- set the script ouput Filename -> "name" variable
- set the website url -> "client" variable
- check the config files comments for customizing more options. 


### 2 - Fetching and extracting incapsula events

- ./export_incap.py
- Enter a start date and an end date (Since the incapsula's API is pretty slow I recommend not to exceed one month)
- The output will be a Json file, 100 events max per line.

### 3 - Parsing the json file to a human/splunk friendly file

- parse.py 2017-10-XX-website-1.json (Can only parse json file created by the first script export_incap.py)
- The output will a txt file, Parsing events into incidents ( One event can contain multiple incidents)

### 4 - Sample files

- You can find one .json sample which is the Output of export_incap.py. You can parse this .json with parsed.py And produce .txt file

- You can find 2017-10-XX-website-1.text, which is the output of parsed.py.


#!/usr/bin/python

import requests
import pprint
import argparse
import json

#
# This is a sample program intended to demonstrate dumping information from Plutora
# it requires previously 'set up' access to Plutora (client_id and client_secret, etc)
# in JSON-format, contained in a file named credentials.cfg (by default).
# Additionally, the -p parameter specifies the URL 'suffix' which we would like to
# 'dump'
# If the user wants to use a different filename, the switch '-f <filename>' also works.
#

def plutoraDump(clientid, clientsecret, PlutoraUsername, PlutoraPassword, dumpEntity):
    # Set up JSON prettyPrinting
    pp = pprint.PrettyPrinter(indent=4)
    
    # Setup to obtain Get authorization-token
    authTokenUrl = "https://usoauth.plutora.com/oauth/token"
    payload = 'client_id=' + clientid + '&client_secret=' + clientsecret + '&grant_type=password&username='
    payload = payload + PlutoraUsername + '&password=' + PlutoraPassword + '&='
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'postman-token': "bc355474-15d1-1f56-6e35-371b930eac6f"
        }
    
    # Connect to get Plutora access token for subsequent queries
    authResponse = requests.post(authTokenUrl, data=payload, headers=headers)
    if authResponse.status_code != 200:
        print('Get auth-release status code: %i' % authResponse.status_code)
        print('plutoraDump.py: Sorry! - [failed on getAuthToken]: ', authResponse.text)
        exit('Sorry, unrecoverable error; gotta go...')
    else:
        accessToken = authResponse.json()["access_token"]
    
    # Setup to query Plutora instances
    plutoraBaseUrl= 'https://usapi.plutora.com'
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "authorization": "bearer "+accessToken,
        "cache-control": "no-cache",
        "postman-token": "bc355474-15d1-1f56-6e35-371b930eac6f"
    }

    try:
        # Experiment -- Get Plutora information for all system releases, or systems, or just the organization-tree
        r = requests.get(plutoraBaseUrl+dumpEntity, data=payload, headers=headers)
        if r.status_code != 200:
            print('Get release status code: %i' % r.status_code)
            print('\nplutoraDump.py: too bad sucka! - [failed on Plutora get]')
            exit('Sorry, unrecoverable error; gotta go...')
        else:
            pp.pprint(r.json())

    except Exception,ex:
        # ex.msg is a string that looks like a dictionary
        print "EXCEPTION: %s " % ex.msg
        exit('Error during API processing [POST]')
        
if __name__ == '__main__':
   # parse commandline and get appropriate passwords/configuration-items
   #
   parser = argparse.ArgumentParser(description='Get configuration-filename and item to dump')
   parser.add_argument('-f', action='store', dest='config_filename',
                       help='Config filename ')
   parser.add_argument('-p', action='store', dest='dump_item',
                       help='Plutora entity to dump (e.g. "/systems")')
   results = parser.parse_args()
   dump_entity = results.dump_item

   config_filename = results.config_filename
   if config_filename == None:
       config_filename = 'credentials.cfg'

   try:
      # If we don't specify a configfile on the commandline, assume one & try accessing
      # using the specified/assumed configfilename, grabbing ClientId & Secret from the JSON (manual setup of Plutora Oauth authorization.
      with open(config_filename) as data_file:
             data = json.load(data_file)
      client_id = data["credentials"]["client_id"]
      client_secret = data["credentials"]["client_secret"]
      plutora_username = data["credentials"]["username"].replace('@','%40')
      plutora_password = data["credentials"]["password"]
   except Exception, ex:
          # ex.msg is a string that looks like a dictionary
          print "EXCEPTION: %s " % ex.msg
          exit('couldnt open file {0}'.format(config_filename))

# Now that everything else is 'set up', go call the logon/dump routine, displaying the dump_entity
   plutoraDump(client_id, client_secret, plutora_username, plutora_password, dump_entity)

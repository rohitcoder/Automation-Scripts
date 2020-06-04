#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, boto3, json, pdb, requests, json, time, os
### Installation process 
## pip install boto3 pdb requests
## Run this script using $ python ec2_automation.py instance-id start

Usage = "\n\t Usage: {0} <Instance-ID> (start|stop|status)".format( sys.argv[0])
exampleUsage = "\n\t Example,\n\n\t\t {0} i-0f16c05ae009649fa status \n\n".format( sys.argv[0])
try:
    # Check if three arguments are there
    if len(sys.argv) != 3:
        print "\n\t Three(3) arguments expected, {0} given.".format( len(sys.argv) )
        print exampleUsage
        sys.exit(1)

    cmdarg = sys.argv[2]
    if cmdarg not in ['start','stop','status']:
        print "\n\t Unknown Argument: '{0}'".format( cmdarg )
        print Usage
        print exampleUsage
        sys.exit(1)      

except IndexError:
    print "\n\nMissing Argument(s)"
    print Usage
    print exampleUsage
    sys.exit(1)


client = boto3.client('ec2',region_name='ap-south-1')
resp = client.describe_instances()

"""
Funtion to get the Intance IDs
@arg - response from boto describe instances call
Returns a dictionary , Key - Instance ID, Value (Type :Dict) : Status & Tag-Name
"""
def getInstanceId(resp):
    # Describe instances returns an dict of reservations
    instanceDict = {}

    if resp['Reservations']:
        for item in resp['Reservations']:
            if item['Instances']:
                instanceMetaData = {} 
                instanceMetaData['Status'] = item['Instances'][0]['State']['Name']
                instanceMetaData['Tag-Name'] = item['Instances'][0]['Tags'][0]['Value']
                if "PublicIpAddress" in item['Instances'][0]:
                    instanceMetaData['PublicIpAddress'] = item['Instances'][0]['PublicIpAddress']
                    instanceMetaData['PrivateIpAddress'] = item['Instances'][0]['PrivateIpAddress']
                else:
                    instanceMetaData['PublicIpAddress'] = ""
                    instanceMetaData['PrivateIpAddress'] = ""
            instanceDict[ item['Instances'][0]['InstanceId'] ] = instanceMetaData
    return instanceDict

def setInstanceStatus(resp):
    instanceDict = getInstanceId(resp) 
    if instanceDict:
        # If the instance exists in the reservations,
        if sys.argv[1] not in instanceDict:
            print "\n\t Invalid Instance ID - {0}".format ( sys.argv[1])
            print "\nFound the following instances,"
            displayInstances( instanceDict )
            sys.exit(1)
    else:
        print "\n\n\t There are no running Reservations-Instances in your account.\n\n"
        sys.exit(1)

    if cmdarg == 'status':
        if instanceDict[sys.argv[1]]['Status'] == 'running':
            public_ip = instanceDict[sys.argv[1]]['PublicIpAddress']
            private_ip = instanceDict[sys.argv[1]]['PrivateIpAddress']
            ## Lets start updating our Cloudflare DNS Records, Reference => https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
            headers = {
                'X-Auth-Email': 'YOUR_CLOUDFLARE_EMAIL_HERE',
                'X-Auth-Key': 'YOUR_CLOUDFLARE_AUTH_KEY',
                'Content-Type': 'application/json',
            }
            data = '{"type":"A","name":"live","content":"'+public_ip+'","ttl":120,"proxied":true}'
            response = requests.put('https://api.cloudflare.com/client/v4/zones/:zone_identifier/dns_records/:identifier', headers=headers, data=data)
            if json.loads(response.text)['success'] == True:
                print("Udpated DNS Record!")
            else:
                print("Unable to update DNS Record!")
            ## DNS Records updated!
        else:
            print("Unable to update DNS record, because it was not in Running state")
        print "Instance '{0}' {1} status is: {2}".format( sys.argv[1], instanceDict[sys.argv[1]]['Tag-Name'] , instanceDict[sys.argv[1]]['Status'])
    
    if cmdarg == 'start':
        # No validation is done for this argument, assuming proper instance ID being passed
        if instanceDict[sys.argv[1]]['Status'] == 'stopped':
            print "Starting instance '{0}'  {1}".format( sys.argv[1], instanceDict[sys.argv[1]]['Tag-Name'])
            resp = client.start_instances( InstanceIds=[sys.argv[1]])
            ## After launching instance lets wait for 6 seconds and then update DNS Records
            time.sleep(6) 
            os.system('python '+os.path.realpath(__file__)+' '+sys.argv[1]+' status')

        else:
            print "skipped: '{0}' {1} state is {2}".format( sys.argv[1], instanceDict[sys.argv[1]]['Tag-Name'], instanceDict[sys.argv[1]]['Status'])
    
    if cmdarg == 'stop':
        if instanceDict[sys.argv[1]]['Status'] == 'running':
            print "stopping instance '{0}'  {1}".format( sys.argv[1], instanceDict[sys.argv[1]]['Tag-Name'])
            resp = client.stop_instances( InstanceIds=[sys.argv[1]])
        else:
            print "skipped: '{0}' {1} state is {2}".format( sys.argv[1], instanceDict[sys.argv[1]]['Tag-Name'], instanceDict[sys.argv[1]]['Status'])

def displayInstances(instanceDict):
    print json.dumps(instanceDict, indent=4,sort_keys=True)

setInstanceStatus(resp)

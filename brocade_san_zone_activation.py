#!/usr/bin/python
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.

from urllib import request
import requests
import json


documentation = '''
Python code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team.
Functions:
    Logging into Brocade switch
    Taking backup of existing zone configuration
    Creating alias
    Creating zone
    Committing zone information
    Adding new zones configuration
    Permanently saving switch configuration
    Logout from the Brocade switch
'''
sys_id = ""
number = ""

class BrocadeZoneActivation:

    """Code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team."""

    def __init__(self, snow_endpoint, snow_user, snow_pass, brocade_ip, username, password, alias_name, wwn, zone_name):
        """Default constructor to initialize the object with values"""
        self.snow_endpoint = snow_endpoint
        self.snow_user = snow_user
        self.snow_pass = snow_pass
        self.ip = brocade_ip
        self.username = username
        self.password = password
        self.alias_name = alias_name
        self.wwn = wwn
        self.zone_name = zone_name
        print("Default constructor being invoked")


    def servicenow_read_data(self):
        """Fetching the required values from ServiceNow RITM table to execute automation pipeline"""
        print("Fetching the required values from ServiceNow RITM table to execute automation pipeline")
        url = "https://" + self.snow_endpoint + "/api/now/table/sc_req_item/0c75a4162f3a5d107572fe7cf699b680?sysparm_fields=sys_id%2Cnumber%2Cstate%2Cvariables.ip%2Cvariables.alias%2Cvariables.wwn_1%2Cvariables.wwn_2%2Cvariables.zone"
        user = self.snow_user
        password = self.snow_pass
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        response = requests.get(url, auth=(user, password), headers=headers)
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

        data = response.json()
        print(data)
        global sys_id
        sys_id = data['result']['sys_id']
        global number
        number = data['result']['number']


    def serviceNow_update_record(self):
        """Updating the RITM record to work-in-progress state within ServiceNow portal"""
        print("Updating the RITM record to work-in-progress within ServiceNow portal")
        url = "https://" + self.snow_endpoint + "/api/now/table/sc_req_item/" + sys_id
        user = self.snow_user
        password = self.snow_pass
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        response = requests.patch(url, auth=(user, password), headers=headers, data='{\"state\":\"2\"}')
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        
        data = response.json()
        print("RITM state = ", data['result']['state'])


brocade = BrocadeZoneActivation('dev78611.service-now.com', 'admin', 'e0uRn=Ph$J4Y', '10.60.22.214', 'admin', 'ctcemc123', 'Axel_spa_A1Port3_Test, Rodge_spa_A4Port3_Test', '50:06:01:63:08:60:1d:e8, 50:06:01:63:08:64:0f:45', 'Axel_Rodge_SPA_Test')
brocade.servicenow_read_data()
brocade.serviceNow_update_record()

#!/usr/bin/python
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.

from wsgiref import headers
import requests


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

snow_endpoint = ""

class BrocadeZoneActivation:

    """Code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team."""

    def __init__(self, snow_endpoint, snow_user, snow_pass, brocade_ip, username, password, alias_name, wwn, zone_name):
        """Default constructor to initialize the object with values"""
        self.snow_ip = snow_endpoint
        self.snow_user = snow_user
        self.snow_pass = snow_pass
        self.ip = brocade_ip
        self.username = username
        self.password = password
        self.alias_name = alias_name
        self.wwn = wwn
        self.zone_name = zone_name
        print("Default constructor being invoked")


    def servicenow_read_data():
        """Fetching the required values from ServiceNow RITM table to execute automation pipeline"""
        url = "https://" + snow_endpoint + "/api/now/table/sc_req_item/0c75a4162f3a5d107572fe7cf699b680?\
            sysparm_fields=sys_id%2Cnumber%2Cstate%2C\
                variables.ip%2C\
                variables.alias%2C\
                variables.wwn_1%2C\
                variables.wwn_2%2C\
                variables.zone"
        user = "admin"
        password = "e0uRn=Ph$J4Y"
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        response = requests.get(url, auth=(user, password), headers=headers)
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())

        data = response.json()
        print(data)

        
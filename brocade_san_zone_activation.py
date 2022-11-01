#!/usr/bin/python
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.

import requests

documentation = '''
Python code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team.
Functions:
    Connecting to ServiceNow to retrieve RITM values
    Updating the ServiceNow RITM with 'work-in-progress' state
    Logging into Brocade switch
    Taking backup of existing zone configuration
    Creating alias
    Creating zone
    Committing zone information
    Adding new zones configuration
    Permanently saving switch configuration
    Logout from the Brocade switch
    Closing the ServiceNow RITM with required updates
'''
sys_id = ""
number = ""


class BrocadeZoneActivation:
    """Code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team."""

    def __init__(self, snow_endpoint, snow_user, snow_pass, brocade_ip, username, password, alias_name, wwn, zone_name):
        """
        :param snow_endpoint: ServiceNow dev instance endpoint
        :param snow_user: ServiceNow username for RestAPI calls
        :param snow_pass: ServiceNow password for calling RestAPI calls
        :param brocade_ip: Brocade dev instance IP address
        :param username: Brocade Fabric OS RestAPI username
        :param password: Brocade Fabric OS RestAPI password
        :param alias_name: Alias for the Host to Storage zone
        :param wwn: World-wide Name of HBA (Node)
        :param zone_name: Host to Storage mapping zone name
        """

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
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: RITM sysid required for subsequent calls
        :return: RITM number, where this is coming from ServiceNow RITM table
        """
        try:
            print("Fetching the required values from ServiceNow RITM table to execute automation pipeline")
            url = "https://" + self.snow_endpoint + "/api/now/table/sc_req_item/0c75a4162f3a5d107572fe7cf699b680?" \
                "sysparm_fields=sys_id%2Cnumber%2Cstate%2Cvariables.ip%2C" \
                    "variables.alias%2Cvariables.wwn_1%2Cvariables.wwn_2%2Cvariables.zone"
            user = self.snow_user
            password = self.snow_pass
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            response = requests.get(url, auth=(user, password), headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(data)
                global sys_id
                sys_id = data['result']['sys_id']
                global number
                number = data['result']['number']
        except Exception as e:
            if response.status_code != 200:
                print('Status: ', response.status_code, 'Headers: ', response.headers, 'Error Response: ', response.json())
                print(e)

    def servicenow_update_record(self):
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: None
        """
        try:
            print("Updating the RITM record to work-in-progress within ServiceNow portal")
            url = "https://" + self.snow_endpoint + "/api/now/table/sc_req_item/" + sys_id
            user = self.snow_user
            password = self.snow_pass
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            response = requests.patch(url, auth=(user, password), headers=headers, data='{\"state\":\"2\"}')
            if response.status_code == 200:
                data = response.json()
                print("RITM state = ", data['result']['state'])
        except Exception as e:
            if response.status_code != 200:
                print('Status: ', response.status_code, 'Headers: ', response.headers, 'Error Response: ', response.json())

    def brocade_api_login(self):
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: Bearer token for the subsequent Brocade RestAPI calls
        """
        try:
            url = 'http://' + self.ip + '/rest/login'
            user = self.username
            pwd = self.password
            headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json'}
            response = requests.post(url, headers=headers, auth=(user, pwd), verify=False)
            if response.status_code == 200:
                custom_api_key = response.headers.get('Authorization')
                print('Custom Token: ', custom_api_key)
        except Exception as e:
            if response.status_code != 200:
                print('Status: ', response.status_code, 'Error Resonse: ', response.json())
                print(e)


brocade = BrocadeZoneActivation('dev78611.service-now.com', 'admin', 'e0uRn=Ph$J4Y', '10.60.22.214', 'admin',
                                'ctcemc123', 'Axel_spa_A1Port3_Test, Rodge_spa_A4Port3_Test',
                                '50:06:01:63:08:60:1d:e8, 50:06:01:63:08:64:0f:45', 'Axel_Rodge_SPA_Test')
brocade.servicenow_read_data()
brocade.servicenow_update_record()
brocade.brocade_api_login()

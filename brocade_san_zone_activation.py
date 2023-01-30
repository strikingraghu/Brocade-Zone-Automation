#!/usr/bin/python
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.

import requests
import json

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


class BrocadeZoneActivation:
    """Code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team."""

    sysid = ""
    number = ""
    custom_api_key = ""
    current_config_backup = ""
    pre_change_checksum = ""
    pre_change_cfg_name = ""
    enabled_zones = ""
    zones = []

    def __init__(self, snow_endpoint, rsysid, snow_user, snow_pass, brocade_ip, username, password, alias_name_1,
                 wwn_1, alias_name_2, wwn_2, zone_name):
        """
        :param snow_endpoint: ServiceNow dev instance endpoint
        :param rsysid: ServiceNow catalog item sysid in ServiceNow platform
        :param snow_user: ServiceNow username for RestAPI calls
        :param snow_pass: ServiceNow password for calling RestAPI calls
        :param brocade_ip: Brocade dev instance IP address
        :param username: Brocade Fabric OS RestAPI username
        :param password: Brocade Fabric OS RestAPI password
        :param alias_name_1: Alias for the Host to Storage zone
        :param wwn_1: World-wide Name of HBA (Node)
        :param alias_name_2: Alias for the Host to Storage zone
        :param wwn_2: World-wide Name of HBA (Node)
        :param zone_name: Host to Storage mapping zone name
        """

        self.snow_endpoint = snow_endpoint
        self.rsysid = rsysid
        self.snow_user = snow_user
        self.snow_pass = snow_pass
        self.ip = brocade_ip
        self.username = username
        self.password = password
        self.alias_name_1 = alias_name_1
        self.wwn_1 = wwn_1
        self.alias_name_2 = alias_name_2
        self.wwn_2 = wwn_2
        self.zone_name = zone_name
        print("Default constructor being invoked")

    def servicenow_read_data(self):
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: As a global variable, RITM sysid required for subsequent calls
        :return: As a global variable, RITM number, where this is coming from ServiceNow RITM table
        """
        try:
            print("Fetching the required values from ServiceNow RITM table to execute automation pipeline")
            url = "https://" + self.snow_endpoint + "/api/now/table/sc_req_item/" + self.rsysid + "?sysparm_fields=" \
                                                    "sys_id%2Cnumber%2Cstate%2Cvariables.ip%2Cvariables.alias%2C" \
                                                    "variables.wwn_1%2Cvariables.wwn_2%2Cvariables.zone"
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
                print("SysID generated & RITM number = ", sys_id, " & ", number)
        except Exception as e:
            if response.status_code != 200:
                print('Status: ', response.status_code, 'Headers: ', response.headers, 'Error Response: ',
                      response.json())
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
                print('Status: ', response.status_code, 'Headers: ', response.headers, 'Error Response: ',
                      response.json())

    def api_login(self):
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: As a global variable, Bearer token for the subsequent Brocade RestAPI calls
        """
        try:
            print("Login to the Brocade RestAPI and fetch the custom token")
            url = 'http://' + self.ip + '/rest/login'
            user = self.username
            pwd = self.password
            headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json'}
            response = requests.post(url, headers=headers, auth=(user, pwd), verify=False)
            if response.status_code == 200:
                global custom_api_key
                custom_api_key = response.headers.get('Authorization')
                print('Custom Token: ', custom_api_key)
        except Exception as e:
            if response.status_code != 200:
                print('Status: ', response.status_code, 'Error Resonse: ', response.json())
                print(e)

    def zones_current_configs(self):
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: As a global variable, configuration backup of the Brocade SAN device
        """
        try:
            print("Latest backup of the Brocade SAN switch configuration is stored in cache!")
            url = 'http://' + self.ip + '/rest/running/brocade-zone/effective-configuration'
            headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json',
                       'Authorization': custom_api_key}
            response = requests.get(url, headers=headers)
            data = response.json()
            if response.status_code == 200:
                global current_config_backup
                current_config_backup = response.content
                global pre_change_checksum
                pre_change_checksum = data['Response']['effective-configuration']['checksum']
                global pre_change_cfg_name
                pre_change_cfg_name = data['Response']['effective-configuration']['cfg-name']
                global enabled_zones
                enabled_zones = data['Response']['effective-configuration']['enabled-zone']
                print(enabled_zones)
                for get_zone_name in enabled_zones:
                    zones.append([get_zone_name['zone-name']])
                print("List of all zones before change: ", zones)
                print("Current checksum value: ", pre_change_checksum)
                print("Current cfg-name before changes: ", pre_change_cfg_name)
        except Exception as e:
            if response.status_code != 200:
                print('Status: ', response.status_code, 'Error Resonse: ', response.json())
                print(e)

    def alias_creation(self):
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: None
        """
        try:
            print("Aliases will be created for provided WWWNs in the ServiceNow RITM record")
            url = 'http://' + self.ip + '/rest/running/brocade-zone/defined-configuration/alias'
            headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json',
                       'Authorization': custom_api_key}
            body = {'alias': {'alias-name': self.alias_name_1, 'member-entry': {'alias-entry-name': self.wwn_1}}}
            body_json_compatible = json.dumps(body, indent=3)
            response = requests.post(url=url, headers=headers, data=body_json_compatible, verify=False)
            alias_1 = response.status_code
            print(alias_1)
            if alias_1 == 201:
                print("Alias " + self.alias_name_1 + "creation status successful", response.json())
                body = {'alias': {'alias-name': self.alias_name_2, 'member-entry': {'alias-entry-name': self.wwn_2}}}
                body_json_compatible = json.dumps(body, indent=3)
                response = requests.post(url, headers=headers, data=body_json_compatible, verify=False)
                alias_2 = response.status_code
                print(alias_2)
                if alias_2 == 201:
                    print("Alias " + self.alias_name_2 + "creation status successful", response.json())
        except Exception as e:
            if alias_1 | alias_2 != 201:
                print('Status: ', response.status_code, 'Error Resonse: ', response.json())
                print(e)

    def zone_creation(self):
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: None
        """
        try:
            print("Zone will be created taking the aliases into consideration")
            url = 'http://' + self.ip + '/rest/running/brocade-zone/defined-configuration/zone'
            headers = {'Accept': 'application/yang-data+json', 'Content-Type': 'application/yang-data+json',
                       'Authorization': custom_api_key}
            body = {'zone': {'zone-name': self.zone_name, 'zone-type': 0,
                             'member-entry': {'entry-name': [self.alias_name_1, self.alias_name_2]}}}
            body_json_compatible = json.dumps(body, indent=3)
            response = requests.post(url, headers=headers, data=body_json_compatible, verify=False)
            data = response.json()
            if response.status_code == 201:
                print("Zone creation is successful", response.json())
        except Exception as e:
            if response.status_code != 201:
                print("Zone creation is not successful", response.json())
                print(e)

    def zone_config_update(self):
        """
        :param self: 'self' parameter is a reference to the current instance of the class
        :return: None
        """


brocade = BrocadeZoneActivation('dev78611.service-now.com', 'admin', 'e0uRn=Ph$J4Y', '10.60.22.214', 'admin',
                                'ctcemc123', 'Axel_Spa_A1Port3_Test', '50:06:01:63:08:60:1d:e8',
                                'Rodge_Spa_A4Port3_Test',
                                '50:06:01:63:08:64:0f:45', 'Axel_Rodge_SPA_Test')
brocade.servicenow_read_data()
brocade.servicenow_update_record()
brocade.api_login()
brocade.zones_current_configs()
brocade.alias_creation()
brocade.zone_creation()

#!/usr/bin/python
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.

from requests.auth import HTTPBasicAuth
import requests
import json

DOCUMENTATION = '''
Python code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team.
Functions:
    a) Logging into Brocade switch
    b) Taking backup of existing zone configuration
    c) Creating alias
    d) Creating zone
    e) Adding new zone configuration
    f) Saving new zone configuration
    g) Taking backup of switch after configuration changes
    h) Taking backup of zone configuration after changes
    i) Enabling port
    j) Disabling Port
    k) Logout from the Brocade switch
'''

# Generic Global Variables
custom_api_key = ""
switch_config_backup_json = ""


def brocade_san_switch_login(ipaddress, username, password):
    """
        :param ipaddress: Provide switch IP address
        :param username: Provide switch username (REST API user)
        :param password: Provide switch password (REST API user password)
        :return: Bearer token for subsequent calls
    """
    global custom_api_key
    try:
        login_url = 'http://' + ipaddress + '/rest/login'
        login = requests.request("POST", login_url, auth=HTTPBasicAuth(username, password))
        print("Brocade login status code: ", login.status_code)
        if login.status_code == 200:
            custom_api_key = login.headers.get('Authorization')
            print("Login API key retrieved: ", custom_api_key)
            print("Brocade switch login successful - ", ipaddress)
    except Exception as e:
        print("Brocade switch login not successful - ", ipaddress)
        print(e)
        print()


def brocade_san_switch_config_backup(ipaddress):
    """
    :param ipaddress: Provide switch IP address
    :return: Switch configuration data (Backup purpose)
    """
    global switch_config_backup_json
    call_config_backup = ""
    try:
        switch_config_url = 'http://' + ipaddress + '/rest/running/brocade-zone/effective-configuration'
        switch_config_backup_call_headers = {'Authorization': custom_api_key, 'Accept': 'application/yang-data+json',
                                             'Content-Type': 'application/yang-data+json'}
        call_config_backup = requests.get(url=switch_config_url, headers=switch_config_backup_call_headers)
        print("Switch zone data: ", call_config_backup)
        switch_config_backup_json = json.loads(call_config_backup.content)
        if call_config_backup.status_code == 200:
            print("Switch zone information backed up - ", switch_config_backup_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", call_config_backup.status_code)
        print(e)
        print()


def brocade_san_switch_alias_creation(alias_name, alias_entry_name, ipaddress):
    """
    :param alias_name: Provide alias name from the payload
    :param alias_entry_name: Provide WWN value from the payload for alias
    :param ipaddress: Provide switch IP address
    :return: alias creation status
    """
    switch_create_alias = ""
    switch_alias_creation_call_headers = {'Authorization': custom_api_key, 'Accept': 'application/yang-data+json',
                                          'Content-Type': 'application/yang-data+json'}
    call_data = '{"alias":{"alias-name": "' + alias_name + '", "member-entry": {"alias-entry-name": "' + \
                alias_entry_name + '"}}}'
    json_transformation = json.loads(call_data)
    print('Call body being used in this function: ', json_transformation)
    try:
        switch_create_alias_url = 'http://' + ipaddress + '/rest/running/brocade-zone/defined-configuration/alias'
        switch_create_alias = requests.post(url=switch_create_alias_url, headers=switch_alias_creation_call_headers,
                                            data=call_data)
        print("Alias creation status: ", switch_create_alias)
        switch_alias_create_json = json.loads(switch_create_alias.content)
        if switch_create_alias.status_code == 200:
            print("Alias creation is successful - ", switch_alias_create_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", switch_create_alias.status_code)
        print(e)
        print()


def brocade_san_switch_zone_creation(zone_name, zone_member_entry_name, ipaddress):
    """
    :param zone_name: Provide zone name from the payload
    :param zone_member_entry_name: Provide members that needs to be part of zone
    :param ipaddress: Provide switch IP address
    :return: zone creation status
    """
    switch_create_zone_element = ""
    switch_zone_creation_api_headers = {'Authorization': custom_api_key, 'Accept': 'application/yang-data+json',
                                        'Content-Type': 'application/yang-data+json'}
    call_data = '{"zone": {"zone-name": "' + zone_name + '", "zone-type": 0, "member-entry": ' \
                                                         '{"entry-name": [' + zone_member_entry_name + ']}}}'
    json_transformation = json.loads(call_data)
    print('Call body being used in this function: ', json_transformation)
    try:
        switch_create_zone_url = 'http://' + ipaddress + '/rest/running/brocade-zone/defined-configuration/zone'
        switch_create_zone_element = requests.post(url=switch_create_zone_url, headers=switch_zone_creation_api_headers,
                                                   data=call_data)
        print("Alias creation status: ", switch_create_zone_element)
        switch_create_zone_json = json.loads(switch_create_zone_element.content)
        if switch_create_zone_element.status_code == 200:
            print("Alias creation is successful - ", switch_create_zone_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", switch_create_zone_element.status_code)
        print(e)
        print()


brocade_san_switch_login('......', 'admin', '......')
brocade_san_switch_config_backup('......')
brocade_san_switch_alias_creation('Axel_spa_A1Port3_Test', '50:06:01:63:08:60:1d:e8', '......')
brocade_san_switch_alias_creation('Rodge_spa_A4Port3_Test', '50:06:01:63:08:64:0f:45', '......')
brocade_san_switch_zone_creation('Axel_Rodge_SPA_Test', '"50:06:01:63:08:60:1d:e8", "50:06:01:63:08:64:0f:45"',
                                 '......')

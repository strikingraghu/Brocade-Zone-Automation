#!/usr/bin/python
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.

from requests.auth import HTTPBasicAuth
import requests
import json

DOCUMENTATION = '''
Python code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team.
Functions:
    a) Logging into Brocade switch
    b) Taking backup of existing switch configuration
    c) Taking backup of existing zone configuration
    d) Creating alias
    e) Creating zone
    f) Adding new zone configuration
    g) Saving new zone configuration
    h) Taking backup of switch after configuration changes
    i) Taking backup of zone configuration after changes
    j) Enabling port
    k) Disabling Port
    l) Logout from the Brocade switch
'''

custom_basic_key = ""
switch_config_backup_json = ""


def brocade_san_switch_login(ipaddress, username, password):
    """
        :param ipaddress: Provide switch IP address
        :param username: Provide switch username (REST API user)
        :param password: Provide switch password (REST API user password)
        :return: Bearer token for subsequent calls
    """
    global custom_basic_key
    try:
        login_endpoint = 'http://' + ipaddress + '/rest/login'
        login = requests.request("POST", login_endpoint, auth=HTTPBasicAuth(username, password))
        print("Brocade login status code: ", login.status_code)
        if login.status_code == 200:
            custom_basic_key = login.headers.get('Authorization')
            print("Login API key retrieved: ", custom_basic_key)
            print("Brocade switch login successful - ", ipaddress)
    except Exception as e:
        print("Brocade switch login not successful - ", ipaddress)
        print(e)


def brocade_san_switch_config_backup(custom_token, ipaddress):
    """
    :param custom_token: Provide custom token fetched in previous call
    :param ipaddress: Provide switch IP address
    :return: Switch configuration data (Backup purpose)
    """
    global switch_config_backup_json
    call_config_endpoint = ""
    try:
        switch_config_endpoint = 'http://' + ipaddress + '/rest/running/brocade-zone/effective-configuration'
        call_headers = {'Authorization': custom_token, 'Accept': 'application/yang-data+json',
                        'Content-Type': 'application/yang-data+json'}
        call_config_endpoint = requests.get(url=switch_config_endpoint, headers=call_headers)
        print("Switch zone data: ", call_config_endpoint)
        switch_config_backup_json = json.loads(call_config_endpoint.content)
        if call_config_endpoint.status_code == 200:
            print("Switch zone information backed up - ", switch_config_backup_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", call_config_endpoint.status_code)
        print(e)


brocade_san_switch_login('10.60.22.214', 'admin', 'ctcemc123')
brocade_san_switch_config_backup(custom_basic_key, '10.60.22.214')

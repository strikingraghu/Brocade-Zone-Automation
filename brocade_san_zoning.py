#!/usr/bin/python
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.

from requests.auth import HTTPBasicAuth
import requests

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


def brocade_san_switch_login(ipaddress, username, password):
    """
        :param ipaddress: Provide switch IP address
        :param username: Provide switch username (REST API user)
        :param password: Provide switch password (REST API user password)
        :return: Bearer token for subsequent calls
    """
    try:
        login_endpoint = 'http://' + ipaddress + '/rest/login'
        login = requests.request("POST", login_endpoint, auth=HTTPBasicAuth(username, password))
        print("Brocade login status code: ", login.status_code)
        if login.status_code == 200:
            login_bearer_token = login.headers.get('Authorization')
            print("Login API key retrieved: ", login_bearer_token)
            print("Brocade switch login successful - ", ipaddress)
    except Exception as e:
        print("Brocade switch login not successful - ", ipaddress)
        print(e)


brocade_san_switch_login('172.24.2.113', 'rathnar', 'rathnar56')

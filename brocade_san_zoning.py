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
custom_api_key = "Custom_Basic YWRtaW46eHh4OmQ4NDE1ZGI5YTJiYjVhMjRiMTFkYWYxODFmOTIxYTk1NGI0NmM4NTk1OWFlZmQyYWQ2N2U1MjVlNTUwODUzNGE="
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
        switch_config_backup_json = json.loads(call_config_backup.content)  # Type conversion to dict is required
        print("Configuration data of the SAN switch before automation: ", switch_config_backup_json)
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
    call_data = {"alias": {"alias-name": alias_name, "member-entry": {"alias-entry-name": alias_entry_name}}}
    json_transformation = json.dumps(call_data, indent=2)
    print('Call body type being used in this function: ', type(json_transformation), json_transformation)
    try:
        switch_create_alias_url = 'http://' + ipaddress + '/rest/running/brocade-zone/defined-configuration/alias'
        switch_create_alias = requests.post(url=switch_create_alias_url, headers=switch_alias_creation_call_headers,
                                            data=json_transformation)
        print("Alias creation status: ", switch_create_alias.status_code)
        switch_alias_create_json = json.loads(switch_create_alias.content)
        if switch_create_alias.status_code == 201:
            print("Alias creation is successful - ", switch_alias_create_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", switch_create_alias.status_code)
        print(e)
        print()


def brocade_san_switch_zone_creation(zone_name, zone_member_entry_name_1, zone_member_entry_name_2, ipaddress):
    """
    :param zone_name: Provide zone name from the payload
    :param zone_member_entry_name_1: Provide member that needs to be part of zone
    :param zone_member_entry_name_2: Provide member that needs to be part of zone
    :param ipaddress: Provide switch IP address
    :return: zone creation status
    """
    switch_create_zone_element = ""
    switch_zone_creation_api_headers = {'Authorization': custom_api_key, 'Accept': 'application/yang-data+json',
                                        'Content-Type': 'application/yang-data+json'}
    call_data = {"zone": {"zone-name": zone_name, "zone-type": 0, "member-entry": {"entry-name":
                                                                                       [zone_member_entry_name_1,
                                                                                        zone_member_entry_name_2]}}}
    json_transformation = json.dumps(call_data, indent=2)
    print('Call body being used in this function: ', type(json_transformation), json_transformation)
    try:
        switch_create_zone_url = 'http://' + ipaddress + '/rest/running/brocade-zone/defined-configuration/zone'
        switch_create_zone_element = requests.post(url=switch_create_zone_url, headers=switch_zone_creation_api_headers,
                                                   data=json_transformation)
        print("Zone creation status: ", switch_create_zone_element)
        switch_create_zone_json = json.loads(switch_create_zone_element.content)
        if switch_create_zone_element.status_code == 201:
            print("Zone creation is successful - ", switch_create_zone_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", switch_create_zone_element.status_code)
        print(e)
        print()


def brocade_san_switch_zone_config_update(config_name, ipaddress):
    """
    :param config_name: Provide config name from SAN switch configuration data
    :param ipaddress: Provide switch IP address
    :return: zone save status
    """
    switch_save_zone_element = ""
    switch_zone_config_update_api_headers = {'Authorization': custom_api_key, 'Accept': 'application/yang-data+json',
                                             'Content-Type': 'application/yang-data+json'}
    call_data = {"cfg": {"cfg-name": config_name, "member-zone": {"zone-name": ["Axel_Dellpr740A",
                                                                                "Axel_Dellpr740C",
                                                                                "Axel_Rodge_SPA",
                                                                                "Axel_Rodge_SPB",
                                                                                "Rodge-Dellpr730H",
                                                                                "Rodge_Dellpr730E",
                                                                                "dellpr730B_Marge"]}}}
    json_transformation = json.dumps(call_data, indent=3)
    print('Call body being used in this function: ', json_transformation)
    try:
        switch_save_zone_url = 'http://' + ipaddress + '/rest/running/brocade-zone/defined-configuration/cfg'
        switch_save_zone_element = requests.patch(url=switch_save_zone_url,
                                                  headers=switch_zone_config_update_api_headers,
                                                  data=json_transformation)
        print("Zone configuration update status: ", switch_save_zone_element)
        switch_save_zone_json = json.loads(switch_save_zone_element.content)
        if switch_save_zone_element.status_code == 204:
            print("Zone configuration update is successful - ", switch_save_zone_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", switch_save_zone_element.status_code)
        print(e)
        print()


def brocade_san_switch_save_checksum(checksum_value, ipaddress):
    """
    :param checksum_value: Provide checksum value retrieved from step # 1 (login function)
    :param ipaddress: Provide switch IP address
    :return: Saving configuration to DB status code
    """
    switch_zonedb_save_element = ""
    switch_zone_config_save_zonedb_api_headers = {'Authorization': custom_api_key,
                                                  'Accept': 'application/yang-data+json',
                                                  'Content-Type': 'application/yang-data+json'}
    call_data = {"checksum": checksum_value}
    json_transformation = json.dumps(call_data, indent=2)
    print('Call body being used in this function: ', json_transformation)
    try:
        switch_zonedb_save_url = 'http://' + ipaddress + '/rest/running/brocade-zone/effective-configuration' \
                                                         '/cfg-action/1'
        switch_zonedb_save_element = requests.patch(url=switch_zonedb_save_url,
                                                    headers=switch_zone_config_save_zonedb_api_headers,
                                                    data=json_transformation)
        print("Zone configuration update status: ", switch_zonedb_save_element)
        switch_zonedb_save_zone_json = json.loads(switch_zonedb_save_element.content)
        if switch_zonedb_save_element.status_code == 204:
            print("Zone configuration is saved to device successful - ", switch_zonedb_save_zone_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", switch_zonedb_save_element.status_code)
        print(e)
        print()


def brocade_san_switch_get_new_checksum(ipaddress):
    """
    :param ipaddress: Provide switch IP address
    :return: Returns a new checksum value
    """
    switch_zone_get_new_checksum_element = ""
    switch_zone_get_new_checksum_api_headers = {'Authorization': custom_api_key,
                                                'Accept': 'application/yang-data+json',
                                                'Content-Type': 'application/yang-data+json'}
    try:
        switch_zone_get_new_checksum_url = 'http://' + ipaddress + '/rest/running/brocade-zone/' \
                                                                   'effective-configuration/checksum'
        switch_zone_get_new_checksum_element = requests.get(url=switch_zone_get_new_checksum_url,
                                                            headers=switch_zone_get_new_checksum_api_headers)
        print("Switch new checksum value: ", switch_zone_get_new_checksum_element)
        switch_zone_get_new_checksum_json = json.loads(switch_zone_get_new_checksum_element.content)
        if switch_zone_get_new_checksum_element.status_code == 200:
            print("Getting new checksum value successful - ", switch_zone_get_new_checksum_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", switch_zone_get_new_checksum_element.status_code)
        print(e)
        print()


def brocade_san_switch_enable_new_config(checksum_value, config_name, ipaddress):
    """
    :param checksum_value: Provide checksum value retrieved from the previous call
    :param config_name: Provide the latest configuration name used in switch's config output
    :param ipaddress: Provide switch IP address
    :return: Enabling new configuration on the SAN switch
    """
    switch_zone_enable_new_config_element = ""
    switch_zone_enable_new_config_api_headers = {'Authorization': custom_api_key,
                                                 'Accept': 'application/yang-data+json',
                                                 'Content-Type': 'application/yang-data+json'}
    call_data = {"checksum": checksum_value}
    json_transformation = json.dumps(call_data, indent=2)
    print('Call body being used in this function: ', json_transformation)
    try:
        switch_zone_enable_new_config_url = 'http://' + ipaddress + '/rest/running/brocade-zone/' \
                                                                    'effective-configuration/cfg-name/' + config_name
        switch_zone_enable_new_config_element = requests.patch(url=switch_zone_enable_new_config_url,
                                                               headers=switch_zone_enable_new_config_api_headers,
                                                               data=json_transformation)
        print("Zone configuration enablement status via new checksum: ", switch_zone_enable_new_config_element)
        switch_zone_enable_new_config_json = json.loads(switch_zone_enable_new_config_element.content)
        if switch_zone_enable_new_config_element.status_code == 204:
            print("Zone configuration is saved to device successful - ", switch_zone_enable_new_config_json)
    except Exception as e:
        print("Brocade switch login token or endpoint issues - ", switch_zone_enable_new_config_element.status_code)
        print(e)
        print()


# brocade_san_switch_login('10.60.22.214', 'admin', 'ctcemc123')
# brocade_san_switch_config_backup('10.60.22.214')
# brocade_san_switch_alias_creation('Axel_spa_A1Port3_Test', '50:06:01:63:08:60:1d:e8', '10.60.22.214')
# brocade_san_switch_alias_creation('Rodge_spa_A4Port3_Test', '50:06:01:63:08:64:0f:45', '10.60.22.214')
# brocade_san_switch_zone_creation('Axel_Rodge_SPA', '50:06:01:63:08:60:1d:e8', '50:06:01:63:08:64:0f:45',
#                                 '10.60.22.214')
# brocade_san_switch_zone_config_update('b238638', '10.60.22.214')
# brocade_san_switch_save_checksum('c9712b1df97e2cb9d2e692796d6fd415', '10.60.22.214')
# brocade_san_switch_get_new_checksum('10.60.22.214')
# brocade_san_switch_enable_new_config('bb5fc695fd1b28eb8856de776a244c35', 'b238638', '10.60.22.214')

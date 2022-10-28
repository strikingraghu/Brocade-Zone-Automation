#!/usr/bin/python
# The term 'Broadcom' refers to Broadcom Inc. and/or its subsidiaries.

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

class BrocadeZoneActivation:

    """Code developed for automating 'Brocade SAN Zoning' tasks performed by Network/Storage team."""

    def __init__(self, snow_endpoint, snow_user, snow_pass, brocade_ip, username, password, alias_name, wwn, zone_name):
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


    def service_now():
        print("Closing the ServiceNow calls")
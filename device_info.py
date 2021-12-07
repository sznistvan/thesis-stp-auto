#! /usr/bin/env python

# SW1 IOSvL2 Switch
sw1 = {
             "address": "198.18.1.101",
             "netconf_port": 22,
             "ssh_port": 22,
             "username": "cisco",
             "password": "cisco",
             "name": "SW1"
          }


# SW2 IOSvL2 Switch
sw2 = {
             "address": "198.18.1.102",
             "netconf_port": 22,
             "ssh_port": 22,
             "username": "cisco",
             "password": "cisco",
             "name": "SW2"
         }

# SW3 IOSvL2 Switch
sw3 = {
             "address": "198.18.1.103",
             "netconf_port": 22,
             "ssh_port": 22,
             "username": "cisco",
             "password": "cisco",
             "name": "SW3"
         }
# SW4 IOSvL2 Switch
sw4 = {
             "address": "198.18.1.104",
             "netconf_port": 22,
             "ssh_port": 22,
             "username": "cisco",
             "password": "cisco",
             "name": "SW4"
         }

# SW5 IOSvL2 Switch
sw5 = {
             "address": "198.18.1.105",
             "netconf_port": 22,
             "ssh_port": 22,
             "username": "cisco",
             "password": "cisco",
             "name": "SW5"
         }

def getDevices():
    return [sw1,sw2,sw3,sw4,sw5]
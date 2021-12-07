import xml.dom.minidom
import xmltodict
from pprint import pprint
import threading
from time import sleep
import datetime


import device_info as di
from device_info import sw1,sw2,sw3,sw4,sw5
from connector import connection


prio = '''
                        <config>
                            <cli-config-data>
                                <cmd>spanning-tree vlan %s priority %s </cmd>
                            </cli-config-data>
                        </config>'''

cost = '''
                        <config>
                            <cli-config-data>
                                <cmd>interface %s</cmd>
                                <cmd>spanning-tree vlan %s cost %s</cmd>
                            </cli-config-data>
                        </config>'''

def change_root(device,rprio,vlan):
    try:
        string_prio = prio % (str(vlan),rprio)
        with connection(device["address"],device["netconf_port"],device["username"],device["password"]) as devicem:
            reply=devicem.edit_config(target='running',config = string_prio)
            if(devicem.ok):
                # print(reply)
                print("Updated priority on "+str(device['name'])+" to "+rprio)
    except (ncclient.operations.errors.TimeoutExpiredError,
            ncclient.transport.errors.SSHError):
        print("Connection timed out or could not be established!")

def change_port_cost(device,inf,pcost,vlan):
    try:
        string_cost = cost % (inf,str(vlan),pcost)
        with connection(device["address"],device["netconf_port"],device["username"],device["password"]) as devicem:
            reply=devicem.edit_config(target='running',config = string_cost)
            if(devicem.ok):
                # print(reply)
                print("Updated cost on "+str(device['name'])+" on "+inf+ " to "+pcost)
    except (ncclient.operations.errors.TimeoutExpiredError,
            ncclient.transport.errors.SSHError):
        print("Connection timed out or could not be established!")

def Threaded(function,vlan):
    
    threads = len(di.getDevices())

    jobs = []
    for i in range(0,threads):
        thread = threading.Thread(target=function, args=(di.getDevices()[i],str(32768),vlan))
        jobs.append(thread)
        thread.start()

    for k in jobs:
        k.join()

def ThreadCost(function,edge_list,G,portcost,vlan):
    
    threads = len(edge_list)

    jobs = []
    for i in range(0,threads):
        a = edge_list[i][0]     #tupple-ben az él első végpontja
        b = edge_list[i][1]     #második végpontja
        #print("A and B nodes: "+str(a)+", "+str(b))
        adev = int(G[a][b]['port1'].split()[0])
        bdev = int(G[a][b]['port2'].split()[0])
        thread = threading.Thread(target=function, 
            args=(di.getDevices()[adev-1],G[a][b]['port1'].split()[1],str(portcost),vlan))
        #print(G.edges.data())
        jobs.append(thread)
        thread.start()

        thread = threading.Thread(target=function, 
            args=(di.getDevices()[bdev-1],G[a][b]['port2'].split()[1],str(portcost),vlan))
        jobs.append(thread)
        thread.start()

    for k in jobs:
        k.join()

if __name__ == '__main__':
    print("setdata")
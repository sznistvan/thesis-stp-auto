import xml.dom.minidom
import xmltodict
from pprint import pprint
import threading
from time import sleep
import datetime


import device_info as di
from device_info import sw1,sw2,sw3,sw4,sw5
from connector import connection

nodes = []
edges = []
returnable_edge_list = []

cdp = '''
                            <filter>
                                  <config-format-text-cmd>
                                     <text-filter-spec> | inc asd</text-filter-spec>
                                  </config-format-text-cmd>
                                  <oper-data-format-text-block>
                                     <exec>show cdp neighbors</exec>
                                  </oper-data-format-text-block>
                               </filter>
                             '''
hostname = '''
                            <filter>
                                  <config-format-text-cmd>
                                     <text-filter-spec> | inc hostname</text-filter-spec>
                                  </config-format-text-cmd>
                            </filter>
                             '''
edge = '''
                            <filter>
                                  <config-format-text-cmd>
                                     <text-filter-spec> | include hostname</text-filter-spec>
                                  </config-format-text-cmd>
                                  <oper-data-format-text-block>
                                     <exec>show spanning-tree vlan %s</exec>
                                  </oper-data-format-text-block>
                               </filter>
                             '''

def getNode(device,vlan):
    try:
        with connection(device["address"],device["netconf_port"],device["username"],device["password"]) as devicem:
            reply=devicem.get(hostname)
            if(devicem.ok):
                try:
                    print("Connected at: "+str(datetime.datetime.now().strftime("%I:%M:%S %p")))
                    xml_doc = xml.dom.minidom.parseString(reply.xml)
                    hostname_response = xml_doc.getElementsByTagName("cmd")
                    myhostname = hostname_response[0].firstChild.nodeValue
                    hn = myhostname.split()[1]
                    print(hn[2])
                    nodes.append(int(hn[2]))
                    return hn[2]
                except(ncclient.operations.errors.TimeoutExpiredError):
                    print("Connection timed out!")
    except (ncclient.operations.errors.TimeoutExpiredError,
            ncclient.transport.errors.SSHError):
        print("Connection timed out or could not be established!")


def getEdge(device,vlan):
    try:
        with connection(device["address"],device["netconf_port"],device["username"],device["password"]) as devicem:
            reply=devicem.get(cdp)
            if(devicem.ok):
                print("Connected to "+device['name']+" at: "+str(datetime.datetime.now().strftime("%I:%M:%S %p")))
                xml_doc = xml.dom.minidom.parseString(reply.xml)
                cdp_response = xml_doc.getElementsByTagName("response")
                mycdp = cdp_response[0].firstChild.nodeValue
                split_mycdp = mycdp.split('\n')
                for i in range(0,5):
                    split_mycdp.pop(0)
                split_mycdp.pop(len(split_mycdp)-1)
                # print(split_mycdp)
                neighbors = []
                port1s = []
                port2s = []
                for n in split_mycdp:
                    a = n.split()
                    neighbors.append(int(a[0][2]))
                    port1s.append(a[1]+a[2])
                    port2s.append(a[7]+a[8])
                #print(neighbors)

                for t in range (0,len(neighbors)):
                    tupple = ((int(device['name'][2]),neighbors[t],{'weight': 0,'port1':device['name'][2]+" "+port1s[t],'port2':str(neighbors[t])+" "+port2s[t]}))
                    edges.append(tupple)

                # for t in neighbors:
                    # tupple = ((int(device['name'][2])),t,0)
                    # edges.append(tupple)

                """print("CDP neighbours for "+str(device['name']))
                print(mycdp)"""
                #print(edges)
    except (ncclient.operations.errors.TimeoutExpiredError,
            ncclient.transport.errors.SSHError):
        print("Connection timed out or could not be established!")


def getEdgeSwitches(device,vlan):
    try:
        print(returnable_edge_list)
        edge_filter = edge % (str(vlan))
        print("VLAN: "+str(vlan))
        with connection(device["address"],device["netconf_port"],device["username"],device["password"]) as devicem:
            reply=devicem.get(edge_filter)
            if(devicem.ok):
                print("Connected to "+device['name']+" at: "+str(datetime.datetime.now().strftime("%I:%M:%S %p")))
                xml_doc = xml.dom.minidom.parseString(reply.xml)
                edge_response = xml_doc.getElementsByTagName("response")
                hostname_response = xml_doc.getElementsByTagName("cmd")
                

                myedge = edge_response[0].firstChild.nodeValue
                myname = hostname_response[0].firstChild.nodeValue


                if "P2p Edge" in myedge:
                    print(myname.split()[1] + " is access switch!")
                    hn = myname.split()[1]
                    num = int(hn[2])
                    returnable_edge_list.append(num)

    except (ncclient.operations.errors.TimeoutExpiredError,
            ncclient.transport.errors.SSHError):
        print("Connection timed out or could not be established!")

def Threaded(function,vlan):
    
    threads = len(di.getDevices())

    jobs = []
    for i in range(0,threads):
        thread = threading.Thread(target=function, args=(di.getDevices()[i],vlan))
        jobs.append(thread)
        thread.start()

    for k in jobs:
        k.join()

def getNodesList():
    nodes.clear()
    Threaded(getNode,1)
    return nodes

def getEdgesList():
    edges.clear()
    Threaded(getEdge,1)
    return edges

def getAccessSwitchList(vlan):
    returnable_edge_list.clear()
    Threaded(getEdgeSwitches,vlan)
    return returnable_edge_list

if __name__ == '__main__':
    
    #Threaded(getNode)
    # Threaded(getEdgeSwitches)
    # print(getAccessSwitchList())
    #Threaded(getEdge)
    #print(getEdgesList())
    print(getNodesList())
    #print(getAccessSwitchList(100))
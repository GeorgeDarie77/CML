# Working with several devices requires to save the running configuration in startup configuratation
# This script will do the job for you! You just need to provide the name of the lab or the id
#
# The script will requier some parameters:

# --cmlUrl   -IP address of the CML Server
# --cmlUsername  -Your user name
# --cmlPassword  -Your password
# --labName      -Lab name to update
#  or
# --labID        -ID of lab to be updated
# Run the script with arguments like:
# --cmlUrl 192.168.178.99 --cmlUsername user --cmlPassword password --labID  yourlabID --labName yourlabName

# Only one parameter is required to identify the topology: --labID or --labName
# If both provided and both are representing 2 different labs only the lab identified based on id will be updated
# If id is missing the script will try to update the lab identified by name
# The configuration (YAML) file will be extracted and saved on disk

#The name or the id can be easily found in the CML Workbench
#In the address bar of the explorer the id is after the IP address/lab
# e.g. https://192.168.178.99/lab/86542ba3-125e-49de-b01e-05dee3e2e2cc
# The id is 86542ba3-125e-49de-b01e-05dee3e2e2cc
# The name is the name of your topology

import argparse
from virl2_client import ClientLibrary
from pathlib import Path
import time

devices = ["iosv", "iol-xe", "iol-xe-serial-4eth", "iosxrv9000", "frr", "iosvl2", "ioll2-xe", "cat9000v-q200", "cat9000v-uadp", "nxosv9000", "unmanaged_switch"]

def getClient(url, username, password):
    try:
        client : ClientLibrary = ClientLibrary(url, username, password, ssl_verify=False)
        return client
    except Exception as e:
        print("An error occurred, please check the URL and authentication data: ", e)
        return None

def getLab_per_name(client, labName):
    labToFind = None
    allLabs = client.all_labs()
    for lab in allLabs:
        if lab.title == labName:
            labToFind = lab
            break
    return labToFind

def getLab_per_id(client, labID):
    labToFind = None
    allLabs = client.all_labs()
    for lab in allLabs:
        if lab.id == labID:
            labToFind = lab
            break
    return labToFind

def printLabsName(client):
    allLabs = client.all_labs()
    print("Available labs...")
    for lab in allLabs:
        print(lab.title)
    return

def fetch(client, labname = None, labid = None, yamlpath = None):
    print(f'Lab name << {labname} >>, Lab ID << {labid} >>')
    lab_per_name = None
    lab_per_id = None
    # Find the lab with the name provided as argument if not empty
    if labname is not None: lab_per_name = getLab_per_name(client, labname)
    # Find the lab with the id specified as argument if not empty
    if labid is not None: lab_per_id = getLab_per_id(client, labid)

    if labid is not None:
        if lab_per_id is not None:
            print(f'Lab with the id {labid} founded! The name of the lab << {lab_per_id.title} >>! Processing...')
            if labname is not None and lab_per_name is not None:
                if lab_per_name.id == labid:
                    print(f'Looks like the id {labid} and name {labname} are referring to the same lab! The processing will be based on the id!')
                else:
                    print(f'Looks like the id {labid} and name {labname} are referring to different labs! The processing per id will have precedence and the processing per name will be ignored!')

            extract_and_save_yaml(lab_per_id,yamlpath)
        else:
            if labname is not None:
                print(f'Fallback to the lab name {labname}')
                if lab_per_name is not None:
                    print(f' Lab with the id {labid} NOT founded but the lab with the name {labname} founded! Processing...')
                    extract_and_save_yaml(lab_per_name,yamlpath)
                else:
                    print(f'Could not find a lab with the id {labid} nor with the name {labname}. Aborting!!!')
            else:
                print(f'Could not find the lab with the id {labid} and no fallback (lab name) was not provided. Aborting!!!')
    else:
        if lab_per_name is not None:
            print(f'Lab with the name {labname} founded! Processing...')
            extract_and_save_yaml(lab_per_name,yamlpath)
        else:
            print(f'Could not find a lab with the name {labname}! Aborting!!!')
    return

def extract_and_save_yaml(lab,yamlpath):
    if lab.is_active():
        allNodesList = lab.nodes()
        nodeCount = len(allNodesList)
        print(f"[+] Successfully joined lab: {lab.title} | id = {lab.id}")
        print(f"[+] Total number of nodes in this lab: {nodeCount}")

        for node in allNodesList:
            node_def = node.node_definition.lower()

            if any(x in node_def for x in devices):
                if node.is_active():
                    print(f"[*] Processing {node.label} ({node.node_definition})...")
                    try:
                        print(f"   -> Extract Configuration...")
                        node.extract_configuration()
                    except Exception as e:
                        print(f"   [!] Error at node {node.label}: {e}")
                else:
                    print(f"[*] Node {node.label} is not active ...")
        print("[*] Global sync running...")
        time.sleep(3)

        print("[*] Generate and download YML...")
        yaml_data = lab.download()
        filename = f"{lab.title}.yaml"
        if yamlpath is None:
            filepath = filename
        else:
            filepath = Path(yamlpath)/filename
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(yaml_data)
        print(f"[+] Success! File saved as: {filename} at {yamlpath}")
    else:
        print(f'Lab >>{lab.title} | {lab.id} << is not active! Nothing to do! Aborting!!!')
    return

parser = argparse.ArgumentParser(description="Command line parser")
parser.add_argument("--cmlUrl", required=True, help="CML_URL")
parser.add_argument("--cmlUsername", required=True, help="User name")
parser.add_argument("--cmlPassword", required=True, help="Password")
parser.add_argument("--labName", required=False, help="Lab name to update...")
parser.add_argument("--labID", required=False, help="ID of lab to be updated...")
parser.add_argument("--yamlPath", required=False, help="Where to save the yaml file..")
args = parser.parse_args()

if not args.labName and not args.labID:
        parser.error("You must specify at least one of the following arguments: --labName or --labID. If both are provided the --labID has precedence")

cml_url = args.cmlUrl
cml_username = args.cmlUsername
cml_password = args.cmlPassword
lab_name = args.labName
lab_id = args.labID
yaml_path = args.yamlPath

## Connect to CML Server.
client = getClient(cml_url, cml_username, cml_password)

if client is not None:
   #printLabsName(client)
   if (lab_name is not None) and (lab_id is not None): fetch(client, lab_name, lab_id,yamlpath=yaml_path)
   if (lab_name is None) and (lab_id is not None):     fetch(client, labid=lab_id, yamlpath=yaml_path)
   if (lab_name is not None) and (lab_id is None):     fetch(client, labname=lab_name, yamlpath=yaml_path)
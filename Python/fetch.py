# This script will connect to the CML
# Will fetch the configuration of each node for a specific topology

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
from virl2_client import ClientLibrary

def getClient(url, username, password):
    try:
        client = ClientLibrary(url, username, password, ssl_verify=False)
        return client
    except Exception as e:
        print("An error occured, please check the URL and authetication data: ", e)
        return None


parser = argparse.ArgumentParser(description="Command line parser")

parser.add_argument("--cmlUrl", required=True, help="CML_URL")
parser.add_argument("--cmlUsername", required=True, help="User name")
parser.add_argument("--cmlPassword", required=True, help="Password")
parser.add_argument("--labName", required=True, help="Lab name to update...")
args = parser.parse_args()
LAB_NAME = args.labName
CML_URL = args.cmlUrl
CML_USERNAME = args.cmlUsername
CML_PASSWORD = args.cmlPassword
print(f'CML_URL: {CML_URL}, CML_USERNAME: {CML_USERNAME}, CML_PASSWORD: {CML_PASSWORD}, LAB_NAME: {LAB_NAME}')

## Connect to CML Server.
client = getClient(CML_URL, CML_USERNAME, CML_PASSWORD)

if client is not None:
    print('Get the labs...')
    allLabs = client.all_labs()
    print("Available labs...")
    for lab in allLabs:
        print(lab.title)

    labToUpdate = None

    # Iterate through all labs to find the one matching the name
    for lab in allLabs:
        if lab.title == LAB_NAME:
            labToUpdate = lab
            print(f"The lab name: {labToUpdate.title} founded and has the ID: {labToUpdate.id}")
            break
    if labToUpdate is not None:
        if labToUpdate.is_active():
            allNodesList = labToUpdate.nodes()
            nodeCount = len(allNodesList)
            print(f"[+] Successfully joined lab: {labToUpdate.title} ({labToUpdate.id})")
            print(f"[+] Total number of nodes in this lab: {nodeCount}")
        else:
            print(f'Lab >>{LAB_NAME}<< is not active, skipping')

    else:
        print('No lab founded...')
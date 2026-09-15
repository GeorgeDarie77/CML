# This script will connect to the CML
# Will fetch the configuration of each node for a specific topology

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from virl2_client import ClientLibrary

CML_URL = "192.168.30.128"
CML_USERNAME = "george"
CML_PASSWORD = "Geo1977mai19"

def getClient(url,username,password):
    try:
        client = ClientLibrary(url, username, password,ssl_verify=False)
        return client
    except Exception as e:
        print("An error occured, please check the URL and authetication data: ", e)
        return None





def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
client = getClient(CML_URL, CML_USERNAME, CML_PASSWORD)

if client is not None:
    print_hi('PyCharm...like a charm')


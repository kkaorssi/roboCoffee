import time
import requests

def get_api(url, model, idx):
    while True:
        endpoint = f'{url}{model}/{str(idx)}/'
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            print("read data:\n", data)
            return data
    
        elif response.status_code == 404:
            print("order has not been received")
        
        else:
            print("Failed to read data")
        
        time.sleep(1)
    
def update_api(url, idx):
    endpoint = f'{url}/order/{str(idx)}'
    data_to_update = {
    'state': 'done'
    }
    response = requests.patch(endpoint, json=data_to_update)
    
    if response.status_code == 200:
        print("Updated successfully")
    else:
        print("Update failed")
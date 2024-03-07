import requests

def check_order(url, order_num):
    endpoint = f'http://{url}recipe/{str(order_num)}/'
    try:
        print('get grom :', endpoint)
        response = requests.get(endpoint)
    
        if response.status_code == 200: # new order exists
            recipe = response.json()
            print(recipe)
            
            return recipe
        
    except:
        print('server connection error')

    return None
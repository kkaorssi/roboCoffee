import requests

def check_order(url, order_num):
    endpoint = f'http://{url}order/{str(order_num)}/'
    try:
        print('get grom :', endpoint)
        response = requests.get(endpoint)
    
        if response.status_code == 200: # new order exists
            order = response.json()
            print(order)
            
            state = order['state']
            if state == 'new':
                order_id = order['id']
                recipe_id = order['recipe']
                drip_num = order['drip_pos'] # 1 = pos 2, 2 = pos 1, 3 = pos 0
                if drip_num == 1: drip_pos = 2
                elif drip_num == 2: drip_pos = 1
                elif drip_num == 3: drip_pos = 0
                
                endpoint = f'http://{url}recipe/{str(recipe_id)}/'
                print('get grom :', endpoint)
                response = requests.get(endpoint)
                recipe = response.json()
                print(recipe)
                
                ground_amount = recipe['ground_amount']
                brewing_ratio = recipe['brewing_ratio']
                total_amount = recipe['total_amount']
            
                return {'id': order_id, 'pos': drip_pos, 'recipe': [ground_amount, brewing_ratio, total_amount]}
        
    except:
        print('server connection error')

    return None

def update_order_state(url, id):
    endpoint = f'http://{url}order/{str(id)}/'
    data_to_update = {
    'state': 'done'
    }
    print('update: ', endpoint, data_to_update)
    response = requests.patch(endpoint, json=data_to_update)
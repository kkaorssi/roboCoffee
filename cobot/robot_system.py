import threading
import queue
import time
import pandas as pd

from cobot.coffee_robot import robotController
from cobot.robot_client import check_order

# program list
# mode 3 drip
DRIP_2EA = 'DRIP2EA'

# mode parameter
DRIP_200_S = 'DRIP200S'
DRIP_200_C = 'DRIP200C'
DRIP_250_S = 'DRIP200S'
DRIP_250_C = 'DRIP200C'
DRIP_300_S = 'DRIP200S'
DRIP_300_C = 'DRIP200C'

def match_program(recipe):
    mode = recipe['mode']
    
    if mode == 'Parameter':
        pattern = recipe['pattern']
        if pattern == 'Spiral':
            pattern_initial = 'S'
        elif pattern == 'Circle':
            pattern_initial = 'C'
        drip = recipe['drip']
        program_name = f'DRIP{str(drip)}{pattern_initial}'
        
    elif mode == '3Drip':
        program_name = 'DRIP2EA'
            
    return program_name

def robot_manager(server_config, robot_config,):
    server_ip = server_config['ip']
    server_port = server_config['port']
    app = server_config['app']
    
    url = f'{server_ip}:{str(server_port)}/{app}/'
    
    rc = robotController(robot_config)
    
    order_num = 1
    while True:
        # check order and done if exists
        recipe = check_order(url, order_num)
        if recipe:
            print('recipe: ', recipe)
            program = match_program(recipe)
            rc.run_program(program)
            order_num += 1
              
        time.sleep(1)
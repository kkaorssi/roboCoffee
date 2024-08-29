import threading
import queue
import time
import pandas as pd

from cobot.cam import azure_kinect
from cobot.coffee_robot import robotController
from cobot.robot_client import check_order, update_order_state
from cobot.vision import Visualization

# dripper state
INIT = 0
READY = 1
RINSED = 2
GROUND = 3
DONE = 4

# command
PICK_UP = 'KETTLEPICK'
RINSE = 'RINSING'
DISCARD = 'WATERING'
BLOOM = 'BLOOMING'
DRIP_COFFEE = 'DRIP'

class checker:
    def __init__(self) -> None:
        self.ak = azure_kinect()
        self.vs = Visualization()
        
    def check_dripper(self):
        while True:
            img = self.ak.capture_img()
            result = self.vs.run_on_image(img)
            if len(result) == 3: break
            
        # Process results list
        names = result.names # A dictionary of class names. 
        boxes = result.boxes.data # A Boxes object containing the detection bounding boxes.
        res_img = result.plot() # Plots the detection results. Returns a numpy array of the annotated image.
        
        drippers_df = pd.DataFrame(columns=['state', 'x1', 'y1', 'x2', 'y2'])

        for n in range(len(boxes)):
            if names[int(boxes[n][5])] == 'init':
                name = INIT
            elif names[int(boxes[n][5])] == 'ready':
                name = READY
            elif names[int(boxes[n][5])] == 'ground':
                name = GROUND
            values = boxes[n][0:4]
            
            new_row = pd.DataFrame({'state': [name], 'x1': [float(values[0])], 'y1': [float(values[1])], 'x2': [float(values[2])], 'y2': [float(values[3])]})
            drippers_df = pd.concat([drippers_df, new_row], ignore_index=True)
    
        check_res = drippers_df.sort_values('y1', ascending=False)['state'].to_list()
        print(check_res)
        
        return check_res
    
def match_program(command, *args, **kwargs):
    if command in [PICK_UP, DISCARD]:
        program = command
    elif command == RINSE:
        pos = args[0]
        cnt = kwargs['cnt']
        program_name = f'{str(pos+1)}{command}{str(cnt+1)}'
    elif command == BLOOM:
        ground_amount = args[0] * args[1]
        program_name = f'{command}{str(ground_amount)}'
    elif command == DRIP_COFFEE:
        pos = args[0]
        if pos != 0:
            program_name = f'{str(pos+1)}{command}'
        else:
            amount = kwargs['ground_amount']
            ratio = kwargs['brewing_ratio']
            bloom_amount = amount * ratio
            total_amount = kwargs['total_amount']
            program_name = f'{str(pos+1)}{command}{str(bloom_amount)}{str(total_amount)}'
            
    return program_name

def robot_manager(server_config, robot_config,):
    server_ip = server_config['ip']
    server_port = server_config['port']
    app = server_config['app']
    
    url = f'{server_ip}:{str(server_port)}/{app}/'
    
    dripper_state = [INIT, INIT, INIT]
    
    rc = robotController(robot_config)
    ch = checker()
    
    order_num = 1
    while True:
        print('current state: ', dripper_state)
        
        # check all state of drippers
        if INIT in dripper_state or RINSED in dripper_state or DONE in dripper_state:
            check_res = ch.check_dripper()
            for pos, cur in enumerate(dripper_state):
                if not (cur in [INIT, RINSED, DONE]): continue
                else:
                    if check_res[pos] == INIT and cur == DONE:
                        print(pos, ' is ', check_res[pos])
                        dripper_state[pos] = check_res[pos]
                    elif check_res[pos] == cur + 1:
                        print(pos, ' is ', check_res[pos])
                        dripper_state[pos] = check_res[pos]
                    else: print(pos, 'detection error')
        
        # check order and done if exists
        if GROUND in dripper_state:
            order = check_order(url, order_num)
            if order:
                print('order: ', order)
                if dripper_state[order['pos']] == GROUND:
                    print('dripping start')
                    rc.run_program(PICK_UP)
                    order_id = order['id']
                    [ground_amount, brewing_ratio, total_amount] = order['recipe']
                    if order['pos'] == 0:
                        program = match_program(BLOOM, ground_amount, brewing_ratio)
                        rc.run_program(program)
                        time.sleep(9)
                    program = match_program(DRIP_COFFEE, order['pos'], 
                                            ground_amount=ground_amount,
                                            brewing_ratio=brewing_ratio,
                                            total_amount=total_amount)
                    rc.run_program(program)
                    rc.run_program(DISCARD)
                    dripper_state[order['pos']] = DONE
                    update_order_state(url, order_id)
                    order_num += 1
                else:
                    print('dripper is not ready')
                
        # check state of dripper and do rinsing
        if READY in dripper_state:
            cnt = 0
            rc.run_program(PICK_UP)
            for pos, state in enumerate(dripper_state):
                if state != READY: continue
                else:
                    print('rinsing start')
                    program = match_program(RINSE, pos, cnt=cnt)
                    rc.run_program(program)
                    dripper_state[pos] = RINSED
                    cnt += 1
            rc.run_program(DISCARD)
              
        time.sleep(1)
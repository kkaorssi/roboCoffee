import time

import frrpc

# Create your models here.
class RobotController:
    def __init__(self, config):
        self.config = config
        ip = self.config['ip']
        
        try:
            print(f'trying to connect robot {ip}')
            self.robot = frrpc.RPC(ip)
            self.robot.Mode(0)
            self.robot_connection = True
            
        except Exception as e:
            print('connection failed')

    def run_program(self, command, *args, **kwargs):
        if args:
            if args[0] == 1: drip_pos = 3
            elif args[0] == 2: drip_pos = 2
            elif args[0] == 3: drip_pos = 1

        program_list = self.config['program']
        if command == 'pick_up':
            program = program_list[command]
            
        elif command == 'rincing':
            program_name = str(drip_pos) + program_list[command] + str(kwargs['idx'])
            program = program_name
            
        elif command == 'discard_water':
            program = program_list[command]
            
        elif command == 'blooming':
            if drip_pos == 1:
                amount = int(kwargs['ground_amount']) * int(kwargs['brewing_ratio'])
                program_name = str(drip_pos) + program_list[command] + str(amount)
            else: 
                return
            program = program_name
            
        elif command == 'drip':
            if drip_pos == 1:
                amount = int(kwargs['ground_amount']) * int(kwargs['brewing_ratio'])
                program_name = str(drip_pos) + program_list[command] + str(amount) + str(kwargs['total_amount'])
            else: 
                program_name = str(drip_pos) + program_list[command]
            program = program_name
        
        base_dir = 'fruser'
        program_path = f'/{base_dir}/{program}.lua'
        self.robot.ProgramLoad(program_path)
        self.robot.ProgramRun()
        
    def get_program_state(self):
        pstate = self.robot.GetProgramState()
        return pstate

import threading
import queue

from cobot.client import get_api, update_api

def place_order(url, q):
    idx = 1
    while True:
        order = get_api(url, 'order', idx)
        if order['state'] == 'new':
            recipe = get_api(url, 'recipe', order['recipe'])
            q.put([order['drip_pos'], recipe], idx)
        elif order['state'] == 'cancelled': pass
        idx += 1
        time.sleep(1)
        
def robot_process(url, config, q, conn):
    rc = RobotController(config)
    
    import pandas as pd

    sample_data = {'Name': [0, 2, 1],
            'x1': [218.740784, 198.446686, 208.476044],
            'y1': [196.023697, 297.161072, 241.412506],
            'x2': [260.631500, 251.297791, 256.675323],
            'y2': [250.527023, 372.368347, 305.720428]}

    sample = pd.DataFrame(sample_data)
    
    state_list = ['init', 'ready', 'rincing', 'ground', 'done']
    pos_state = ['init', 'init', 'init']
    
    robot_status = 'ready' # ready/busy
    
    while True:
        order = q.get()
        if order:
            if pos_state[order[0]-1] == 'ground':
                rc.run_program('blooming', order[0], ground_amount = order[1]['ground_amount'], brewing_ratio = order[1]['brewing_ratio'])
                time.sleep(1)
                while rc.get_program_state(2): pass
                rc.run_program('drip', order[0], ground_amount = order[1]['ground_amount'], brewing_ratio = order[1]['brewing_ratio'], total_amount = order[1]['total_amount'])
                time.sleep(1)
                while rc.get_program_state(2): pass
                update_api(url, order[2])
                pos_state[order[0]-1] == 'done'
                q.task_done()
                
        elif 'ready' in pos_state:
            cnt = 1
            rc.run_program('pick_up')
            time.sleep(1)
            while rc.get_program_state(2): pass
            if pos_state[2] == 'ready':
                rc.run_program('rincing', 3, idx=cnt)
                time.sleep(1)
                while rc.get_program_state(2): pass
                pos_state[2] == 'rincing'
                cnt += 1
            
            if pos_state[1] == 'ready':
                rc.run_program('rincing', 2, idx=cnt)
                time.sleep(1)
                while rc.get_program_state(2): pass
                pos_state[1] == 'rincing'
                cnt += 1
            
            if pos_state[0] == 'ready':
                rc.run_program('rincing', 1, idx=cnt)
                time.sleep(1)
                while rc.get_program_state(2): pass
                pos_state[0] == 'rincing'
                cnt += 1
                
            rc.run_program('discard_water')
            time.sleep(1)
            while rc.get_program_state(2): pass
            
        elif 'init' in pos_state or 'rincing' in pos_state or 'done' in pos_state:
            conn.send('trigger')
            res_df = conn.recv()
            
            for state, x1, y1, x2, y2 in res_df:
                for d_pos, d_x1, d_y1, d_x2, d_y2 in sample:
                    if d_y1 < (y1 + y2)/2 <d_y2:
                        if state_list.index(pos_state[d_pos])+1 == state_list.index(state):
                            pos_state[d_pos] = state
                            break
                  
def process_queue(config, conn):
    server_config = config.get('server', {})
    server_ip = server_config['ip']
    server_port = server_config['port']
    app = server_config['app']
    url = f'{server_ip}:{str(server_port)}/{app}/'
    
    robot_config = config.get('robot', {})
    
    order_queue = queue.Queue()
    
    ordering_thread = threading.Thread(target=place_order, args=(url, order_queue,))
    processing_thread = threading.Thread(target=robot_process, args=(url, robot_config, order_queue, conn))
    
    ordering_thread.start()
    processing_thread.start()
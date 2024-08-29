import subprocess
from multiprocessing import Pipe, Process
import yaml
import os

from cobot.robot_system import robot_manager

def get_default_config():
    config_file = 'config.yaml'
    with open(config_file) as f:
        config = yaml.safe_load(f)

    return config

def run_server(config):
    ip = config['ip']
    port = config['port']
    input_arg = "runserver " + ip + ':' + str(port)
    subprocess.call(["python", "manage.py"] + input_arg.split())
    
if __name__ == '__main__':
    config = get_default_config()
    server_config = config.get('server', {})
    robot_config = config.get('robot', {})
    
    # SQLite3 데이터베이스 파일 경로
    db_file_path = 'db.sqlite3'

    # 파일이 존재하는지 확인하고 삭제
    if os.path.exists(db_file_path):
        os.remove(db_file_path)
        print(f"Database file at {db_file_path} has been successfully deleted.")
    else:
        print(f"No database file found at {db_file_path}.")
    
    # 실행할 명령어
    cmd = 'python manage.py migrate'

    # shell에서 명령어 실행하고 완료될 때까지 기다림
    process = subprocess.Popen(cmd, shell=True)
    process.wait()  # 명령어가 완료될 때까지 기다림

    # 명령어 실행이 완료되면 여기로 이동
    print("Command execution completed.")
    
    p1 = Process(target=run_server, args=(server_config,))
    p2 = Process(target=robot_manager, args=(server_config, robot_config,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
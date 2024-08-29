import threading
import queue
import time

# 스레드에서 실행될 함수
def worker(thread_id, work_queue):
    while True:
        item = work_queue.get()
        if item is None:
            break

        # 작업 처리
        print(f"Thread {thread_id} is processing: {item}")
        time.sleep(1)  # 작업 시뮬레이션

        work_queue.task_done()

# 작업 큐 생성
work_queue = queue.Queue()

# 스레드 개수
num_threads = 3
threads = []

# 스레드 생성 및 실행
for i in range(num_threads):
    thread = threading.Thread(target=worker, args=(i, work_queue))
    thread.start()
    threads.append(thread)

# 작업 아이템 추가
for item in range(10):
    work_queue.put(item)

# 모든 스레드가 작업을 완료할 때까지 대기
work_queue.join()

# 종료 신호 전달
for _ in range(num_threads):
    work_queue.put(None)

# 모든 스레드가 종료될 때까지 대기
for thread in threads:
    thread.join()

print("All threads have finished.")

################################## lock
import threading

# Lock 객체 생성
data_lock = threading.Lock()

shared_data = []

def add_data(value):
    with data_lock:
        shared_data.append(value)

def get_data():
    with data_lock:
        return shared_data

# 스레드 생성 및 실행
thread1 = threading.Thread(target=add_data, args=("Data 1",))
thread2 = threading.Thread(target=add_data, args=("Data 2",))
thread1.start()
thread2.start()
thread1.join()
thread2.join()

result = get_data()
print(result)


################################ event
import threading

event = threading.Event()

def producer():
    print("Producer is producing data...")
    event.set()  # 이벤트를 설정하여 소비자 스레드에 신호를 보냄

def consumer():
    event.wait()  # 이벤트를 기다림
    print("Consumer received the signal and is processing data")

# 스레드 생성 및 실행
producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)
producer_thread.start()
consumer_thread.start()
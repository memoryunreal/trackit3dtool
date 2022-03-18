import multiprocessing
import time

def sub_process(process_name, share_var, share_lock):
    share_lock.acquire()

def func(num):
    while True:
        print("subprocess num.value: ", num.value)
        time.sleep(2)

def main_process():
    share_var = multiprocessing.Manager().list()
    share_lock = multiprocessing.Manager().Lock()
    tmp_process = multiprocessing.Process(target=sub_process, args=())
    num = multiprocessing.Value('f', 0.0)
    p = multiprocessing.Process(target=func, args=(num,))
    p.start()
    while True:
        num.value+=1
        time.sleep(2)
        print("main process num.value: ", num.value)
    # p.join()
    # print(num.value)

if __name__ == "__main__":
    main_process()
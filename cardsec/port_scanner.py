import os
import signal
import time
import socket
import threading
import sys
import subprocess
from queue import Queue
from datetime import datetime

# Start Threader3000 with clear terminal
subprocess.call('clear', shell=True)

# Main Function
def scan_ports():
    socket.setdefaulttimeout(0.30)
    print_lock = threading.Lock()
    discovered_ports = []


    time.sleep(1)
    target = socket.gethostname()
    t_ip = socket.gethostbyname(target)
    print ('Starting scan on host: ', t_ip)
    print("-" * 60)
    print("Time started: "+ str(datetime.now()))
    print("-" * 60)
    t1 = datetime.now()

    def portscan(port):

       s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
       try:
          conx = s.connect((t_ip, port))
          with print_lock:
             print("Port {} is open".format(port))
             discovered_ports.append(str(port))
          conx.close()

       except (ConnectionRefusedError, AttributeError, OSError):
          pass

    def threader():
       while True:
          worker = q.get()
          portscan(worker)
          q.task_done()
      
    q = Queue()
     
    #startTime = time.time()
     
    for x in range(200):
       t = threading.Thread(target = threader)
       t.daemon = True
       t.start()

    for worker in range(1, 65536):
       q.put(worker)

    q.join()

    t2 = datetime.now()
    total = t2 - t1
    if discovered_ports:
      print("Port scan completed in "+str(total))
      print("\nHappy Secure Minting!")
    else:
      print("No ports were open!")
      print("\nHappy Secure Minting!")

if __name__ == '__main__':
    try:
        scan_ports()
    except KeyboardInterrupt:
        print("\nHappy Secure Minting!")
        quit()

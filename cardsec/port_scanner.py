import socket
import time
import threading

from queue import Queue
socket.setdefaulttimeout(0.25)
print_lock = threading.Lock()

target = socket.gethostname()
t_IP = socket.gethostbyname(target)
#print ('Starting scan on host: ', t_IP)

port_list=set()
q = Queue()

def portscan(port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      con = s.connect((t_IP, port))
      with print_lock:
          port_list.add(port)
      con.close()
   except:
      pass

def threader():
   while True:
      worker = q.get()
      port_list.add(portscan(worker))
      q.task_done()

def scan_ports(port_range):
   for x in range(100):
            t = threading.Thread(target = threader)
            t.daemon = True
            t.start()

   for worker in range(1, port_range):
            q.put(worker)

   q.join()
   port_list.discard(None)
   if port_list:
      return port_list
   else: return False

#print(scan_ports())

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

#VULNERABILITY DETECTION  
   #  print("Scan these ports for vulnerability detection:")
   #  print("*" * 60)
   #  print("nmap -p{ports} -sV -sC -T4 -Pn -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target))
   #  print("*" * 60)
   #  outfile = "nmap -p{ports} -sV -sC -Pn -T4 -oA {ip} {ip}".format(ports=",".join(discovered_ports), ip=target)
   #  t3 = datetime.now()
   #  total1 = t3 - t1

#Nmap

   #  def automate():
   #     choice = '0'
   #     while choice =='0':
   #        print("Would you like to run a vulnerability scan or quit?")
   #        print("-" * 60)
   #        print("1 = Run suggested Nmap scan")
   #        print("2 = Exit to terminal")
   #        print("-" * 60)
   #        choice = input("Option Selection: ")
         #  if choice == "1":
         #     try:
         #        print(outfile)
         #        os.mkdir(target)
         #        os.chdir(target)
         #        os.system(outfile)
         #        convert = "xsltproc "+target+".xml -o "+target+".html"
         #        os.system(convert)
         #        t3 = datetime.now()
         #        total1 = t3 - t1
         #        print("-" * 60)
         #        print("Combined scan completed in "+str(total1))
         #        print("Press enter to quit...")
         #        input()
         #     except FileExistsError as e:
         #        print(e)
         #        exit()
   #        if choice =="2":
   #           print("\nHappy Secure Minting!")
   #           sys.exit()
   #        else:
   #           print("Please make a valid selection")
   #           automate()
   #  automate()

if __name__ == '__main__':
    try:
        scan_ports()
    except KeyboardInterrupt:
        print("\nHappy Secure Minting!")
        quit()

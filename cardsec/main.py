import psutil
import subprocess
import distro
from typing import Optional
from typing import Optional
from termcolor import colored
from cardsec.port_scanner import scan_ports


def banner():
 print("                                                                      ")
 print("                                                                      ")
 print(colored("          █████╗  █████╗ ██████╗ ██████╗  ██████╗███████╗ █████╗         ", "white"))
 print(colored("         ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════ ██╔════╝██╔══██╗        ", "white"))
 print(colored("         ██║  ╚═╝███████║██████╔╝██║  ██║╚█████╗ █████╗  ██║  ╚═╝        ", "white"))
 print(colored("         ██║  ██╗██╔══██║██╔══██╗██║  ██║ ╚═══██╗██╔══╝  ██║  ██╗        ", "white"))
 print(colored("         ╚█████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗╚█████╔╝        ", "white"))
 print(colored("          ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝ ╚════╝        ", "white"))
 print("                                                                      ")
 print(colored("                        Developed by: SkryptLabs                              ", "blue"))
 print(colored("                         twitter.com/skryptlabs             				   ", "red"))
 print("                                                                         ")

banner()

def info():
			try:
				node=subprocess.check_output(['cardano-node','version']).decode().split()[1]
			except: node="Not found."

			print(colored("-------System Info---------", "blue"))

			print("Distro: "+distro.id()+' '+distro.version())
			print("RAM Size: " +str(psutil.virtual_memory()[0]/1024/1024//1024)+' GB')
			print("Disk Size: " +str(psutil.disk_usage('/')[0]/1024/1024//1024)+'GB'+'\n')
			print(colored("Recommended RAM: 16GB", "cyan"))
			print(colored("Recommended Disk: 50GB", "cyan"))
			print("Cardano-Node: " + colored((node), "red"))

def load():
			#cpu_load=(psutil.getloadavg()[2]/psutil.cpu_count())*100
			cpu_load=psutil.cpu_percent()
			ram_load=psutil.virtual_memory()[2]
			disk_load=psutil.disk_usage('/')
			
			print(colored("-------System Load---------", "blue"))
			
			print("CPU usage: ",cpu_load)
			print("RAM usage: ",ram_load)
			print("Disk usage: ",disk_load[3])

def scan():
	print(colored("-------Port Scanner---------", "magenta"))
	def submenu():
					print("[1] Exhaustive Scan - 64000 ports")
					print("[2] Light Scan - 6000 ports")
					print("[3] Exit to Main Menu")
	submenu()
	suboption = int(input(colored("Select your option: ", "yellow")))

	while suboption != 0:
		if suboption == 1:
			port_range=65000
			print("Scanning", 65000, "ports...")

			port_list=scan_ports(port_range)
			if port_list:
				print(colored("The following ports were found open:", "magenta"))
				for i in port_list:
					print(i)
				print(colored("Note: Only keep 2 outgoing ports open. (SSH & Node port)", "red"))
				print("")
			else: print(colored("No ports open!", "red"))
		      
		elif suboption == 2:
				port_range=6000
				print("Scanning", 6000, "ports...")

				port_list=scan_ports(port_range)
				if port_list:
					print(colored("The following ports were found open:", "magenta"))
					for i in port_list:
						print(i)
					print(colored("Note: Only keep 2 outgoing ports open. (SSH & Node port)", "red"))
					print("")
				else: print(colored("No ports open!", "red"))
		elif suboption == 3:
			print("")
			banner()
			option
			break
	
		else:
			print("Invalid Option!")	
		
		submenu()
		suboption = int(input(colored("Select your option: ", "yellow")))	
		


def menu():
		print("[1] System Info")
		print("[2] System Load")
		print("[3] Port Scanner")
		print("[4] Vulnerability Scanner")
		print("[5] Exit Cardsec")

menu()
option = int(input(colored("Select your option: ", "yellow")))

while option != 0:
	if option == 1:
		print("")
		info()
		print("")	
	elif option == 2:
		print("")
		load()
		print("")
	elif option == 3:
		print("")
		scan()
		print("")
	elif option == 4:
		print("")
		print("Coming Soon....")
		print("")
	elif option == 5:
		print("Happy Minting!")
		exit()	
	else:
		print("Invalid option.")
	
	menu()
	option = int(input(colored("Select your option: ", "yellow")))

if __name__ == '__main__':
	banner()

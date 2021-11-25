import psutil
import socket
import os
import subprocess
import distro
import requests
from termcolor import colored
from cardsec.port_scanner import scan_ports
from simple_term_menu import TerminalMenu, main
from cardsec.utils import parser

GOOD=50
OK=75

try:
	LATEST = requests.get("https://pypi.org/pypi/cardsec/json").json()["info"]["version"]
	from importlib.metadata import version 
	VERSION = version('cardsec')
except: 
	VERSION = "Not found."


def num_colour(num:int):
    if num<=GOOD:
        end = colored(f"{num}%", "green")
    elif num<=OK:
        end = colored(f"{num}%", "yellow")
    else: end = colored(f"{num}%", "red")

    return end

def run_cmd(cmd):
	return subprocess.run(cmd, shell= True, text = True, stdout= subprocess.PIPE)

def banner():
	print("                                                                      ")
	print("                                                                      ")
	print(colored("          █████╗  █████╗ ██████╗ ██████╗  ██████╗███████╗ █████╗         ", "white"))
	print(colored("         ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════ ██╔════╝██╔══██╗        ", "white"))
	print(colored("         ██║  ╚═╝███████║██████╔╝██║  ██║╚█████╗ █████╗  ██║  ╚═╝        ", "white"))
	print(colored("         ██║  ██╗██╔══██║██╔══██╗██║  ██║ ╚═══██╗██╔══╝  ██║  ██╗        ", "white"))
	print(colored("         ╚█████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗╚█████╔╝        ", "white"))
	print(colored("          ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝ ╚════╝        ", "white"))
	if LATEST != VERSION:
		print(colored(f"                               version {VERSION}        ", "yellow"))
		print(colored(f"     		        New update {LATEST} available", "red"))
	else:
		print(colored(f"                               version {VERSION}        ", "green"))
	print("                                                                      ")
	print(colored("                        Developed by: SkryptLabs                              ", "blue"))
	print(colored("                         twitter.com/skryptlabs             				   ", "red"))
	print("                                                                         ")


def info():
	try:
		node=subprocess.check_output(['cardano-node','version']).decode().split()[1]
	except: node="Not found."

	print(colored("\n-------System Info---------", "magenta"))

	print("Distro: "+distro.id()+' '+distro.version())
	print("RAM Size: " +str(psutil.virtual_memory()[0]/1024/1024//1024)+' GB')
	print("Disk Size: " +str(psutil.disk_usage('/')[0]/1024/1024//1024)+'GB'+'\n')
	print("Cardano-Node: " +node)
	latest=requests.get("https://api.github.com/repos/input-output-hk/cardano-node/releases/latest").json()["tag_name"]
	if latest == node:
		print(colored("Cardano-Node is up to date", "green"))
	else:
		print(colored(f"Cardano-Node {latest} update available ", "red"))
	print()


def load():
    #cpu_load=(psutil.getloadavg()[2]/psutil.cpu_count())*100
    cpu_load=psutil.cpu_percent()
    ram_load=psutil.virtual_memory()[2]
    disk_load=psutil.disk_usage('/')
    
    print(colored("\n-------System Load---------", "magenta"))
    
    print("CPU usage: ", num_colour(cpu_load))
    print("RAM usage: ", num_colour(ram_load))
    print("Disk usage: ", num_colour(disk_load[3])+'\n')

		
		
def nmapscan():
	print(colored("-------Vulnerability Scanner---------", "magenta"))
	print()
	
	target = socket.gethostname()
	t_IP = socket.gethostbyname(target)
	print(colored("Installing vulnerability scanning scripts....", "yellow"))
	run_cmd("sudo apt-get install nmap -y")
	if not os.path.exists("vulners.nse"):
		run_cmd("wget https://raw.githubusercontent.com/vulnersCom/nmap-vulners/master/vulners.nse > /dev/null 2>&1")
		run_cmd("sudo cp vulners.nse /usr/share/nmap/scripts/")
		print("Installed Succesfully")
	print(colored("Scanning in process, please have patience.", "yellow"))
	print()
	run_cmd("sudo nmap -Pn"+ " " + t_IP + " " + "-p 1-64000 --script=vulners.nse" + " " + "-sV -oX report.xml")
	f = open("report.xml", "r")
	output = parser(f)
	if output == None:
		print(colored("No Vulnerabilites Found", "green"))
	else:
		print(output)
	print()



def scanner(port_range):
	port_list=scan_ports(port_range)
	if port_list:
		print(colored("The following ports were found open:", "magenta"))
		for i in port_list:
			print(i)
		print(colored("Note: Only keep 2 outgoing ports open. (SSH & Node port)", "red"))
		print()
	else: print(colored("No ports open!", "red"))


def scan():

	def submenu():
		menu_options=["[1] Light Scan - 6000 ports", "[2] Exhaustive Scan - 64000 ports", "[3] Back"]
		terminal_menu = TerminalMenu(menu_options, title="Scan")
		return terminal_menu.show()

	while 1:
		print('')
		suboption = submenu()
		

		if suboption == 0:
			print(colored("-------Port Scanner---------", "magenta"))
			port_range=6000
			print(f"Scanning {port_range} ports...")
			scanner(port_range)			
		      
		elif suboption == 1:
			print(colored("-------Port Scanner---------", "magenta"))
			port_range=64000
			print(f"Scanning {port_range} ports...")
			scanner(port_range)

		elif suboption == 2:
			os.system("clear")
			banner()
			break		
		

def quit():
	os.system("clear")
	print("Happy Minting!")
	exit()


def menu():
	menu_options=["[1] System Info", "[2] System Load", "[3] Port Scanner", "[4] Vulnerability Scanner", "[5] Exit"]
	terminal_menu = TerminalMenu(menu_options, title="Home")
	return terminal_menu.show()


def select(option):

	menu_func = [info, load, scan, nmapscan, quit]

	print()
	return menu_func[option]()



def main():
	os.system("clear")
	banner()
	while 1:
		option = menu()
		os.system("clear")
		banner()
		select(option)

if __name__ == "__main__":
    main()

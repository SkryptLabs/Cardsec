import psutil
import socket
import os
import subprocess
import shutil
import distro
import requests
import json
import time
from termcolor import colored
from cardsec.port_scanner import scan_ports
from simple_term_menu import TerminalMenu, main
from cardsec.utils import parser, conf

GOOD=50
OK=75

try:
	LATEST = requests.get("https://pypi.org/pypi/cardsec/json").json()["info"]["version"]
	from importlib.metadata import version 
	VERSION = version('cardsec')
except: 
	VERSION = False


def num_colour(num:int):
    if num<=GOOD:
        end = colored(f"{num}%", "green")
    elif num<=OK:
        end = colored(f"{num}%", "yellow")
    else: end = colored(f"{num}%", "red")

    return end

def run_cmd(cmd):
	return subprocess.run(cmd, shell= True, text = True, stdout= subprocess.PIPE)

def node_ver():
	return subprocess.check_output(['cardano-node','version']).decode().split()[1]

def banner():
	print("                                                                      ")
	print("                                                                      ")
	print(colored("          █████╗  █████╗ ██████╗ ██████╗  ██████╗███████╗ █████╗         ", "white"))
	print(colored("         ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════ ██╔════╝██╔══██╗        ", "white"))
	print(colored("         ██║  ╚═╝███████║██████╔╝██║  ██║╚█████╗ █████╗  ██║  ╚═╝        ", "white"))
	print(colored("         ██║  ██╗██╔══██║██╔══██╗██║  ██║ ╚═══██╗██╔══╝  ██║  ██╗        ", "white"))
	print(colored("         ╚█████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗╚█████╔╝        ", "white"))
	print(colored("          ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝ ╚════╝        ", "white"))
	if VERSION and LATEST > VERSION:
		print(colored(f"                               version {VERSION}        ", "yellow"))
		print(colored(f"     		        New update {LATEST} available", "red"))
	elif VERSION:
		print(colored(f"                               version {VERSION}        ", "green"))
	print("                                                                      ")
	print(colored("                        Developed by: SkryptLabs                              ", "blue"))
	print(colored("                         twitter.com/skryptlabs             				   ", "red"))
	print("                                                                         ")


def setup():
	try:
		node_ver()
	except:
		print('Cardano Node not installed.')
		print('Skipping setup...')
		return 1
	
	print(colored("\n-------Setup---------\n", "magenta"))
	print("Is this a relay node?")
	menu1 = TerminalMenu(["[1] Yes", "[2] No"])
	menu1_choice = menu1.show()

	if menu1_choice == 0:
		conf["relay"] = "true"
		print("What network does the node use?")
		menu2 = TerminalMenu(["[1] Mainnet", "[2] Testnet"])
		menu2_choice = menu2.show()
		if menu2_choice == 0:
			conf["network"] = "mainnet"
		elif menu2_choice == 1:
			conf["network"] = "testnet"
		with open("/tmp/cardsec.conf", "w") as f:
			json.dump(conf, f)
		run_cmd('sudo cp /tmp/cardsec.conf /etc/cardsec.conf')
		print("\nSetup complete!\n")
		return 0
		
	elif menu1_choice == 1:
		conf["relay"] = "false"
		with open("/tmp/cardsec.conf", "w") as f:
			json.dump(conf, f)
		run_cmd('sudo cp /tmp/cardsec.conf /etc/cardsec.conf')
		print("\nSetup complete!\n")
		return 1
	

def system():
	menu_options = ["[1] System Info", "[2] System Load", "[3] Back"]
	terminal_menu = TerminalMenu(menu_options, title="System")
	option = terminal_menu.show()

	if option == 0:
		info()
	elif option == 1:
		load()
	elif option == 2:
		back()
		return 1

def info():
	try:
		node = node_ver()
	except: node="Not installed"

	print(colored("\n-------System Info---------", "magenta"))

	print("Distro: "+distro.id()+' '+distro.version())
	print("RAM Size: " +str(psutil.virtual_memory()[0]/1024/1024//1024)+' GB')
	print("Disk Size: " +str(psutil.disk_usage('/')[0]/1024/1024//1024)+'GB'+'\n')
	print("Cardano-Node: " + node)
	latest = requests.get(
		"https://api.github.com/repos/input-output-hk/cardano-node/releases/latest"
		).json()["tag_name"]
	if node != "Not installed" and latest <= node:
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
	
	try:
		nmap_v = subprocess.check_output(['nmap','--version']).decode().split()[2]
		print(colored("Nmap version: "+nmap_v, "green"))
	except:
		#run_cmd("sudo apt-get install nmap -y")
		print(colored("Nmap not installed.", "red"))
		print('You will need Nmap to use this feature.\n')
		return 1
	print(colored("Installing vulnerability scanning scripts....", "yellow"))
	if not os.path.exists("vulners.nse"):
		run_cmd("sudo wget https://raw.githubusercontent.com/vulnersCom/nmap-vulners/master/vulners.nse > /dev/null 2>&1")
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
			back()
			return 1		
		

def installer():
	print(colored('Experimental Feature',"red"))
	print("Use with with caution.\n")
	menu_options = ["[1] Cardano-node", "[2] Back"]
	print(colored("-------One-Click Installer---------\n", "magenta"))
	terminal_menu = TerminalMenu(menu_options)
	option = terminal_menu.show()

	if option == 0:
		print(colored("Installing Cardano-node...", "yellow"))
		try:
			subprocess.check_output(['cardano-node','version']).decode()
			path = shutil.which("cardano-node")[:-13]
			run_cmd(f"cd {path}")
		except:
			path = "/usr/local/bin"
			print(colored("No existing version found...", "yellow"))
		print(colored("Downloading Cardano-node...", "yellow"))
		download = subprocess.Popen(
			"sudo wget https://hydra.iohk.io/job/Cardano/cardano-node/cardano-node-linux/latest-finished/download --output-document latest-node.tar.xf",
			shell = True,
			cwd = path
			)
		download.wait()
		unzip = subprocess.Popen(
			"sudo tar -xf latest-node.tar.xf && sudo rm latest-node.tar.xf",
			shell = True,
			cwd = path
			)
		unzip.wait()
		print(colored("Cardano-node is now installed\n", "yellow"))
		node = node_ver()
		print(colored("Cardano-node version: "+ node, "green"))
	elif option == 1:
		back()
		return 1

def back():
	os.system("clear")
	banner()

def quit():
	os.system("clear")
	print("Happy Minting!")
	exit()


def menu():
	menu_options=[
		"[1] System", "[2] Port Scanner", "[3] Vulnerability Scanner", 
		"[4] One-Click Installer", "[5] Setup", "[6] Exit"
		]
	terminal_menu = TerminalMenu(menu_options, title="Home")
	return terminal_menu.show()


def select(option):

	menu_func = [system, scan, nmapscan, installer, setup, quit]

	print()
	return menu_func[option]()



def main():
	os.system("clear")
	banner()
	if not os.path.exists("/etc/cardsec.conf"):
		setup()
		time.sleep(2)
		os.system("clear")
		banner()

	while 1:
		option = menu()
		os.system("clear")
		banner()
		select(option)

if __name__ == "__main__":
    main()

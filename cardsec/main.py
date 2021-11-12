import typer
import psutil
import subprocess
import distro
from os import system
from termcolor import colored
from cardsec.port_scanner import scan_ports
from simple_term_menu import TerminalMenu

GOOD=50
OK=75

try:
	from importlib.metadata import version 
	VERSION = version('cardsec')
except: 
	VERSION = "Not found."


def num_colour(start:str,num:int):
    start=typer.style(start,fg=typer.colors.BRIGHT_WHITE)
    if num<=GOOD:
        end=typer.style(str(num)+'%', fg=typer.colors.GREEN, bold=True)
    elif num<=OK:
        end=typer.style(str(num)+'%', fg=typer.colors.YELLOW, bold=True)
    else: typer.style(str(num)+'%', fg=typer.colors.RED, bold=True)

    return start+end


def banner():
	print("                                                                      ")
	print("                                                                      ")
	print(colored("          █████╗  █████╗ ██████╗ ██████╗  ██████╗███████╗ █████╗         ", "white"))
	print(colored("         ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════ ██╔════╝██╔══██╗        ", "white"))
	print(colored("         ██║  ╚═╝███████║██████╔╝██║  ██║╚█████╗ █████╗  ██║  ╚═╝        ", "white"))
	print(colored("         ██║  ██╗██╔══██║██╔══██╗██║  ██║ ╚═══██╗██╔══╝  ██║  ██╗        ", "white"))
	print(colored("         ╚█████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗╚█████╔╝        ", "white"))
	print(colored("          ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝ ╚════╝        ", "white"))
	print(f"                               version {VERSION}                     ")
	print("                                                                      ")
	print(colored("                        Developed by: SkryptLabs                              ", "blue"))
	print(colored("                         twitter.com/skryptlabs             				   ", "red"))
	print("                                                                         ")


def info():
    try:
        node=subprocess.check_output(['cardano-node','version']).decode().split()[1]
    except: node="Not found."

    typer.secho("\n-------System Info---------",fg=typer.colors.MAGENTA,bold=True)

    typer.echo("Distro: "+distro.id()+' '+distro.version())
    typer.echo("RAM Size: " +str(psutil.virtual_memory()[0]/1024/1024//1024)+' GB')
    typer.echo("Disk Size: " +str(psutil.disk_usage('/')[0]/1024/1024//1024)+'GB'+'\n')
    typer.echo("Cardano-Node: " +node)


def load():
    #cpu_load=(psutil.getloadavg()[2]/psutil.cpu_count())*100
    cpu_load=psutil.cpu_percent()
    ram_load=psutil.virtual_memory()[2]
    disk_load=psutil.disk_usage('/')
    
    typer.secho("\n-------System Load---------",fg=typer.colors.MAGENTA,bold=True)
    
    typer.echo(num_colour("CPU usage: ",cpu_load))
    typer.echo(num_colour("RAM usage: ",ram_load))
    typer.echo(num_colour("Disk usage: ",disk_load[3])+'\n')


def scanner(port_range):
	port_list=scan_ports(port_range)
	if port_list:
		print(colored("The following ports were found open:", "magenta"))
		for i in port_list:
			print(i)
		print(colored("Note: Only keep 2 outgoing ports open. (SSH & Node port)", "red"))
		print("")
	else: print(colored("No ports open!", "red"))


def scan():
	print(colored("-------Port Scanner---------", "magenta"))
	def submenu():
		menu_options=["[1] Light Scan - 6000 ports", "[2] Exhaustive Scan - 64000 ports", "[3] Back"]
		terminal_menu = TerminalMenu(menu_options, title="Scan")
		return terminal_menu.show()

	while 1:
		print('')
		suboption = submenu()
		

		if suboption == 0:
			port_range=6000
			print(f"Scanning {port_range} ports...")
			scanner(port_range)			
		      
		elif suboption == 1:
			port_range=64000
			print(f"Scanning {port_range} ports...")
			scanner(port_range)

		elif suboption == 2:
			break		
		

def menu():
	menu_options=["[1] System Info", "[2] System Load", "[3] Port Scanner", "[4] Vulnerability Scanner", "[5] Exit"]
	terminal_menu = TerminalMenu(menu_options, title="Home")
	return terminal_menu.show()


def select(option):	
	print("")
	if option == 0:
		info()	
	elif option == 1:
		load()
	elif option == 2:
		scan()
	elif option == 3:
		print("Coming Soon....")
	elif option == 4:
		system("clear")
		print("Happy Minting!")
		exit()



app=typer.Typer(invoke_without_command=True)
system("clear")
banner()
while 1:
	option = menu()
	system("clear")
	banner()
	select(option)
